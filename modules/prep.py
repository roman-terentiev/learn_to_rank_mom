import numpy as np
import pandas as pd


def drop_sparse_dates(data, min_syms):
    num_syms = data.groupby(level="date").size()
    dates = num_syms[num_syms > min_syms].index
    return data.loc[dates]