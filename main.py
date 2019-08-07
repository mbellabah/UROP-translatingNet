import pickle
from typing import Dict

from os import path, listdir
from helpers import scrape_nodes, get_arcs


if __name__ == '__main__':
    pickles_bool = {filename: path.exists(f"pickle_data/{filename}") for filename in listdir('pickle_data')}

    busname_to_nodename: Dict[str, int]
    if pickles_bool.get('busname_to_nodename.p'):
        with open('pickle_data/busname_to_nodename.p', 'rb') as f:
            busname_to_nodename = pickle.load(f)
    else:
        busname_to_nodename = scrape_nodes(save_pickle=True)

    print(busname_to_nodename)

    get_arcs(busname_to_nodename)
