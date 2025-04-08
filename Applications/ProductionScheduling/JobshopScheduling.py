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

    # grouped = base_data.groupby('product', as_index=False)
    # processes = []
    # for g in grouped:
    #     process = g[1].sort_values(by='process', inplace=False)
    #     j = 1
    #     for i, row in process.iterrows():
    #         process.loc[i,'process'] = j
    #         j = j + 1

    #     processes.append(process)

    # new = pd.concat(processes)

    from pandasgui import show
    show(base_data, order)

if __name__ == '__main__':
    app.run(main)
