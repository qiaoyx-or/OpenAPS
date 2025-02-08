from absl import app

import numpy as np
import pandas as pd
from pandasgui import show

from pathlib import Path
import sys, os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)

from Interface.Interface import *
from Interface.ExportSqliteData import *
import datetime


class AnalysisOfResult:
    """ 分析服务于决策。
        围绕3个坐标轴: 时间、产能、制品
    """
    def __init__(self, db_file: str):
        self.__db_file = db_file
        self._dt_mapper = {}

        self.coord_dt: List[int]
        self.coord_cap: List[int]
        self.coord_prod: List[int]

        self.process: Preprocessing

    def setup(self, capacity_group=['line']):
        units, order, craft = import_base_data(self.__db_file)

        for i in range(units.shape[0]):
            d = units.iloc[i].date_time.date()
            self._dt_mapper[d] = i

        self.calendar = TimeLine([   # 生产日历
            TimeLineUnit(
                int(units.iloc[i].id),
                int(units.iloc[i].scale),
                int(units.iloc[i].status),
                float(units.iloc[i].used),
                units.iloc[i].date_time,
                int(units.iloc[i].id * units.iloc[i].scale)
            ) for i in range(units.shape[0])
        ])

        demand = IDemand(order, self.calendar)
        self.coord_dt = sorted(list(set(units.id)))
        self.coord_prod = demand.production_ids
        self.coord_cap = list(set(craft.line))

        self.process = Preprocessing(
            demand, craft, capacity_group
        )

        return self


    def get_result(self) -> List[pd.DataFrame]:
        result = pd.DataFrame(
            import_planning_result(self.__db_file)
        )
        if result.size == 0:
            return []

        colname, rowname = {}, {}
        data = self.process.demand.data
        for p in self.coord_prod:
            colname[p] = data[data['production'] == p].name.iloc[0]
        for u in self.calendar.units:
            rowname[u.index] = u.time.date()

        plan = {}
        grouped = result.groupby(['line'])
        for index, line in grouped:
            _outputs = {
                t: {
                    self.coord_prod[i]: 0 for i in range(
                        len(self.coord_prod)
                    )
                } for t in self.coord_dt
            }
            for t in self.coord_dt:
                selected = line[line['time_unit'] == t]
                for p in selected.production.values:
                    n = selected[selected.production == p].number.sum()
                    _outputs[t][p] += n

            _plan = pd.DataFrame(_outputs).T
            _plan.rename(rowname, inplace=True)
            _plan.rename(colname, axis=1, inplace=True)

            plan[index[0]] = _plan

        return plan


    def get_plan(self) -> List[pd.DataFrame]:
        result = pd.DataFrame(
            import_planning_result(self.__db_file)
        )
        if result.size == 0:
            return []

        colname, rowname = {}, {}
        data = self.process.demand.data
        for p in self.coord_prod:
            colname[p] = data[data['production'] == p].name.iloc[0]
        for u in self.calendar.units:
            rowname[u.index] = u.time.date()

        plan = {}
        grouped = result.groupby(['line'])
        for index, line in grouped:
            prods = list(set(line.production))
            _outputs = {
                t: {
                    p: 0 for p in prods
                } for t in self.coord_dt
            }
            for t in self.coord_dt:
                selected = line[line['time_unit'] == t]
                for p in prods:
                    n = selected[selected.production == p].number.sum()
                    _outputs[t][p] += n

            _plan = pd.DataFrame(_outputs).T
            for i in range(_plan.shape[0]-1, 0, -1):
                _plan.iloc[i] -= _plan.iloc[i-1]

            # _plan.rename(rowname, inplace=True)
            # _plan.rename(colname, axis=1, inplace=True)
            plan[index[0]] = _plan

        return plan


    def get_demand(self) -> IDemand:
        return self.process.demand


    def workload_analysis(self):
        """ 工作负荷分析: 可用加工时长与实际加工时长的对比
        """
        pass


    def OTD_analysis(self):
        """ 交付满足情况分析:
        1. 展示需求与实际产出量间的关系
        2. 展示交付量、欠交量以及库存量

        """
        plan = 0
        sub_plans = self.get_result().values()
        for p in sub_plans:
            plan += p

        demand = pd.DataFrame(
            self.get_demand().quantity_acc,
            index=plan.index,
            columns=plan.columns
        )
        otd = plan - demand
        show(plan, demand, otd)

        return otd


    def kitting_analysis(self):
        material, ingredient, kitting = import_kitting_information(
            self.__db_file
        )

        mname = {}
        for index, row in material.iterrows():
            mname[row.id] = row['name']

        matA, matB = KittingProcess.to_kitting_condition(
            ingredient, kitting,
            self.calendar, self.coord_prod,
            list(mname.keys())
        )

        pname, tname = {}, {}
        data = self.process.demand.data
        for p in self.coord_prod:
            pname[p] = data[data['production'] == p].name.iloc[0]
        for u in self.calendar.units:
            tname[u.index] = u.time.date()

        dfA = pd.DataFrame(
            matA,
            index=list(pname.values()),
            columns=list(mname.values())
        )
        dfB = pd.DataFrame(
            matB,
            index=list(tname.values()),
            columns=list(mname.values())
        )

        return dfA, dfB


    def capacity_analysis(self):
        """ 产能情况分析: 展示不可用、计划使用、空闲时间
        """
        # workload waittime idletime
        plans = self.get_plan()

        capacities = self.process.get_capacity_list(self.calendar)
        for cap in capacities:
            prods = cap.production_ids
            syncs = cap.syncs(prods)
            plan = plans[cap.id]

            dim_p, dim_t = len(prods), len(self.coord_dt)
            mask = np.zeros(dim_p, dtype=int)
            recode = {}
            for i in range(dim_p):
                k = syncs[i]
                if k not in recode:
                    recode[k] = i
                    mask[i] = 1
            del recode

            ava = cap.calendar.availables()
            pts = cap.processing_times(prods)
            ptv = cap.productivities(prods)
            sft = cap.shift_times(prods)
            idles = np.zeros(dim_t, dtype=float)

            for i in range(dim_t):
                nums = np.divide(
                    np.array(plan.iloc[i]),
                    ptv
                )
                loads = np.multiply(nums, pts)
                waits = np.zeros(dim_p, dtype=float)
                for j in range(dim_p):
                    if nums[j] == 0:
                        continue
                    waits[j] = max(0, sft[j] - loads[j])

                idles[i] = (ava[i] - np.dot(loads + waits, mask)) / 60.
                idles[i] = round(idles[i])

            print(idles)


    def inventory_analysis(self):
        """ 库存情况分析
        """
        pass


    def satisfactory_rate(self):
        """ 约束满足率分析
        """
        pass


def main(argv) -> None:
    from pathlib import Path
    dirname = Path(__file__).parent.parent.parent
    database = dirname.joinpath("DataSets/Example/stamping_workshop.db")

    analy = AnalysisOfResult(database)
    analy.setup()

    # analy.get_result()
    analy.OTD_analysis()
    # analy.capacity_analysis()
    # analy.kitting_analysis()


if __name__ == '__main__':
    app.run(main)
