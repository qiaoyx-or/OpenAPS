import pandas as pd
import numpy as np

test_data = pd.DataFrame({
    '1':  {'code': 1, 'tt': 1, 'type': 5, 'color': 1, 'craft': 1, 'cat': 2, 'number': 24, 'pri': 2},
    '2':  {'code': 2, 'tt': 1, 'type': 7, 'color': 2, 'craft': 1, 'cat': 3, 'number': 53, 'pri': 1},
    '3':  {'code': 3, 'tt': 2, 'type': 6, 'color': 2, 'craft': 1, 'cat': 2, 'number': 25, 'pri': 1},
    '4':  {'code': 4, 'tt': 2, 'type': 6, 'color': 1, 'craft': 2, 'cat': 2, 'number': 22, 'pri': 2},
    '5':  {'code': 5, 'tt': 2, 'type': 8, 'color': 4, 'craft': 2, 'cat': 3, 'number': 21, 'pri': 2},
    '6':  {'code': 6, 'tt': 3, 'type': 9, 'color': 3, 'craft': 1, 'cat': 4, 'number': 23, 'pri': 2},
    '7':  {'code': 7, 'tt': 3, 'type': 9, 'color': 5, 'craft': 1, 'cat': 4, 'number': 32, 'pri': 2},
    '8':  {'code': 7, 'tt': 3, 'type': 9, 'color': 5, 'craft': 2, 'cat': 2, 'number': 24, 'pri': 2},
    '9':  {'code': 6, 'tt': 3, 'type': 8, 'color': 4, 'craft': 2, 'cat': 3, 'number': 53, 'pri': 1},
    '10': {'code': 5, 'tt': 3, 'type': 8, 'color': 4, 'craft': 1, 'cat': 2, 'number': 25, 'pri': 1},
    '11': {'code': 4, 'tt': 2, 'type': 7, 'color': 3, 'craft': 2, 'cat': 2, 'number': 22, 'pri': 2},
    '12': {'code': 3, 'tt': 2, 'type': 7, 'color': 2, 'craft': 2, 'cat': 3, 'number': 21, 'pri': 2},
    '13': {'code': 2, 'tt': 1, 'type': 6, 'color': 2, 'craft': 1, 'cat': 4, 'number': 23, 'pri': 2},
    '14': {'code': 1, 'tt': 1, 'type': 6, 'color': 1, 'craft': 1, 'cat': 4, 'number': 32, 'pri': 2}
}).T


class TestData(object):

    @staticmethod
    def get_data():
        return test_data

    @staticmethod
    def get_random_data(length: int=0):
        if length <= 0:
            return test_data

        props = TestData.get_property_names()
        data = [[] for i in range(length)]
        for r in range(length):
            data[r] = [
                np.random.randint(1, 5),     # code
                np.random.randint(1, 4),     # tt
                np.random.randint(1, 8),     # type
                np.random.randint(1, 6),     # color
                np.random.randint(1, 3),     # craft
                np.random.randint(1, 5),     # catelog
                np.random.randint(10, 100),  # number
                np.random.randint(1, 3),     # priority
            ]
        return pd.DataFrame(data, columns=props)

    @staticmethod
    def get_property_names():
        return list(test_data.columns)
