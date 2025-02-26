from absl import app

import pandas as pd
import sys, os
sys.path.append(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)

from Interface.Interface import (
    TimeLineUnit, TimeLine,
    # IDemand,
    # IDemandFixed,
    IDemandTimed,
    # ICapacity,
    KittingProcess,
    Preprocessing
)
from Interface.ImportSqliteData import (
    import_base_data,
    import_kitting_information,
)
import OptimizationCalculusKernel as GOCK


class WorkshopSolver:
    def __init__(self, config=None) -> None:
        self.config = config

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
                order, self.calendar, ['production'],
                'production',
                'number'
            ),
            craft
        )
        process.demand.fixed_batch_size = process.demand.snps() * 2**0
        process.demand.supplements += process.check_fixed_batch_size()
        process.demand.supplements += process.check_sync()

        self.engine = GOCK.NormalWorkshopEngine(
            process.demand,
            process.get_capacity_list(self.calendar)
        )

    def export_csv(self) -> None:
        import pathlib
        from sqlalchemy import create_engine
        from sqlalchemy.orm import Session
        from Interface.IDataBase import Production

        folder = pathlib.Path(__file__).parent.resolve()
        dbfile = f'{folder}/{self.config['dbfile']['file']}'

        names = {}
        with Session(
                create_engine(f'sqlite:///{dbfile}?charset=utf8')
        ) as session:
            Productions = pd.DataFrame(session.query(Production))
            session.commit()
            for _, row in Productions.iterrows():
                names[row['id']] = row['name']

        business = self.engine.business
        columns = {}
        codes = business.scene.form.codes
        columns[0] = [names[c] for c in codes]
        for wc in business.scene.workcenters:
            codes = wc.form.codes
            columns[wc.code] = [names[c] for c in codes]

        folder = pathlib.Path(__file__).parent.resolve()

        indexes = [f'第{i+1}班' for i in range(
            self.engine.demand.calendar.length()
        )]
        df = pd.DataFrame(
            self.engine.demand.quantity,
            # index=indexes,
            columns=[names[i] for i in self.engine.demand.production_ids]
        )
        df.loc[len(df.index)]=self.engine.demand.quantity_acc[-1,:]
        indexes.append('合计')
        df.index=indexes
        df.to_csv(f'{folder}/demand.csv')

        for k, v in business.data.result.items():
            indexes = [f'第{i+1}班' for i in range(v.shape[0])]
            df = pd.DataFrame(v, index=indexes, columns=columns[k])
            df.to_csv(f'{folder}/workcenter_{k}.csv')

    def store_result(self, file: str, result) -> None:
        records = self.engine.get_result(result)
        if len(records) == 0:
            return

        from sqlalchemy.orm import Session
        from sqlalchemy import create_engine
        from IDataBase import PlanningResult
        with Session(
                create_engine(f'sqlite:///{file}?charset=utf8')
        ) as session:
            session.query(PlanningResult).delete()
            # session.execute("TRUNCATE TABLE planning_result")
            for record in records:
                session.add(record)
            session.commit()

    def run(self) -> None:
        solver_conf = dict(self.config['solver'])
        for k, v in solver_conf.items():
            solver_conf[k] = int(v)
        self.engine.run(config=solver_conf)

        pd.DataFrame(self.engine.business.data.demand).to_csv('demand.csv')
        for k, v in self.engine.business.data.result.items():
            pd.DataFrame(v).to_csv(f'workcenter_{k}.csv')

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
    cfg.read(file, encoding='utf-8')
    return cfg

def create_solver() -> WorkshopSolver:
    import pathlib

    folder = pathlib.Path(__file__).parent.resolve()
    config = read_config(f'{folder}/conf.ini')
    solver = WorkshopSolver(config)
    database = f'{folder}/{config['dbfile']['file']}'

    objective_weights = dict(config['objective'])
    for k, v in objective_weights.items():
        objective_weights[k] = float(v)

    units, order, craft = import_base_data(database)
    # records = import_planning_result(database)
    material, ingredient, kitting = import_kitting_information(database)

    # 必选项: 基础配置
    solver.create_calendar(units)
    solver.create_engine(order, craft)
    solver.engine.setup()
    matA, matB = KittingProcess.to_kitting_condition(
        ingredient, kitting, solver.calendar,
        solver.engine.demand.production_ids,
        list(material.id)
    )

    # 配置约束条件
    if config.getboolean('constraints', 'enable_capacity_cons'):
        solver.engine.create_capacity_constraints()

    if config.getboolean('constraints', 'enable_demand_cons'):
        m = config.getint('constraints', 'demand_cons_mode')
        if m is None:
            solver.engine.create_demand_constraints()
        else:
            mode = int(m)       # 数值类型必须显式转换
            solver.engine.create_demand_constraints(mode=mode)

    if config.getboolean('constraints', 'enable_inventory_cons'):
        solver.engine.create_inventory_constraints()

    if config.getboolean('constraints', 'enable_kitting_cons'):
        solver.engine.create_kitting_constraints(matA, matB)

    # 配置目标函数
    if not config.getboolean('constraints', 'CSP'):
        objective_weights['waittime'] = 0
        solver.engine.create_objective(objective_weights)

    return solver

def main(argv) -> None:
    solver = create_solver()

    solver_conf = dict(solver.config['solver'])
    for k, v in solver_conf.items():
        solver_conf[k] = int(v)
    result = solver.engine.run(config=solver_conf)
    solver.export_csv()

    times = 1
    objective_weights = dict(solver.config['objective'])
    for k, v in objective_weights.items():
        objective_weights[k] = float(v)
    for i in range(times):      # 热启动连续解算
        if not solver.config.getboolean('constraints', 'CSP'):
            solver.engine.create_objective(objective_weights)

        result = solver.engine.run(
            history=result, config=solver_conf
        )

    solver.export_csv()
    # solver.display_result(mode=1)


if __name__ == '__main__':
    app.run(main)
