from absl import app

import pandas as pd
# from pandasgui import show

# base_data = r"/home/qiaoyx/workspace/DataSet/3.xls"
plan_18 = r"/home/qiaoyx/workspace/DataSet/20240918.xlsx"
plan_19 = r"/home/qiaoyx/workspace/DataSet/20240919.xlsx"

# base = pd.read_excel(base_data, sheet_name="Sheet")
base = pd.read_csv(r"/home/qiaoyx/workspace/DataSet/base.csv")
# p18 = pd.read_excel(plan_18, sheet_name="PP2白班")
# plan = pd.read_excel(plan_19, sheet_name="PP2白班")
# plan = pd.read_excel(plan_19, sheet_name="PP2晚班")[:-1]

# plan = pd.read_excel(plan_18, sheet_name="PP2白班")
plan = pd.read_excel(plan_19, sheet_name="PP2晚班")[:-1]
# plan = pd.read_excel(plan_19, sheet_name="PP2白班")
data = plan[plan['合计']>0][:-1]
_prod_code = data['物料编码']
prod_code = [  # 保持顺序去重
    x for i, x in enumerate(_prod_code)
    if x not in _prod_code[:i]
]

map19 = {prod_code[i]: i+1 for i in range(len(prod_code))}
typeidmap = {i+1: prod_code[i] for i in range(len(prod_code))}
namemap = {i+1: data[data['物料编码']==prod_code[i]]['产品名称'].values[0]
           for i in range(len(prod_code))}

obj = prod_code
selected = [
    base[base['Mcc零件号']==c] for c in obj
]

# 标签数为0表示什么？ 替换为1
# productivities = [
#     int(max(1, e['标签数量'].sum())) for e in selected
# ]
ppp = [
    e['挂载量'].dropna().values for e in selected
]
productivities = [
    int(e['标签数量'].sum()) for e in selected
]
for i in range(len(productivities)):
    if len(ppp[i]) != 0:
        productivities[i] = int(ppp[i][0])

capacities = [0 for e in selected]
syncs = [0 for e in selected]
sames = [0 for e in selected]

_cap = [e['载具数量'].dropna().values for e in selected]
_sync = [e['搭配'].dropna().values for e in selected]
_same = [e['挂架共用'].dropna().values for e in selected]

for i in range(len(obj)):
    if len(_cap[i]) != 0:
        capacities[i] = int(_cap[i][0])

    if len(_sync[i]) != 0:
        syncs[i] = int(_sync[i][0])

    if len(_same[i]) != 0:
        sames[i] = int(_same[i][0])

# print(
#     [list(data[data['物料编码']==e]['合计'].values) for e in obj]
# )

_production = list(map19.values())
# print(_production)

# 订单信息
_number = [int(data[data['物料编码']==e]['合计'].sum()) for e in obj]
# print(_number)

colors = [
    '马里亚纳灰', '铱泽银', '时光灰', '翠羽蓝', '纳银', '徽墨黑',
    '开瑞黄', '深夜蓝', '哈瓦那灰', '海岩灰', '新卡其白', '若草黄',
    '威尼斯蓝', '罗兰紫', '熔岩灰', '炫彩白', '金属红', '香草蓝',
    '血石红', '航空银', '苍穹蓝', '青竹灰', '翡翠绿', '水晶蓝',
    '极光绿', '底漆件', '海空蓝', '橄榄灰', '浮氧蓝', '太空银',
    '松林绿', '幻影灰', '蒂芙尼蓝', '高光纳银', '宝马蓝', '阳橙',
    '龙鳞灰', '绿色', '亚光银', '地中海蓝', '水绿', '碧海青',
    '科技蓝', '新碳晶黑', '科技灰', '松霜绿', '紫色', '哑光灰']
colormap = {colors[i]: i+1 for i in range(len(colors))}
coloridmap = {i+1: colors[i] for i in range(len(colors))}

# 统计颜色属性: 对应值非0的列的列序号，代表该表头所示的颜色
# print(data.columns)

_color = []
for idx, row in data.iterrows():
    for c in colors:
        if row[c] != 0:
            _color.append(colormap[c])

ids = list(map19.values())
_data = pd.DataFrame(
    {
        'id': ids,
        'type': _production,
        'color': _color,
        'number': _number,
        'productivity': productivities,
        'bias': [0 for i in ids],
        'capacity': capacities,
        'sync': syncs,
        'same': sames,
        'name': [namemap[i] for i in ids],
        'code': [typeidmap[i] for i in ids],
        'property_1': [colors[i] for i in _color]
    }
)

def get_data():
    return _data

def get_productivity():
    return productivities

def get_type_num():
    return len(obj)

def get_color_num():
    return len(list(set(_color)))

def get_color_map():
    return coloridmap

def get_type_map():
    return typeidmap

def get_name_map():
    return namemap

def get_capacities():
    return capacities

def get_syncs():
    return syncs

def get_sames():
    return sames

def get_capacity_from_production(prod_list):
    selected = [
        base[base['Mcc零件号']==c] for c in prod_list
    ]
    values = [s['挂架共用'].values for s in selected]
    cap_code = [0 for s in selected]
    for i in range(len(values)):
        if len(values[i]) != 0:
            cap_code[i] = values[i][0]
        else:
            cap_code[i] = 5555

    return cap_code

def get_production_from_capacity(df, cap_list):
    selected = [
        df[df['挂架共用']==c] for c in cap_list
    ]
    values = [list(s['Mcc零件号'].values) for s in selected]
    for i in range(len(values)):
        if len(values[i]) == 0:
            values[i] = ['EMPTY']

    return values

def main(argv) -> None:
    caps = get_capacity_from_production(obj)
    tmp = zip(obj, caps)
    print(list(tmp))

    prods = get_production_from_capacity(base, caps)
    print(prods)

if __name__ == '__main__':
    app.run(main)
