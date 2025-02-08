import pandas as pd
import numpy as np
import dataclasses

from typing import List, Optional
from abc import ABC, abstractmethod

import datetime


@dataclasses.dataclass(frozen=False)
class TimeLineUnit:
    """ 离散时间单元
    """
    index: int=dataclasses.field(default_factory=int)  # time seq id
    scale: int=dataclasses.field(default_factory=int)  # e.g. 8*60*60 seconds
    status: int=dataclasses.field(default_factory=int)  # -1, 0, 1
    used: float=dataclasses.field(default_factory=float)  # in [0, 1]

    time: datetime=dataclasses.field(default_factory=datetime)
    # 距离起始时刻的偏移时长, 可用于构建库存周期/成本约束
    duration: int=dataclasses.field(default_factory=int)


class TimeLine:
    def __init__(self, units: List[TimeLineUnit]) -> None:
        self.units = units

    def length(self) -> int:
        return len(self.units)

    def index(self, dt: datetime) -> int:
        _dt = max(dt, self.units[0].time)
        _dt = min(dt, self.units[-1].time)
        for i in range(self.length()):
            if _dt.day == self.units[i].time.day:
                return i

    def availables(self):
        timelen = self.length()
        unused = np.array(
            [self.units[t].scale for t in range(timelen)],
            dtype=float
        )
        for t in range(timelen):
            unused[t] *= (1-self.units[t].used)  # 可用加工时长
            if self.units[t].status == 0:  # 该时段不可用
                unused[t] = 0

        return unused


@dataclasses.dataclass(frozen=True)
class ICalendar:
    """ 业务层描述
    """

    def toTimeLine(self) -> TimeLine:
        pass


class IDemand(ABC):
    def __init__(
            self,
            data: pd.DataFrame,
            props: List[str]=[],
            id_field: str='id',
            number_field: str='number'
    ) -> None:
        self.__data = data
        self.__props = props
        self.__id_field = id_field
        self.__number_field = number_field
        self.__productions = sorted(list(set(data[id_field])))

    @property
    def data(self):
        return self.__data
    @data.setter
    def data(self, data):
        self.__data = data

    @property
    def id_field(self) -> str:
        return self.__id_field

    @property
    def number_field(self) -> str:
        return self.__number_field

    @property
    def properties(self) -> List[str]:
        return self.__props

    @property
    def production_ids(self):
        return self.__productions

    def statistic(
            self,
            *,
            properties: Optional[List[str]]=None
    ) -> (np.ndarray, list, list):
        """ 需求统计
        """

        _props = []
        if properties is not None:
            for p in self.data.columns:
                if p == number_field:
                    continue

                # _props中的元素需要保持在data.columns中的顺序
                if p in properties:
                    _props.append(p)
        else:
            _props = self.properties

        grouped = self.data.groupby(_props, as_index=False)
        statistic = grouped[self.number_field].sum()
        # 按照id排列 recodes
        statistic.sort_values(by=self.id_field, inplace=True)
        values = statistic.values

        return values[:,:-1], list(values[:,-1]), self.production_ids


class IDemandFixed(IDemand):
    def __init__(
            self,
            data: pd.DataFrame,
            props: List[str]=[],
            id_field: str='id',
            number_field: str='number'
    ) -> None:
        super().__init__(data, props, id_field, number_field)

        self.__productivity = np.ones(data.shape[0], dtype=int)

    @property
    def productivity(self):
        return self.__productivity
    @productivity.setter
    def productivity(self, productivity: np.ndarray):
        self.__productivity = productivity


