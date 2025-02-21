from absl import app
from typing import List, Optional

import pandas as pd
import numpy as np

import sys, os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)

import OptimizationCalculusKernel as GOCK
from Interface.Interface import (
    ICapacity, IDemandFixed
)


class CircularSequenceSchedulingSolver:

    def __init__(self, config=None) -> None:
        self.config = config

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

        # 构造 padding 填充因子, 注: padding 的值必须保持为最大的唯一值
        # 此处选择 1e5
        new_code = demand.data.production_code.max() + 1
        demand.data.loc[len(demand.data.index)] = [
            new_code,           # production_code
            'no-load', 1e5,     # production_name, color_code
            'padding', 1e5, 1,  # color_name, material_code, productivity
            1e5, 1e5,           # container_cap, sync
            1e5, 1e5,           # container_type, container_code
            1e5, 0              # number, bias
        ]
        demand.production_ids.append(new_code)

        # 对并行加工(该场景下称为搭配加工)进行合并处理
        self.recode = {}
        grp = demand.data.groupby(['sync'])
        for a, g in grp:
            __key, __ids = a[0], g.production_code.values
            if __key == '':     #  or __key.isna()
                continue

            for e in __ids:
                if __key not in self.recode:
                    self.recode[__key] = e
                else:
                    i = demand.data[demand.data['production_code']==e].index
                    demand.data.loc[i,'number'] = 0

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
            j = demand.data[
                demand.data.production_code == row.production_code
            ].index

            # 还原加工量 num' = num * batch - bias
            # row.number = \
            # result.loc[i].number = \
            #     row.number * demand.data.loc[j].productivity - \
            #     demand.data.loc[j].bias

            numbers[i] = int(
                row.number * demand.data.loc[j].productivity.values[0] -
                demand.data.loc[j].bias.values[0])
            names[i] = demand.data.loc[j].production_name.values[0]
            codes[i] = demand.data.loc[j].production_code.values[0]
            colors[i] = demand.data.loc[j].color_name.values[0]

        result['production_name'] = names
        result['production_code'] = codes
        result['color_name'] = colors
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
        __result = self.engine.demand.data.copy()

        for i in range(data.shape[0]):
            seq[i] = np.dot(flag[i,:], obj.codes)
            if seq[i] == 0:
                seq[i] = obj.codes[-1]
            __result.loc[i,:] = self.engine.demand.data[
                self.engine.demand.data.production_code == seq[i]
            ].values[0]
        __result['number'] = [
            np.sum(data[k,:]) for k in range(data.shape[0])
        ]

        slices = []
        df, cyc_len = __result[['container_code']], obj.cyc_len

        if self.engine.capacity is not None:
            conf = pd.DataFrame(
                self.engine.capacity.loc[:cyc_len-1, 'container_code'].values,
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
            origin=__result
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
        self.engine = GOCK.CircularSequenceEngine(
            cyc_len=cyc_len,
            cyc_num=cyc_num,
            demand=demand,
            capacity=capacity
        )


def read_config(file: str='conf.ini') -> dict:
    from configparser import ConfigParser

    cfg = ConfigParser()
    cfg.read(file, encoding='utf-8')
    return cfg

def create_solver() -> CircularSequenceSchedulingSolver:
    import pathlib

    folder = pathlib.Path(__file__).parent.resolve()
    config = read_config(f'{folder}/conf.ini')
    properties = ['production_code', 'color_code', 'container_code']

    solver = CircularSequenceSchedulingSolver(config)

    path = f'{folder.parent.parent}/DataSets/InjectionMoldingWorkshop'
    cap_conf = solver.import_result(f'{path}/FirstShift.csv')
    base_data = pd.read_csv(f'{path}/BaseData.csv')
    order = pd.read_csv(f'{path}/SecondShift.csv')
    raw_data = pd.merge(
        base_data, order, on='production_code', sort=False
    )
    raw_data['bias'] = 0
    demand=solver.preprocess(
        IDemandFixed(
            raw_data.copy(), properties, 'production_code', 'number'
        )
    )

    solver.create_engine(
        # cyc_len=160,  # when setup_mode == 0
        cyc_len=40,             # 30~50
        cyc_num=3,
        demand=demand,
        # capacity=cap_conf[['container_code', 'number']].astype(int)
        capacity=None
    )
    m = config.getint('constraints', 'setup_mode')
    if m is None:
        m = 1
    solver.engine.setup(mode=m)

    if config.getboolean('constraints', 'enable_capacity_cons'):
        solver.engine.create_capacity_constraints()
    if config.getboolean('constraints', 'enable_demand_cons'):
        solver.engine.create_demand_constraints()
    if config.getboolean('constraints', 'enable_inventory_cons'):
        solver.engine.create_inventory_constraints()
    if config.getboolean('constraints', 'enable_kitting_cons'):
        solver.engine.create_kitting_constraints()
    if config.getboolean('constraints', 'enable_circular_capacity_cons'):
        solver.engine.create_circular_capacity_constraint(
            # {1:140, 2:140, 3:140}
            150
        )
    if config.getboolean('constraints', 'enable_changeover_cons'):
        solver.engine.create_changeover_constraints(
            field_index=properties.index('color_code'),
            values=sorted(raw_data['color_code'].unique())[:-1]

        )
    if config.getboolean('constraints', 'enable_circular_changeover_cons'):
        solver.engine.create_circular_changeover_constraints(
            field_index=properties.index('container_code'),
            values=sorted(raw_data['container_code'].unique())[:-1]
        )

    objective_weights = dict(config['objective'])
    for k, v in objective_weights.items():
        objective_weights[k] = float(v)

    if not config.getboolean('constraints', 'CSP'):
        objective_weights['color_changeover'] = 0
        solver.engine.create_objective(objective_weights)

    return solver

def main(argv) -> None:
    solver = create_solver()

    solver_conf = dict(solver.config['solver'])
    for k, v in solver_conf.items():
        solver_conf[k] = int(v)
    result = solver.engine.run(config=solver_conf)

    times = 1
    objective_weights = dict(solver.config['objective'])
    for k, v in objective_weights.items():
        objective_weights[k] = float(v)
    for i in range(times):
        if not solver.config.getboolean('constraints', 'CSP'):
            solver.engine.create_objective(objective_weights)

        result = solver.engine.run(
            history=result, config=solver_conf
        )

    solver.display_result()


if __name__ == '__main__':
    app.run(main)
