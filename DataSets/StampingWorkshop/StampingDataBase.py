"""
   1. dict <-> "dataframe" <-> json <-> CSV <-> "db"
   2. docs
"""

from absl import app
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from StampingData import *

import sys, os
path = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(os.path.dirname(path)))
from Interface.IDataBase import *

filename = os.path.join(path, "stamping_workshop.db")

def main(argv) -> None:
    engine = create_engine(f'sqlite:///{filename}?charset=utf8')
    reg.metadata.drop_all(engine)
    reg.metadata.create_all(engine)

    with Session(engine) as session:
        for t in timeUnits:
            session.add(
                TimeUnit(
                    date_time=t['datetime'],
                    used=t['used']
                )
            )
        session.commit()

    with Session(engine) as session:
        for line in productLine:
            session.add(
                WorkCenterOrg_Line(
                    name=line['name'],
                    code=str(line['code'])
                )
            )
        session.commit()

    with Session(engine) as session:
        for d in SNP:           # 容器信息
            session.add(
                Property_1(
                    name=d['name'],
                    value=d['value']
                )
            )
        session.commit()

    with Session(engine) as session:
        for d in inventory_limit:  # 库存上限
            session.add(
                Property_2(
                    name=d['name'],
                    value=d['value']
                )
            )
        session.commit()

    with Session(engine) as session:
        for d in productionData:  # 录入零件信息
            session.add(
                Production(
                    name=d['name'],
                    code=d['code'],
                    prop_1=d['SNP'],
                    prop_2=d['prop_id']
                )
            )
        session.commit()

    with Session(engine) as session:
        count = 1
        for d in workcenterCraftRoute:  # 录入加工信息/工艺路径
            session.add(
                WorkCenterCraftRoute(
                    name=d['name'],
                    code=str(d['code']),
                    OEE=d['OEE'],
                    description=d['description']
                )
            )
            session.add(
                CraftRouteItem(
                    craft=count,
                    line=d['line']
                )
            )
            count += 1
        session.commit()

    with Session(engine) as session:
        for d in processItem:   # 录入零件与工艺路径的对应关系
            session.add(
                ProcessItem(
                    prod=d['prod'],
                    craft=d['craft'],
                    productivity=d['productivity'],
                    processing_time=(60./d['pt']),  # seconds
                    sync=d['sync']
                )
            )
        session.commit()

    with Session(engine) as session:
        for d in orderInfo:
            session.add(
                OrderInformation(
                    description=d['desc'],
                    priority=d['priority'],
                    code=str(d['code'])
                )
            )
        session.commit()

    with Session(engine) as session:
        for d in orderItem:
            session.add(
                OrderItem(
                    production=d['prod'],
                    information=d['info'],
                    delivery_time=d['dt'],
                    number=d['number']
                )
            )
        session.commit()

    with Session(engine) as session:
        for d in materialData:
            session.add(
                Material(
                    name=d['name'],
                    code=d['code']
                )
            )
        session.commit()

    with Session(engine) as session:
        for d in ingredient:
            session.add(
                Ingredient(
                    production=d['production'],
                    material=d['material'],
                    number=d['number']
                )
            )
        session.commit()

    with Session(engine) as session:
        for d in kittingInformation:
            session.add(
                KittingInformation(
                    time_unit=d['time_unit'],
                    material=d['material'],
                    number=d['number']
                )
            )
        session.commit()


def test(argv) -> None:
    engine = create_engine(f'sqlite:///{filename}?charset=utf8')
    reg.metadata.drop_all(engine)
    reg.metadata.create_all(engine)

    with Session(engine) as session:
        for d in prod_data:
            session.add(
                Production(name=d[3], code=d[4])
            )
        session.commit()

        for d in mold_data:
            session.add(
                WorkCenterCraftRoute(name=d[0], code=d[1])
            )
        session.commit()

        for d in process_data:
            prod_id = session.execute(
                select(Production.id).filter_by(code=d[1])
            ).scalar_one()

            craft_id = session.execute(
                select(WorkCenterCraftRoute.id).filter_by(code=d[0])
            ).scalar_one()

            session.add(
                ProcessItem(prod=prod_id, craft=craft_id)
            )
        session.commit()

def example() -> None:
    # prod = session.query(Production)
    # for p in prod:
    #     print(p)

    # session.get(Production, 4)

    # ret = session.execute(
    #     select(Production).filter_by(code="...")
    # ).scalar_one()

    # session.execute(
    #     select(User).where(User.name == "patrick")
    # ).first()

    # select(Address.email_address).select_from(User).join(
    #     User.addresses)

    # for user_obj in session.execute(
    #         select(User).options(selectinload(User.addresses))
    # ).scalars():
    #     # access addresses collection already loaded
    #     user_obj.addresses

    return


if __name__ == '__main__':
    app.run(main)
