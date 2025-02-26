import pandas as pd

# from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
# from sqlalchemy.schema import CreateSchema

import sys, os
sys.path.append(
    os.path.dirname(os.path.abspath(__file__))
)
from IDataBase import (
    PlanningResult,
    Material,
    Ingredient,
    KittingInformation,
    Calendar,
    WorkCenterOrgNode,
    Property_1,
    Property_2,
    Production,
    ProcessRoute,
    ProcessRouteItem,
    ProcessItem,
    OrderInformation,
    OrderItem
)


def import_planning_result(
        dbfile
) -> pd.DataFrame:
    engine = create_engine(f'sqlite:///{dbfile}?charset=utf8')
    session = Session(engine)
    return session.query(PlanningResult).all()


def import_kitting_information(
        dbfile
) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    with Session(           # get data from database file
            create_engine(f'sqlite:///{dbfile}?charset=utf8')
    ) as session:
        material = pd.DataFrame(session.query(Material))
        ingredient = pd.DataFrame(session.query(Ingredient))
        kitting = pd.DataFrame(session.query(KittingInformation))
        session.commit()

    return material, ingredient, kitting


def import_base_data(
        dbfile
) -> (pd.DataFrame, pd.DataFrame, pd.DataFrame):
    with Session(           # get data from database file
            create_engine(f'sqlite:///{dbfile}?charset=utf8')
    ) as session:
        # 生产日历
        calendar = pd.DataFrame(session.query(Calendar))

        # 产线信息，生产序列生成的地方(生产序列的坐标系)
        workcenters = pd.DataFrame(session.query(WorkCenterOrgNode))

        # 容器容量
        container_sizes = pd.DataFrame(session.query(Property_1))

        # 库存容量
        container_limits = pd.DataFrame(session.query(Property_2))

        # 制品信息
        prods = pd.DataFrame(session.query(Production))

        # 工艺路径基本信息
        processes = pd.DataFrame(session.query(ProcessRoute))

        # 工艺路径与设备或产线的对应关系(many2many)
        routes = pd.DataFrame(session.query(ProcessRouteItem))

        # 制品与工艺路径的对应关系(many2many)
        route_items = pd.DataFrame(session.query(ProcessItem))

        # 订单基本信息
        order_info = pd.DataFrame(session.query(OrderInformation))
        # 订单包含的制品信息(many2many)
        order_items = pd.DataFrame(session.query(OrderItem))

        # session.commit()

        order = pd.merge(
            order_items,
            order_info,
            how="inner",
            on=None,
            left_on="information",
            right_on="id",
            left_index=False,
            right_index=False,
            sort=False,
            suffixes=("_order_item", "_order_info"),
            copy=False,
            indicator=False,
            validate=None,
        )

        order = pd.merge(
            order,
            prods,
            how="inner",
            on=None,
            left_on="production",
            right_on="id",
            left_index=False,
            right_index=False,
            sort=False,
            suffixes=("", "_prod"),
            copy=False,
            indicator=False,
            validate=None,
        )

        order = pd.merge(
            order,
            container_sizes,
            how="inner",
            on=None,
            left_on="prop_1",
            right_on="id",
            left_index=False,
            right_index=False,
            sort=False,
            suffixes=("", "_prop_1"),
            copy=False,
            indicator=False,
            validate=None,
        )

        order = pd.merge(
            order,
            container_limits,
            how="inner",
            on=None,
            left_on="prop_2",
            right_on="id",
            left_index=False,
            right_index=False,
            sort=False,
            suffixes=("", "_prop_2"),
            copy=False,
            indicator=False,
            validate=None,
        )

        process = pd.merge(
            processes,
            routes,
            how="inner",
            on=None,
            left_on="id",
            right_on="process",
            left_index=False,
            right_index=False,
            sort=False,
            suffixes=("_process", "_route"),
            copy=False,
            # indicator=True,
            indicator=False,
            validate=None,
        )

        process = pd.merge(
            route_items,
            process,
            how="inner",
            on="process",
            # left_on="process",
            # right_on="id",
            left_index=False,
            right_index=False,
            sort=False,
            suffixes=("_route_item", ""),
            copy=False,
            # indicator=True,
                indicator=False,
            validate=None,
        )

        process = pd.merge(
            process,
            workcenters,
            how="inner",
            left_on="workcenter",
            right_on="id",
            left_index=False,
            right_index=False,
            sort=False,
            suffixes=("_route_item", ""),
            copy=False,
            # indicator=True,
                indicator=False,
            validate=None,
        )

    return calendar, order, process
