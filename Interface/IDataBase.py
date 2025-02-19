""" DataBase定义数据组织的结构，其目的：
    1. 各中场景的数据可以清晰的组织在一起
    2. 而不是用于定义实现逻辑
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import (
    # func,
    Identity,
    ForeignKey,
    Integer,
    # Float,
    # String,
    DateTime
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    registry,
    # relationship,
    # DeclarativeBase,
    # MappedAsDataclass
)


reg = registry()


@reg.mapped_as_dataclass(unsafe_hash=True)
class TimeUnit:
    """ 离散时间单元

    Attributes:
        id: 数据库表索引, 同时表示时间单元的顺序
        scale: e.g. 8*60*60 seconds
        status: in (-1, 0, 1), 1表示正常，0表示不可用，-1为特殊情形
        used: in [0, 1]

        date_time: [Optional] 用于记录绝对时间

    Notes:
        status 与 used功能有重叠, 为便于扩展保持这种重叠, 以status优先
        生产计划/作业计划(设备调度)与产能规划结合模式，status为-1(表示可选)不再需要
            这种情况下，status字段可以去掉. 同时，绑定了人参与决策的过程: 在常规时间内无法完成，如何增加产能
    """

    __tablename__ = "time_unit"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )
    scale: Mapped[int] = mapped_column(default=8*60*60)
    status: Mapped[int] = mapped_column(default=1)
    used: Mapped[float] = mapped_column(default=0.)

    date_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        default=None
    )


@reg.mapped_as_dataclass(unsafe_hash=True)
class Property_1:
    """ 预留属性字段
    Attributes:
        name: 扩展属性名称, 如: 颜色
        code: 扩展属性唯一编码, 如: 1 表示颜色
        value: 扩展属性值，如: 红色
    """
    __tablename__ = "property_1"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)
    value: Mapped[Optional[float]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class Property_2:
    """ 预留属性字段

    Attributes:
        name: 扩展属性名称, 如: 型号
        code: 扩展属性唯一编码, 如: 2 表示型号
        value: 扩展属性值，如: 型号A
    """
    __tablename__ = "property_2"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)
    value: Mapped[Optional[float]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class Property_3:
    """ 预留属性字段 """
    __tablename__ = "property_3"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)
    value: Mapped[Optional[float]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class Property_4:
    """ 预留属性字段 """
    __tablename__ = "property_4"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)
    value: Mapped[Optional[float]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class Property_5:
    """ 预留属性字段 """
    __tablename__ = "property_5"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)
    value: Mapped[Optional[float]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class Property_6:
    """ 预留属性字段 """
    __tablename__ = "property_6"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)
    value: Mapped[Optional[float]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class Property_7:
    """ 预留属性字段 """
    __tablename__ = "property_7"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)
    value: Mapped[Optional[float]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class Property_8:
    """ 预留属性字段 """
    __tablename__ = "property_8"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)
    value: Mapped[Optional[float]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class Property_9:
    """ 预留属性字段 """
    __tablename__ = "property_9"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)
    value: Mapped[Optional[float]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class Property_10:
    """ 预留属性字段 """
    __tablename__ = "property_10"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)
    value: Mapped[Optional[float]] = mapped_column(default=None)
    # 基于各属性构建的约束条件
    # constraints


@reg.mapped_as_dataclass(unsafe_hash=True)
class Production:
    """ 制品/零部件信息

    Attributes:
        id: 数据库表索引
        name: 制品/零部件名称
        code: 制品/零部件唯一编码
        vin:  所属成品的唯一编码
        prop_i: 扩展属性信息
    """

    __tablename__ = "production"

    # 数据记录的唯一标识
    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    # 制品名称
    name: Mapped[str] = mapped_column(nullable=False)
    # 制品/零部件的唯一编码
    code: Mapped[str] = mapped_column(nullable=True)
    # 所属成品的唯一编码，通常对应交付品(多个零部件经过组装形成)的编码
    vin:  Mapped[Optional[str]] = mapped_column(
        nullable=True,
        default=None
        # default=str(uuid.uuid4())
        # default_factory=uuid.uuid4
    )

    # 预留十个扩展字段，用于表示特殊属性
    prop_1: Mapped[Optional[int]] = mapped_column(
        ForeignKey("property_1.id"),
        default=None
    )
    prop_2: Mapped[Optional[int]] = mapped_column(
        ForeignKey("property_2.id"),
        default=None
    )
    prop_3: Mapped[Optional[int]] = mapped_column(
        ForeignKey("property_3.id"),
        default=None
    )
    prop_4: Mapped[Optional[int]] = mapped_column(
        ForeignKey("property_4.id"),
        default=None
    )
    prop_5: Mapped[Optional[int]] = mapped_column(
        ForeignKey("property_5.id"),
        default=None
    )
    prop_6: Mapped[Optional[int]] = mapped_column(
        ForeignKey("property_6.id"),
        default=None
    )
    prop_7: Mapped[Optional[int]] = mapped_column(
        ForeignKey("property_7.id"),
        default=None
    )
    prop_8: Mapped[Optional[int]] = mapped_column(
        ForeignKey("property_8.id"),
        default=None
    )
    prop_9: Mapped[Optional[int]] = mapped_column(
        ForeignKey("property_9.id"),
        default=None
    )
    prop_10: Mapped[Optional[int]] = mapped_column(
        ForeignKey("property_10.id"),
        default=None
    )

    def __eq__(self, other):
        assert type(other) is Production and other.code == self.code


@reg.mapped_as_dataclass(unsafe_hash=True)
class OrderInformation:
    """ 订单(头)信息

    Attributes:
        id: 数据库表索引
        description: 订单描述
        priority: (保证交付)优先级
        code: 订单的唯一编码[可选]
        create_at: 创建时间[可选]
    """

    __tablename__ = "order_info"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    description: Mapped[str] = mapped_column(nullable=True)
    priority: Mapped[int] = mapped_column(default=0)

    code: Mapped[Optional[str]] = mapped_column(default=None)
    created_at: Mapped[Optional[datetime]] = mapped_column(
        # insert_default=func.utc_timestamp(),
        default=None
    )


@reg.mapped_as_dataclass(unsafe_hash=True)
class OrderItem:
    """ 订单内容信息: 一个订单可包含多个订单条目

    Attributes:
        id: 数据库表索引
        production: 所属订单中包含的具体制品信息
        information: 所属订单
        delivery_time: 交付时间
        number: 交付数量
    """

    __tablename__ = "order_item"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    production: Mapped[int] = mapped_column(
        ForeignKey("production.id"),
        nullable=False
    )
    information: Mapped[int] = mapped_column(
        ForeignKey("order_info.id"),
        nullable=False
    )

    number: Mapped[int] = mapped_column(default=0)

    delivery_time: Mapped[Optional[datetime]] = mapped_column(
        DateTime,
        # insert_default=func.utc_timestamp(),
        default=None
    )


@reg.mapped_as_dataclass(unsafe_hash=True)
class WorkCenterDevice:
    """ 工作中心.设备 """

    __tablename__ = "workcenter_device"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[str] = mapped_column(nullable=True, default='')
    description: Mapped[str] = mapped_column(nullable=True, default='')

    # Overall Equipment Effectiveness
    OEE: Mapped[int] = mapped_column(nullable=False, default=100)

    # calendar: Mapped[List[int]]= mapped_column(
    #     nullable=False, default_factory=list
    # )


@reg.mapped_as_dataclass(unsafe_hash=True)
class WorkCenterCraftRoute:
    """ 工作中心.工艺路径
    """
    __tablename__ = "workcenter_craft_route"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[str] = mapped_column(nullable=True, default='')
    description: Mapped[str] = mapped_column(nullable=True, default='')

    # Overall Equipment Effectiveness
    OEE: Mapped[int] = mapped_column(nullable=False, default=100)

    # calendar: Mapped[List[int]]= mapped_column(
    #     nullable=False, default_factory=list
    # )


@reg.mapped_as_dataclass(unsafe_hash=True)
class CraftRouteItem:
    """ 工序: 由工艺、设备构成的关系. flowshop中通常不需要处理这一级, 多用于jobshop

    Attributes:
        id: 数据库表索引
        craft: 所属工艺路径
        device: 对应的设备(用于jobshop), 与line二选一，不同时生效
        line: 对应的产线(用于flowshop)
        seq_no: 表示该job在所属工艺路径中的工序
        buff: 对应缓存区的容量[可选]
    """
    __tablename__ = "craft_route_item"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    craft: Mapped[int] = mapped_column(
        ForeignKey("workcenter_craft_route.id")
    )
    device: Mapped[Optional[int]] = mapped_column(
        ForeignKey("workcenter_device.id"),
        default=None
    )
    line: Mapped[Optional[int]] = mapped_column(
        ForeignKey("workcenter_org_line.id"),
        default=None
    )

    # 工序数，表示工艺的第几个工序。相同工序数的多个加工表示无序列要求
    # Example: [1,2,3,3,3,4,5,6,6,7,8,...]
    seq_no: Mapped[int] = mapped_column(default=1)
    buff: Mapped[int] = mapped_column(default=0)


""" 默认5级组织结构： 集团 -> 工厂 -> 车间 -> 产线 -> 班组
"""
@reg.mapped_as_dataclass(unsafe_hash=True)
class WorkCenterOrg_Group:
    """ 产能组织结构.集团 """

    __tablename__ = "workcenter_org_group"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class WorkCenterOrg_Factory:
    """ 产能组织结构.工厂 """

    __tablename__ = "workcenter_org_factory"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[int]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class WorkCenterOrg_workshop:
    """ 产能组织结构.车间 """

    __tablename__ = "workcenter_org_workshop"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class WorkCenterOrg_Line:
    """ 产能组织结构.产线 """

    __tablename__ = "workcenter_org_line"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class WorkCenterOrg_Team:
    """ 产能组织结构.班组 """

    __tablename__ = "workcenter_org_team"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    name: Mapped[str] = mapped_column(nullable=False)
    code: Mapped[Optional[str]] = mapped_column(default=None)


@reg.mapped_as_dataclass(unsafe_hash=True)
class ProcessItem:
    """ 定义一个具体的加工(job): 什么production在那个craft(所包含的workcenters)上
        进行加工的基础信息

    Attributes:
        id: 数据库表索引
        prod: 该加工对应的制品信息
        craft: 该加工所属的工艺路径
        productivity: 一次加工的出件率，如: 一次冲压可以出多个零件
        processing_time: 一次加工需要花费的时间(秒)。生产节拍需要转化为加工时长
        sync: 并行加工标识。sync值相同的jobs，表示它们并行加工
    """
    __tablename__ = "process_item"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    prod: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("production.id")
    )
    craft: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("workcenter_craft_route.id")
    )

    # 单次加工的出件数量
    productivity: Mapped[int] = mapped_column(
        nullable=False,
        default=1
    )
    # 单次加工的时长，生产节拍需要转换为加工时长
    processing_time: Mapped[float] = mapped_column(
        nullable=False,
        default=0.0
    )

    # sync值相同，则并行加工
    sync: Mapped[int] = mapped_column(default=1)


@reg.mapped_as_dataclass(unsafe_hash=True)
class Material:
    """ 物料信息
    """

    __tablename__ = "material"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    code: Mapped[str] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(default='')


@reg.mapped_as_dataclass(unsafe_hash=True)
class Ingredient:
    """ 配料信息: Production 与 Material 的对应关系(many to many)

    Attributes:
        id: 数据库表索引
        production: 制品信息
        material: 制品所需的物料信息
        number: 该制品所需该物料的数量
    """

    __tablename__ = "ingredient"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    production: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("production.id")
    )
    material: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("material.id")
    )
    number: Mapped[int] = mapped_column(
        Integer, default=0
    )


@reg.mapped_as_dataclass(unsafe_hash=True)
class KittingInformation:
    """ 齐套信息: 在 time_unit 代表的时间, material 已备好的数量 number

    Attributes:
        id: 数据库表索引
    """

    __tablename__ = "kitting_information"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    time_unit: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("time_unit.id")
    )
    material: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("material.id")
    )

    number: Mapped[int] = mapped_column(
        Integer, default=0
    )


@reg.mapped_as_dataclass(unsafe_hash=True)
class LocalTimeUnit:
    """ 局部离散时间，如果与全局 TimeUnit 重叠，则使用局部覆盖全局数据

    Attributes:
        id: 数据库表索引

    """
    __tablename__ = "local_time_unit"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    time_unit: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("time_unit.id")
    )
    scale: Mapped[int] = mapped_column(default=8*60*60)
    status: Mapped[int] = mapped_column(default=1)
    used: Mapped[float] = mapped_column(default=0.)

    # 如果设备或产线的生产日历与全局生产日历不一致，则设置对应设备或产线的可用情况
    device: Mapped[Optional[int]] = mapped_column(
        ForeignKey("workcenter_device.id"),
        default=None
    )
    line: Mapped[Optional[int]] = mapped_column(
        ForeignKey("workcenter_org_line.id"),
        default=None
    )


@reg.mapped_as_dataclass(unsafe_hash=True)
class PlanningResult:
    """

    Attributes:
        id: 数据库表索引

    """
    __tablename__ = "planning_result"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    time_unit: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("time_unit.id")
    )
    production: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("production.id")
    )

    number: Mapped[int] = mapped_column(
        Integer, default=0
    )
    device: Mapped[Optional[int]] = mapped_column(
        ForeignKey("workcenter_device.id"),
        default=None
    )
    line: Mapped[Optional[int]] = mapped_column(
        ForeignKey("workcenter_org_line.id"),
        default=None
    )


@reg.mapped_as_dataclass(unsafe_hash=True)
class ConstraintBatch:
    __tablename__ = "constraint_batch"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )


@reg.mapped_as_dataclass(unsafe_hash=True)
class ConstraintChangeOver:
    """ 工序: 由工艺、设备构成的关系
        flowshop中通常不需要处理这一级
        多用于jobshop
    """
    __tablename__ = "constraint_change_over"

    id: Mapped[int] = mapped_column(
        Integer,
        Identity(),
        init=False,
        primary_key=True
    )

    curr: Mapped[int] = mapped_column(
        ForeignKey("craft_route_item.id")
    )
    next: Mapped[Optional[int]] = mapped_column(
        ForeignKey("craft_route_item.id")
    )

    change_time: Mapped[float] = mapped_column(default=0.0)
    cost: Mapped[float] = mapped_column(default=0.0)