class IDemandTimed(IDemand):

    def __init__(
            self,
            data: pd.DataFrame,
            calendar: TimeLine,
            props: List[str]=['production'],
            id_field: str='id',
            number_field: str='number'
    ) -> None:
        super().__init__(data, props, id_field, number_field)

        self.__calendar = calendar

        timelen = calendar.length()
        day_idx = {}       # 将日期映射为时间区间索引
        grouped = data.groupby(['delivery_time'])
        for index, _ in grouped:
            _date = index[0]
            day_idx[_date] = calendar.index(_date)
        del grouped

        # self.__produtions = sorted(list(set(data['production'])))
        self.__id_idx = {}
        __l = len(self.production_ids)
        for i in range(__l):
            self.__id_idx[self.production_ids[i]] = i

        _dim = len(self.production_ids)
        self.__fixed_batch_size = np.ones(_dim, dtype=int)
        self.__supplements = np.zeros(_dim, dtype=int)
        self.__quantity = np.zeros((timelen, _dim), dtype=int)
        self.__quantity_acc = np.zeros(
            self.__quantity.shape, dtype=int
        )

        for i in range(data.shape[0]):
            _rec = data.iloc[i]
            t = _rec['delivery_time']
            p = _rec['production']
            n = _rec['number']
            r = day_idx[t]
            c = self.production_ids.index(p)
            self.__quantity[r,c] += n

        for r in range(self.__quantity.shape[0]):
            self.__quantity_acc[r,:] = self.__quantity[r,:]
            if r != 0:
                self.__quantity_acc[r,:] +=  self.__quantity_acc[r-1,:]

    def get_index(self, index: int=-1) -> int:
        if index in self.__id_idx:
            return self.__id_idx[index]
        return -1

    def select(self, productions=None) -> IDemand:
        if productions is None:
            return self

        selected = self.data[
            self.data['production'].isin(productions)
        ]
        return IDemandTimed(
            selected,
            self.calendar,
            self.properties,
            self.id_field,
            self.number_field
        )

    def snps(self, ids=None) -> np.ndarray:
        """ 整倍数加工
        """

        id_list = ids
        if not ids:
            id_list = self.production_ids

        selected = [
            self.data[self.data['production'] == p] for p in id_list
        ]

        return np.array(
            [int(min(e['value'].values)) for e in selected]
        )

    def inventory_limits(self, ids=None) -> np.ndarray:
        id_list = ids
        if not ids:
            id_list = self.production_ids

        selected = [
            self.data[self.data['production'] == p] for p in id_list
        ]

        return np.array(
            [int(min(e['value_prop_2'].values)) for e in selected]
        )

    @property
    def supplements(self):
        return self.__supplements
    @supplements.setter
    def supplements(self, supplements: np.ndarray):
        self.__supplements = supplements

    @property
    def fixed_batch_size(self):
        return self.__fixed_batch_size
    @fixed_batch_size.setter
    def fixed_batch_size(self, size: np.ndarray):
        self.__fixed_batch_size = size

    @property
    def calendar(self):
        return self.__calendar

    @property
    def quantity(self):
        return self.__quantity
    @property
    def quantity_acc(self):
        return self.__quantity_acc


class ICapacity:

    def __init__(
            self,
            data: pd.DataFrame,
            workcenter_id: int,
            calendar: TimeLine
    ) -> None:
        self.data = data
        self.calendar = calendar
        self.__workcenter_id = workcenter_id

    @property
    def id(self):
        return self.__workcenter_id

    @property
    def production_ids(self):
        return list(set(self.data['prod']))

    def syncs(self, ids=None):
        id_list = ids
        if not ids:
            id_list = self.production_ids
        selected = [
            self.data[self.data['prod'] == p] for p in id_list
        ]

        return np.array(
            [min(e.sync.values) for e in selected]
        )

    def productivities(self, ids=None):
        id_list = ids
        if not ids:
            id_list = self.production_ids
        selected = [
            self.data[self.data['prod'] == p] for p in id_list
        ]

        return np.array(
            [min(e.productivity.values) for e in selected]
        )

    def OEEs(self, ids=None):
        id_list = ids
        if not ids:
            id_list = self.production_ids
        selected = [
            self.data[self.data['prod'] == p] for p in id_list
        ]

        return np.array(
            [min(e.OEE.values) for e in selected]
        )

    def shift_times(self, ids=None):
        id_list = ids
        if not ids:
            id_list = self.production_ids
        # selected = [
        #     self.data[self.data['prod'] == p] for p in id_list
        # ]

        # return np.array(
        #     [min(e.sync.values) for e in selected]
        # )
        return np.array(
            [60*60 for i in id_list]
        )

    def processing_times(self, ids=None):
        id_list = ids
        if not ids:
            id_list = self.production_ids
        _len = len(id_list)

        selected = [
            self.data[self.data['prod'] == p] for p in id_list
        ]

        oees = np.array(
            [min(e.OEE.values) for e in selected]
        )
        durations = np.array(
            [min(e.processing_time.values) for e in selected]
        )

        for i in range(_len):
            if oees[i] > 0 and oees[i] <= 100:
                durations[i] = durations[i] * 100 / oees[i]

        # just for testing!
        durations.fill(1.8)
        # durations.fill(1.)
        # end testing

        return durations


