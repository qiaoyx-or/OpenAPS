import uuid
import datetime
import numpy as np
import pandas as pd
from absl import app
from IPython.display import display

filename = 'stamping_workshop.db'

# w.r.t WorkCenterOrg_1
ns = uuid.NAMESPACE_DNS
# 模拟产线信息
productLine = [
    {'name': 'Line A', 'code': uuid.uuid5(ns, 'Line A')},
    {'name': 'Line B', 'code': uuid.uuid5(ns, 'Line B')}
]

# 模拟工艺路径
workcenterCraftRoute = [
    {'name': '零件A', 'line': 1, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 1+1"},
    {'name': '零件B', 'line': 1, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 1+1"},
    {'name': '零件C1', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "单件加工"},
    {'name': '零件C2', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "单件加工"},
    {'name': '零件D1', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 1+1"},
    {'name': '零件E1', 'line': 1, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 1+1"},
    {'name': '零件D2', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 1+1"},
    {'name': '零件E2', 'line': 1, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 1+1"},
    {'name': '零件F', 'line': 1, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "单件加工"},
    {'name': '零件G', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "单件加工"},
    {'name': '零件H', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "单件加工"},
    {'name': '零件I1', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "单件加工"},
    {'name': '零件I2', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "单件加工"},
    {'name': '零件J', 'line': 1, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "单件加工"},
    {'name': '零件K1', 'line': 1, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 2+2"},
    {'name': '零件K2', 'line': 1, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 2+2"},
    {'name': '零件K3', 'line': 1, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 2+2"},
    {'name': '零件L1', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 1+1"},
    {'name': '零件L2', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 1+1"},
    {'name': '零件M1', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 1+1"},
    {'name': '零件M2', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 1+1"},
    # ----------------------------------------------------
    {'name': '零件C1', 'line': 1, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "单件加工"},
    {'name': '零件C2', 'line': 1, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "单件加工"},
    {'name': '零件J', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "单件加工"},
    {'name': '零件K1', 'line': 2, 'OEE': np.random.randint(40, 100),
     'code': uuid.uuid4(), 'description': "并行加工，模式: 2+2"}
]

# 模拟扩展属性
propertyCat = [
    {'name': 'common',  'code': uuid.uuid5(ns, 'common')},
    {'name': 'Type_1',  'code': uuid.uuid5(ns, 'Type_1')},
    {'name': 'Type_2', 'code': uuid.uuid5(ns, 'Type_2')},
    {'name': 'Type_3',   'code': uuid.uuid5(ns, 'Type_3')}
]

# 模拟容器共用策略
inventory_limit = [
    {'name': 'container 1',  'value': 48},
    {'name': 'container 2',  'value': 26},
    {'name': 'container 3',  'value': 48},
    {'name': 'container 4',  'value': 48},
    {'name': 'container 5',  'value': 20},
    {'name': 'container 6',  'value': 56},
    {'name': 'container 7',  'value': 26},
    {'name': 'container 8',  'value': 34},
    {'name': 'container 9',  'value': 34},
    {'name': 'container 10', 'value': 34},
    {'name': 'container 11', 'value': 34},
    {'name': 'container 12', 'value': 48},
    {'name': 'container 13', 'value': 48},
    {'name': 'container 14', 'value': 48},
    {'name': 'container 15', 'value': 48},
    {'name': 'container 16', 'value': 98},
    {'name': 'container 17', 'value': 184},
    {'name': 'container 18', 'value': 98},
    {'name': 'container 19', 'value': 62},
    {'name': 'container 20', 'value': 26},
    {'name': 'container 21', 'value': 26},
    {'name': 'container 22', 'value': 44},
    {'name': 'container 23', 'value': 78}
]

# 模拟容器容量
SNP = [
    {'name': 'SNP', 'value': 30},
    {'name': 'SNP', 'value': 60},
    {'name': 'SNP', 'value': 30},
    {'name': 'SNP', 'value': 30},
    {'name': 'SNP', 'value': 80},
    {'name': 'SNP', 'value': 25},
    {'name': 'SNP', 'value': 50},
    {'name': 'SNP', 'value': 60},
    {'name': 'SNP', 'value': 60},
    {'name': 'SNP', 'value': 60},
    {'name': 'SNP', 'value': 60},
    {'name': 'SNP', 'value': 28},
    {'name': 'SNP', 'value': 28},
    {'name': 'SNP', 'value': 28},
    {'name': 'SNP', 'value': 28},
    {'name': 'SNP', 'value': 14},
    {'name': 'SNP', 'value': 15},
    {'name': 'SNP', 'value': 15},
    {'name': 'SNP', 'value': 14},
    {'name': 'SNP', 'value': 14},
    {'name': 'SNP', 'value': 30},
    {'name': 'SNP', 'value': 30},
    {'name': 'SNP', 'value': 100},
    {'name': 'SNP', 'value': 100},
    {'name': 'SNP', 'value': 100},
    {'name': 'SNP', 'value': 100},
    {'name': 'SNP', 'value': 100},
    {'name': 'SNP', 'value': 100},
    {'name': 'SNP', 'value': 55},
    {'name': 'SNP', 'value': 55},
    {'name': 'SNP', 'value': 30},
    {'name': 'SNP', 'value': 30},
]

# 模拟物料信息
materialData = [
    {'code': 'X00011228', 'name': '物料C2.1'},
    {'code': 'X00011229', 'name': '物料C2.2'},
    {'code': 'X00011233', 'name': '物料E2'},
    {'code': 'X00011234', 'name': '物料D2'},
    {'code': 'X00011220', 'name': '物料J'},
    {'code': 'X00011223', 'name': '物料L'},
    {'code': 'X00011224', 'name': '物料M'},
    {'code': 'X00011227', 'name': '物料H+G'},
    {'code': 'X00011230', 'name': '物料C1'},
    {'code': 'X00011231', 'name': '物料K'},
    {'code': 'X00011219', 'name': '物料B2'},
    {'code': 'X00011225', 'name': '物料F'},
    {'code': 'X00011232', 'name': '物料E1.1'},
    {'code': 'X00011235', 'name': '物料D1.1'},
    {'code': 'X00011330', 'name': '物料B1'},
    {'code': 'X00011331', 'name': '物料I'},
    {'code': 'X00011332', 'name': '物料D1.2'},
    {'code': 'X00011333', 'name': '物料E1.2'},
    {'code': 'X00011221', 'name': '物料A1'},
    {'code': 'X00011222', 'name': '物料A2'}
]

# 模拟制品/零部件信息
productionData = [
    {'name': "零件A1", 'code': "1071533", 'cat': 1,
     'SNP': 1, 'limit': 48, 'prop_id': 1},
    {'name': "零件A2", 'code': "1071710", 'cat': 1,
     'SNP': 2, 'limit': 26, 'prop_id': 2},
    {'name': "零件B1", 'code': "1071927", 'cat': 1,
     'SNP': 3, 'limit': 48, 'prop_id': 3},
    {'name': "零件B2", 'code': "1071923", 'cat': 1,
     'SNP': 4, 'limit': 48, 'prop_id': 4},
    {'name': "零件C1", 'code': "1071817", 'cat': 1,
     'SNP': 5, 'limit': 20, 'prop_id': 5},
    {'name': "零件C2.1", 'code': "1071221", 'cat': 1,
     'SNP': 6, 'limit': 56, 'prop_id': 6},
    {'name': "零件C2.2", 'code': "1071694", 'cat': 1,
     'SNP': 7, 'limit': 26, 'prop_id': 7},
    {'name': "零件D1.1",   'code': "1071242", 'cat': 1,
     'SNP': 8, 'limit': 34, 'prop_id': 8},
    {'name': "零件D1.2",   'code': "1071364", 'cat': 1,
     'SNP': 9, 'limit': 34, 'prop_id': 9},
    {'name': "零件E1.1",   'code': "1071090", 'cat': 1,
     'SNP': 10, 'limit': 34, 'prop_id': 10},
    {'name': "零件E1.2",   'code': "1071092", 'cat': 1,
     'SNP': 11, 'limit': 34, 'prop_id': 11},
    {'name': "零件D2.1",   'code': "1071237", 'cat': 1,
     'SNP': 12, 'limit': 48, 'prop_id': 12},
    {'name': "零件D2.2",   'code': "1071350", 'cat': 1,
     'SNP': 13, 'limit': 48, 'prop_id': 13},
    {'name': "零件E2.1",   'code': "1071098", 'cat': 1,
     'SNP': 14, 'limit': 48, 'prop_id': 14},
    {'name': "零件E2.2",   'code': "1071100", 'cat': 1,
     'SNP': 15, 'limit': 48, 'prop_id': 15},
    {'name': "零件F",   'code': "1072114", 'cat': 1,
     'SNP': 16, 'limit': 98, 'prop_id': 16},
    {'name': "零件H",     'code': "1072146", 'cat': 1,
     'SNP': 17, 'limit': 184, 'prop_id': 17},
    {'name': "零件G", 'code': "1073807", 'cat': 1,
     'SNP': 18, 'limit': 184, 'prop_id': 17},
    {'name': "零件I1",   'code': "1072116", 'cat': 2,
     'SNP': 19, 'limit': 98, 'prop_id': 18},
    {'name': "零件I2",   'code': "1146408", 'cat': 3,
     'SNP': 20, 'limit': 98, 'prop_id': 18},
    {'name': "零件J1",          'code': "1060962", 'cat': 2,
     'SNP': 21, 'limit': 62, 'prop_id': 19},
    {'name': "零件J2",   'code': "1155623", 'cat': 3,
     'SNP': 22, 'limit': 62, 'prop_id': 19},
    {'name': "零件K1.1",        'code': "1137608", 'cat': 2,
     'SNP': 23, 'limit': 26, 'prop_id': 20},
    {'name': "零件K1.2",        'code': "1158831", 'cat': 2,
     'SNP': 24, 'limit': 26, 'prop_id': 21},
    {'name': "零件K2.1", 'code': "1144139", 'cat': 3,
     'SNP': 25, 'limit': 26, 'prop_id': 20},
    {'name': "零件K2.2", 'code': "1173404", 'cat': 3,
     'SNP': 26, 'limit': 26, 'prop_id': 21},
    {'name': "零件K3.1",   'code': "1144140", 'cat': 4,
     'SNP': 27, 'limit': 26, 'prop_id': 20},
    {'name': "零件K3.2",   'code': "1161016", 'cat': 4,
     'SNP': 28, 'limit': 26, 'prop_id': 21},
    {'name': "零件L1",          'code': "1072649", 'cat': 2,
     'SNP': 29, 'limit': 44, 'prop_id': 22},
    {'name': "零件L2",   'code': "1102081", 'cat': 3,
     'SNP': 30, 'limit': 44, 'prop_id': 22},
    {'name': "零件M1",          'code': "1041020", 'cat': 1,
     'SNP': 31, 'limit': 78, 'prop_id': 23},
    {'name': "零件M2",     'code': "1128557", 'cat': 4,
     'SNP': 32, 'limit': 78, 'prop_id': 23}
]

# 配料表
ingredient = [
    {'material': 19, 'production': 1,  'number': 1},
    {'material': 20, 'production': 2,  'number': 1},
    {'material': 15, 'production': 3,  'number': 1},
    {'material': 11, 'production': 4,  'number': 1},
    {'material': 9,  'production': 5,  'number': 1},
    {'material': 1,  'production': 6,  'number': 1},
    {'material': 2,  'production': 7,  'number': 1},
    {'material': 14, 'production': 8,  'number': 1},
    {'material': 17, 'production': 9,  'number': 1},
    {'material': 13, 'production': 10, 'number': 1},
    {'material': 18, 'production': 11, 'number': 1},
    {'material': 4,  'production': 12, 'number': 1},
    {'material': 4,  'production': 13, 'number': 1},
    {'material': 3,  'production': 14, 'number': 1},
    {'material': 3,  'production': 15, 'number': 1},
    {'material': 12, 'production': 16, 'number': 1},
    {'material': 8,  'production': 17, 'number': 1},
    {'material': 8,  'production': 18, 'number': 1},
    {'material': 16, 'production': 19, 'number': 1},
    {'material': 16, 'production': 20, 'number': 1},
    {'material': 5,  'production': 21, 'number': 1},
    {'material': 5,  'production': 22, 'number': 1},
    {'material': 10, 'production': 23, 'number': 1},
    {'material': 10, 'production': 24, 'number': 1},
    {'material': 10, 'production': 25, 'number': 1},
    {'material': 10, 'production': 26, 'number': 1},
    {'material': 10, 'production': 27, 'number': 1},
    {'material': 10, 'production': 28, 'number': 1},
    {'material': 6,  'production': 29, 'number': 1},
    {'material': 6,  'production': 30, 'number': 1},
    {'material': 7,  'production': 31, 'number': 1},
    {'material': 7,  'production': 32, 'number': 1}
]

# 模拟加工信息
processItem = [
    {'craft': 1,  'prod': 1 , 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 1},
    {'craft': 1,  'prod': 2 , 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 1},
    {'craft': 2,  'prod': 3 , 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 2},
    {'craft': 2,  'prod': 4 , 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 2},
    {'craft': 3,  'prod': 5 , 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 2},
    {'craft': 4,  'prod': 6 , 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 4},
    {'craft': 4,  'prod': 7 , 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 4},
    {'craft': 5,  'prod': 8 , 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 5},
    {'craft': 5,  'prod': 9 , 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 5},
    {'craft': 6,  'prod': 10, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 6},
    {'craft': 6,  'prod': 11, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 6},
    {'craft': 7,  'prod': 12, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 7},
    {'craft': 7,  'prod': 13, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 7},
    {'craft': 8,  'prod': 14, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 8},
    {'craft': 8,  'prod': 15, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 8},
    {'craft': 9,  'prod': 16, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 9},
    {'craft': 10, 'prod': 17, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 10},
    {'craft': 11, 'prod': 18, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 11},
    {'craft': 12, 'prod': 19, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 12},
    {'craft': 13, 'prod': 20, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 13},
    {'craft': 14, 'prod': 21, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 14},
    {'craft': 14, 'prod': 22, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 14},
    {'craft': 15, 'prod': 23, 'productivity': 2, 'pt': np.random.randint(30, 100), 'sync': 15},
    {'craft': 15, 'prod': 24, 'productivity': 2, 'pt': np.random.randint(30, 100), 'sync': 15},
    {'craft': 16, 'prod': 25, 'productivity': 2, 'pt': np.random.randint(30, 100), 'sync': 16},
    {'craft': 16, 'prod': 26, 'productivity': 2, 'pt': np.random.randint(30, 100), 'sync': 16},
    {'craft': 17, 'prod': 27, 'productivity': 2, 'pt': np.random.randint(30, 100), 'sync': 17},
    {'craft': 17, 'prod': 28, 'productivity': 2, 'pt': np.random.randint(30, 100), 'sync': 17},
    {'craft': 18, 'prod': 29, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 18},
    {'craft': 19, 'prod': 30, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 19},
    {'craft': 20, 'prod': 31, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 20},
    {'craft': 21, 'prod': 32, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 21},
    # --------------------------------------
    # {'craft': 22,  'prod': 5 , 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 2},
    {'craft': 23,  'prod': 6 , 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 4},
    {'craft': 23,  'prod': 7 , 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 4},
    {'craft': 24, 'prod': 21, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 14},
    {'craft': 24, 'prod': 22, 'productivity': 1, 'pt': np.random.randint(30, 100), 'sync': 14},
    {'craft': 25, 'prod': 23, 'productivity': 2, 'pt': np.random.randint(30, 100), 'sync': 15},
    {'craft': 25, 'prod': 24, 'productivity': 2, 'pt': np.random.randint(30, 100), 'sync': 15}
]

# 模拟BOM信息
bom_finished_A = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 19, 21, 23, 24, 29, 31
]
bom_finished_B = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 20, 22, 25, 26, 30, 31
]
bom_finished_C = [
    1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19, 21, 27, 28, 29, 32
]
bom = [bom_finished_A, bom_finished_B, bom_finished_C, bom_finished_C,
       bom_finished_B, bom_finished_C, bom_finished_B, bom_finished_C,
       bom_finished_C, bom_finished_C, bom_finished_C, bom_finished_C]

# 模拟订单信息
orderInfo = [
    {'desc': '备件',
     'code': uuid.uuid5(ns, '备件'),  'priority': 0},
    {'desc': '客户A',
     'code': uuid.uuid5(ns, '客户A'), 'priority': 1},
    {'desc': '客户B',
     'code': uuid.uuid5(ns, '客户B'), 'priority': 3},
    {'desc': '代工A',
     'code': uuid.uuid5(ns, '代工A'), 'priority': 2},
    {'desc': '客户C',
     'code': uuid.uuid5(ns, '客户C'), 'priority': 1},
    {'desc': '客户D',
     'code': uuid.uuid5(ns, '客户D'), 'priority': 3},
    {'desc': '代工B',
     'code': uuid.uuid5(ns, '代工B'), 'priority': 2},
    {'desc': '安全库存',
     'code': uuid.uuid5(ns, '安全库存'), 'priority': 0}
]

def gen_time():
    t = datetime.date.today()
    return [
        {
            'datetime': t + datetime.timedelta(days=i),
            'used': np.random.randint(0, 30) / 100.
        }  for i in range(25)
    ]

timeUnits = gen_time()

# 模拟订单内容信息
orderItem = [
    # {'info': , 'prod': , 'number': , 'dt': },
]

# 模拟齐套信息
kittingInformation = [
    # {'time_unit': , 'meterial': , 'number': }
]

for info in range(len(orderInfo)):
    # 默认出件率为1或2, 为构造满足出件率的数据，2的倍数
    num = 2*np.random.randint(100, 500)

    for i in range(10):
        # 随机选取bom，用于生成订单信息
        j = np.random.randint(1, len(bom))

        # 随机生成订单交期
        m = len(timeUnits) - 1 - 2
        t = timeUnits[np.random.randint(1, m)]['datetime']

        for item in bom[j-1]:   # 将成品订单拆解为制品/零部件订单
            orderItem.append(
                {'info': info+1, 'prod': item, 'number': num, 'dt':t}
            )

for i in range(len(materialData)):
    candidates = [0, 1000, 2000, 5000, 10000]

    sup = len(candidates)-1
    n = candidates[np.random.randint(0, sup)]
    kittingInformation.append(
        {
            'time_unit': 1,
            'material': i+1,
            'number': 20000 + n
        }
    )

    for t in range(len(timeUnits)):
        if t == 0:
            continue
        n = candidates[np.random.randint(0, sup)]
        kittingInformation.append(
            {'time_unit': t+1, 'material': i+1, 'number': n}
        )

def main(argv) -> None:
    print(pd.DataFrame(timeUnits))
    print(pd.DataFrame(kittingInformation))

if __name__ == '__main__':
    app.run(main)
