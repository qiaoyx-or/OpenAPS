from absl import app

import pandas as pd
import numpy as np
import json

from pathlib import Path
import sys, os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)

from Interface.Interface import *
from Interface.ExportSqliteData import *
import OptimizationCalculusKernel as gock


class WorkshopSolver:
    def __init__(self) -> None:
        pass

    def create_calendar(self, units) -> None:
        self.calendar = TimeLine([   # 模拟生产日历
            TimeLineUnit(
                int(units.iloc[i].id),
                int(units.iloc[i].scale),
                int(units.iloc[i].status),
                float(units.iloc[i].used),
                units.iloc[i].date_time,
                int(units.iloc[i].id * units.iloc[i].scale)
            ) for i in range(units.shape[0])
        ])

    def create_engine(
            self, order, craft
    ) -> None:
        process = Preprocessing(
            IDemandTimed(
                order, self.calendar,
                ['production'], 'production', 'number'),
            craft,
            ['line']            # 此处传入'line'，表示产能是以产线进行组织的
        )
        process.demand.fixed_batch_size = process.demand.snps() * 2**0
        process.demand.supplements += process.check_fixed_batch_size()
        process.demand.supplements += process.check_sync()

        self.engine = gock.NormalWorkshopEngine(
            process.demand,
            process.get_capacity_list(self.calendar)
        )

    def create_kitting_condition(
            self,
            material, ingredient, kitting,
    ) -> None:
        matA, matB = KittingProcess.to_kitting_condition(
            ingredient, kitting,
            self.calendar,
            self.engine.demand.production_ids,
            list(material.id)
        )

        self.engine.create_kitting_constraints(matA, matB)

    def store_result(self, file: str, result) -> None:
        records = self.engine.get_result(result)
        if len(records) == 0:
            return

        with Session(
                create_engine(f'sqlite:///{file}?charset=utf8')
        ) as session:
            session.query(PlanningResult).delete()
            # session.execute("TRUNCATE TABLE planning_result")
            for record in records:
                session.add(record)
            session.commit()

    def run(self):
        print('--------------------------------------------------')
        self.engine.run()
        data = self.engine.business.data.get_result(
            self.engine.business.scene.code
        )

        if data is not None:
            return pd.DataFrame(
                data.astype(int),
                columns=self.engine.business.scene.form.codes
            )

        return None

    def display_result(self, *, mode: int=0) -> None:
        data = self.engine.business.data.get_result(
            self.engine.business.scene.code
        )

        dfs = {}
        if data is not None:
            df = pd.DataFrame(
                data.astype(int),
                columns=self.engine.business.scene.form.codes
            )

            if mode == 0:
                self.display_with_style(df)
            else:
                dfs['workshop'] = df

        for wc in self.engine.business.scene.workcenters:
            data = self.engine.business.data.get_result(wc.code).astype(int)
            factor = self.engine.business.data.factor[wc.code]

            df = pd.DataFrame(data.astype(int), columns=wc.form.codes)
            df['idletime'] = factor['idletime'].astype(int) // 60
            df['workload'] = factor['workload'].astype(int) // 60

            if data is not None:
                if mode == 0:
                    self.display_with_style(df)
                else:
                    dfs[f'workcenter {wc.code}'] = df

        if mode == 1:
            from pandasgui import show
            show(**dfs)

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


def read_config(file: str='conf.ini') -> dict:
    from configparser import ConfigParser

    cfg = ConfigParser()
    cfg.read(file)
    return dict(cfg.items())

def get_solver() -> WorkshopSolver:
    import pathlib

    solver = WorkshopSolver()

    folder = pathlib.Path(__file__).parent.resolve()
    config = read_config(f'{folder}/conf.ini')
    database = f'{folder}/{config['dbfile']['file']}'

    units, order, craft = import_base_data(database)
    records = import_planning_result(database)
    material, ingredient, kitting = import_kitting_information(database)

    solver.create_calendar(units)
    solver.create_engine(order, craft)

    solver.engine.setup()
    solver.engine.create_capacity_constraints()
    solver.engine.create_demand_constraints(mode=3)
    solver.engine.create_inventory_constraints()
    solver.create_kitting_condition(material, ingredient, kitting)

    return solver

def main(argv) -> None:
    solver = WorkshopSolver()

    config = read_config('conf.ini')
    database = config['dbfile']['file']

    units, order, craft = import_base_data(database)
    records = import_planning_result(database)
    material, ingredient, kitting = import_kitting_information(database)

    solver.create_calendar(units)
    solver.create_engine(order, craft)

    solver.engine.setup()
    solver.engine.create_capacity_constraints()
    solver.engine.create_demand_constraints(mode=3)
    solver.engine.create_inventory_constraints()
    solver.create_kitting_condition(material, ingredient, kitting)

    # 目标函数中的各权重为配置项
    solver.engine.create_objective(
        {
            'workload': -0,     # -号表示 maximize -> minimize 转换
            'idletime':  0,
            'job_bias': -1e-3,  # -0
            'waittime':  0
        }
    )

    result = solver.engine.run(config=dict(config['solver']))

    times = 1
    solver.engine.create_objective(
        {
            'workload': -0,     # -号表示 maximize -> minimize 转换
            'idletime':  0,
            'job_bias': -1e-3,  # -0
            'waittime':  1
        }
    )
    for i in range(times):
        result = solver.engine.run(
            history=result,
            config=dict(config['solver'])
        )

    solver.display_result(mode=1)


if __name__ == '__main__':
    app.run(main)
