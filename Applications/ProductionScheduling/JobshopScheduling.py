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


class JobshopSchedulingSolver:
    """ 当前状态: 模型已完成，应用待实现
        纯Jobshop场景对APS的需求不高，实现的价值低
        研发暂时搁置!
    """

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

    def setup(self) -> None:
        pass


def main(argv) -> None:
    import pathlib

    folder = pathlib.Path(__file__).parent.resolve()
    path = f'{folder.parent.parent}/DataSets/Jobshop'

    base_data = pd.read_csv(f'{path}/BaseDataS.csv')
    order = pd.read_csv(f'{path}/OrderData.csv')

    from pandasgui import show
    show(base_data, order)

if __name__ == '__main__':
    app.run(main)
