from absl import app
from typing import List, Optional

import pandas as pd
import numpy as np
import json

import sys, os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)

import OptimizationCalculusKernel as gock
from DataSets.Example import MultiPropertiesData as mpd
from DataSets.Workshop import Workshop
from Interface.Interface import (
    ICapacity, IDemandFixed
)
import datetime


class CircularSequenceSchedulingSolver:

    def __init__(self) -> None:
        pass

    def import_result(
            self, file: str=''
    ) -> pd.DataFrame:
        return pd.read_csv(file)

    def export_result(
            self, result: pd.DataFrame, file: str=''
    ) -> None:
        if os.path.exists(file):
            os.remove(file)

        result.to_csv(file)

    def preprocess(self, demand: IDemandFixed) -> IDemandFixed:
        """ 数据预处理
            1. 处理出件率为0的情况
               if pro == 0, then pro = num
            2. 整倍数处理以及bias设定, 注: bias 表示整倍数处理后的余量 residue
               正向: num' = ceil(num / pro), bias = num'*pro - num
               还原: num = num' * pro - bias
            3. 可搭配合并
        """

        # 整倍数及余量处理
        for i, row in demand.data.iterrows():
            if row.productivity == 0:
                demand.data.loc[i,'productivity'] = row.number
                demand.data.loc[i,'number'] = 1
            else:
                oldnum = row.number
                newnum = int(np.ceil(oldnum / row.productivity))
                demand.data.loc[i,'number'] = newnum
                demand.data.loc[i,'bias'] = newnum * row.productivity - oldnum

        # 构造 padding 填充因子
        type_id = demand.data.type.max() + 1
        demand.data.loc[len(demand.data.index)] = [
            demand.data.id.max() + 1,  # id
            type_id,  # type
            # 注: padding 的值必须保持为最大的唯一值, 此处选择 1e5
            # demand.data.color.max() + 1,  # color
            1e5,                # color
            1e5, 1, 0,          # 数量(足够大), 产出率, 整倍数余量
            1e5,                # 产能上限, 此处需要选取一个足够大的值
            1e5,                # 并行加工标记值, 此处需选取一个唯一值
            1e5,                # 共用产能标记值, 此处需选取一个唯一值
            '空载',             # name
            'EMPTY',            # code
            'Padding'           # property_1 name / color name
        ]
        demand.production_ids.append(type_id)

        # 对并行加工(该场景下称为搭配加工)进行合并处理
        self.recode, droplist = {}, []
        grp = demand.data.groupby(['sync'])
        for a, g in grp:
            __key, __ids = a[0], g.id.values

            if __key <= 0:
                continue

            for e in __ids:
                if __key not in self.recode:
                    self.recode[__key] = e
                else:
                    i = demand.data[demand.data['id']==e].index
                    # demand.data.loc[i,'bias'] = demand.data.loc[i,'number']
                    demand.data.loc[i,'number'] = 0
                    # droplist.append(i[0])

        return demand

    def postprocess(
            self, demand: IDemandFixed, result: pd.DataFrame
    ) -> pd.DataFrame:
        """
        1. 扣除 bias
        2. [Optional] 旋转, 去除空置
        3. 还原搭配合并(注: 同样会导致扣除 bias)
        """

        names = ['' for i in range(result.shape[0])]
        codes = ['' for i in range(result.shape[0])]
        colors = ['' for i in range(result.shape[0])]
        numbers = [0 for i in range(result.shape[0])]

        for i, row in result.iterrows():
            j = demand.data[demand.data.id == row.id].index

            # 还原加工量 num' = num * batch - bias
            # row.number = \
            # result.loc[i].number = \
            #     row.number * demand.data.loc[j].productivity - \
            #     demand.data.loc[j].bias

            numbers[i] = int(
                row.number * demand.data.loc[j].productivity.values[0] -
                demand.data.loc[j].bias.values[0])
            names[i] = demand.data.loc[j].name.values[0]
            codes[i] = demand.data.loc[j].code.values[0]
            colors[i] = demand.data.loc[j].property_1.values[0]

        result['name'] = names
        result['code'] = codes
        result['color'] = colors
        result['number'] = numbers
        result['seq'] = [
            i % self.capacity for i in range(result.shape[0])
        ]

        data = list(result['cid'])
        colseq = [
            x for i, x in enumerate(data)
            if x not in data[:i]]

        grps = {}
        temp = result[result['cyc']==1]
        colorgroup = temp.groupby(['cid'])
        for a, b in colorgroup:
            typegroup = b.groupby(['id'])

            _list = []
            for c, d in typegroup:
                _list.append(d)
            grps[a[0]] = pd.concat(_list)

        groups = []
        for key in colseq:
            if key in grps:
                groups.append(grps[key])
        ret = pd.concat(groups)

        __seq = list(ret['seq'])
        record = {__seq[i]: i for i in range(ret.shape[0])}

        __cyc = list(result['cyc'])
        __seq = list(result['seq'])
        new_index = [
            (__cyc[i]-1)*self.capacity + record[__seq[i]]
            for i in range(result.shape[0])
        ]

        # 贪心式处理
        # result['seq'] = new_index
        # result.sort_values(by=['seq'], inplace=True)
        result.drop(['seq'], axis=1)

        # self.export_result('result.csv', result)

        return result

    def display_result(self):
        data = self.engine.business.data.get_result(
            self.engine.business.scene.code
        )

        if data is None:
            return
        obj = self.engine.business.scene.form

        flag = np.zeros(data.shape, dtype=int)
        for i in range(data.size):
            flag.flat[i] = (data.flat[i] > 0)

        df = pd.DataFrame(flag.astype(int), columns=obj.codes)

        seq = np.zeros((data.shape[0],), dtype=int)
        result = self.engine.demand.data.copy()
        for i in range(data.shape[0]):
            seq[i] = np.dot(flag[i,:], obj.codes)
            result.loc[i] = self.engine.demand.data[
                self.engine.demand.data.type == seq[i]
            ].values[0]
        result['number'] = [np.sum(data[k,:]) for k in range(data.shape[0])]

        slices = []
        df, cyc_len = result[['same']], obj.cyc_len

        if self.engine.capacity is not None:
            conf = pd.DataFrame(
                self.engine.capacity.loc[:cyc_len-1, 'same'].values,
                columns=['cap_conf']
            )
            conf.reset_index(drop=True, inplace=True)
            slices.append(conf)

        for i in range(obj.ncycs):
            s, e = i * cyc_len, (i + 1) * cyc_len
            slice = pd.DataFrame(df.iloc[s:e])
            slice.reset_index(drop=True, inplace=True)
            slices.append(slice)

        all = pd.concat(slices, axis=1)
        all['number'] = [np.sum(data[k,:]) for k in range(cyc_len)]

        stat = np.zeros(data.shape[1], dtype=int)
        for i in range(data.shape[1]):
            stat[i] = np.sum(data[:,i])
        print(stat)

        from pandasgui import show
        show(
            all=all.T.astype(int),
            origin=result
        )

    def display_with_style(
            self,
            data: pd.DataFrame
    ) -> None:
        pd.set_eng_float_format(accuracy=4, use_eng_prefix=True)
        with pd.option_context(
                'display.max_rows', None,
                'display.max_columns', None,
                'display.width', 1000,
                'display.precision', 1,
                'display.html.table_schema', True,
                'display.colheader_justify', 'right'):
            print(data)

    def create_engine(
            self,
            cyc_len: int,
            cyc_num: int,
            demand: IDemandFixed,
            capacity: Optional[List[ICapacity]]=None
    ) -> None:
        self.engine = gock.CircularSequenceEngine(
            cyc_len=cyc_len,
            cyc_num=cyc_num,
            demand=demand,
            capacity=capacity
        )


