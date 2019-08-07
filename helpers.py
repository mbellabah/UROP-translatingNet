import pickle
from typing import Dict, List

import pandas as pd
import numpy as np


def scrape_nodes(save_pickle: bool = True) -> dict:
    df = pd.read_csv('csv_data/Buscoords.csv', names=['BUSNAME'], usecols=[0])
    df_indices = np.asarray(df.index.values) + 2
    df['NODENAME'] = df_indices

    data = df.to_dict('split')['data']   # [['M1047751', 2], ['M1027011', 3], ['L3254214', 4], ['M1089203', 5]]
    out: Dict[str, int]  = {}
    for bus_name, node_name in data:
        out[str(bus_name)] = node_name

    if save_pickle:
        with open('pickle_data/busname_to_nodename.p', 'wb') as f:
            pickle.dump(out, f)

    return out


def get_arcs(bus_node_map: dict, save_pickle: bool = True):
    df = pd.read_csv(
        'csv_data/Lines.csv',
        names=['Bus1', 'Bus2', 'Length', 'LineCode'],
        usecols=[1, 3, 5, 7]
    )

    df['Bus1'] = df['Bus1'].astype('str')
    df['Bus2'] = df['Bus2'].astype('str')

    def map(data):
        #  D6231996-1_INT

        bus1: str = data['Bus1'].lstrip()
        bus2: str = data['Bus2'].lstrip()

        out = [bus_node_map.get(bus1), bus_node_map.get(bus2)]
        # print([bus1, bus2], out)
        return pd.Series(out, index=['Node1', 'Node2'])

    df[['Node1', 'Node2']] = df.apply(map, axis=1)

    # print(df)