class IOrganization:
    pass


class KittingProcess:
    """ 处理齐套, 将齐套信息转化为条件
    """

    def __init__(self) -> None:
        pass

    @staticmethod
    def to_kitting_condition(
            ingredient: pd.DataFrame,
            kitting_information: pd.DataFrame,
            calendar: TimeLine,
            productions: List[int],
            materials: List[int]
    ) -> (np.ndarray, np.ndarray):
        """ return matrix A and B """
        num_p = len(productions)
        num_t = calendar.length()
        num_m = len(materials)

        if num_p == 0 or num_t == 0 or num_m == 0:
            return np.array([]), np.array([])

        tidx, pidx, midx = {}, {}, {}
        for t in range(num_t):
            tidx[calendar.units[t].index] = t

        for p in range(num_p):
            pidx[productions[p]] = p

        for m in range(num_m):
            midx[materials[m]] = m

        matA = np.zeros((num_p, num_m), dtype=int)
        matB = np.zeros((num_t, num_m), dtype=int)

        for index, row in ingredient.iterrows():
            i = pidx[row.production]
            j = midx[row.material]

            matA[i,j] = row.number

        for index, row in kitting_information.iterrows():
            i = tidx[row.time_unit]
            j = midx[row.material]

            matB[i,j] += row.number

        for r in range(num_t):
            if r == 0:
                continue
            matB[r,:] += matB[r-1,:]

        return matA, matB


class Preprocessing:
    def __init__(
            self,
            demand: IDemandTimed,
            capacity: pd.DataFrame,
            workcenter: List[str]
    ) -> None:
        self.demand = demand

        join = set(workcenter) & set(capacity.columns)
        self.line_groups = capacity.groupby(
            list(join),
            as_index=False
        )

    def get_capacity_list(
            self,
            calendar: TimeLine
    ) -> List[ICapacity]:
        caps = []
        for index, line in self.line_groups:
            caps.append(
                ICapacity(line, index[0], calendar)
            )

        return caps

    def check_sync(self):
        """ 检查并行加工的数量是否一致, 不一致会导致部分加工
            返回: 需要增补的数量
        """
        supplements = np.zeros(
            len(self.demand.production_ids), dtype=int
        )

        for _, capacity in self.line_groups:
            _products = list(set(capacity['prod']))

            syncs = capacity.groupby(['sync'])
            for s in syncs:
                _prods = list(s[1]['prod'])
                if len(_prods) <= 1:
                    continue

                _cols = [self.demand.get_index(p) for p in _prods]
                _nums = [
                    self.demand.quantity_acc[-1,c] +
                    self.demand.supplements[c]
                    for c in _cols
                ]

                for i in range(len(_cols)):
                    supplements[_cols[i]] = max(_nums) - _nums[i]

        return supplements

    def check_fixed_batch_size(self):
        """ 检查需求量是否满足整批量加工要求
            返回: 需要增补的需求数量
        """
        dim = len(self.demand.production_ids)
        fix_batch_sizes = self.demand.fixed_batch_size
        supplements = np.zeros(dim, dtype=int)

        quantity = self.demand.quantity_acc[-1,:] + \
            self.demand.supplements
        for i in range(dim):
            if fix_batch_sizes[i] == 0 or quantity[i] == 0:
                continue

            res = quantity[i] % fix_batch_sizes[i]
            if res != 0:
                supplements[i] = fix_batch_sizes[i] - res

        return supplements

    def round_fixed_batch_size(self):
        """ 增补量可以是负值，用于逐精度逼近方式
        """
        dim = len(self.demand.production_ids)
        fix_batch_sizes = self.demand.fixed_batch_size
        supplements = np.zeros(dim, dtype=int)

        quantity = self.demand.quantity_acc[-1,:] + \
            self.demand.supplements
        for i in range(dim):
            if fix_batch_sizes[i] == 0 or quantity[i] == 0:
                continue

            res = quantity[i] % fix_batch_sizes[i]
            if res == 0:
                continue
            if res * 2 >= snp[i]:
                supplements[i] = fix_batch_sizes[i] - res
            else:
                supplements[i] = -res

        return supplements

    def justify(self, batch_size=None):
        """ 通过增补虚拟需求量，使得需求满足并行加工以及整批量条件
        """
        if batch_size == None:
            pass
        else:
            pass

    def extern_calendar(self):
        pass