def read_config(file: str='conf.ini') -> dict:
    from configparser import ConfigParser

    cfg = ConfigParser()
    cfg.read(file)
    return dict(cfg.items())

def main(argv) -> None:
    solver = CircularSequenceSchedulingSolver()

    data = Workshop.get_data().copy()
    config = dict(read_config('conf.ini')['solver'])
    cap_conf = solver.import_result(
        '~/workspace/data/scheduling0204-19-day.csv'
    )

    properties = ['type', 'color', 'same']
    solver.create_engine(
        cyc_len=40,             # 30~50
        # cyc_len=160,
        cyc_num=3,
        demand=solver.preprocess(
            IDemandFixed(
                data, properties, 'type', 'number'
            )
        ),
        # capacity=cap_conf[['same', 'number']].astype(int)
        capacity=None
    )

    solver.engine.setup(mode=1)
    solver.engine.create_capacity_constraints()
    solver.engine.create_demand_constraints()
    solver.engine.create_inventory_constraints()
    # solver.engine.create_kitting_constraints()
    # solver.engine.create_circular_capacity_constraint(
    #     # {1:140, 2:140, 3:140}
    #     150
    # )
    solver.engine.create_changeover_constraints(
        field_index=properties.index('color'),
        values=sorted(set(data['color'][:-1]))
    )
    solver.engine.create_circular_changeover_constraints(
        field_index=properties.index('same'),
        values=sorted(set(data['same'][:-1]))
    )

    # from pyarmor_runtime_005890 import __pyarmor__
    # print(str(__pyarmor__(1, None, b'hdinfo', 1)))
    # print('bind data is', __pyarmor__(0, None, b'keyinfo', 1))
    # import time
    # print(
    #     'expired epoch is',
    #     time.strftime(
    #         "%Y-%m-%d %H:%M:%S",
    #         time.localtime(__pyarmor__(1, None, b'keyinfo', 1))
    #     )
    # )

    # 目标函数中的各权重为配置项
    solver.engine.create_objective(
        {
            'capacity_changeover': 1,
            'color_changeover': 0
        }
    )
    result = solver.engine.run(config=config)

    times = 1
    solver.engine.create_objective(
        {
            'capacity_changeover': 1,
            'color_changeover': 1e-1
        }
    )
    for i in range(times):
        result = solver.engine.run(
            history=result,
            config=config
        )

    solver.display_result()


if __name__ == '__main__':
    app.run(main)
