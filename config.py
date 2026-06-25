DATA_PATH = "../data/norgate/capitalspecial/stocks_20260304T105113Z.csv"

NUM_TRAIN_YEARS = 15
NUM_BOOST_ROUND = 200
MAX_TOP_LIQUID = 999999
MODEL_PARAMS = {
    "objective": "rank:ndcg",
    "eta": 0.1,
    "max_depth": 7,
    "ndcg_exp_gain": False,
    "verbosity": 1,
    "tree_method": "hist",
}

NUM_QUANTILES = 10

MIN_SYMS_PER_DAY = 1000
NUM_PER_SIDE = 150
GROSS_LEVERAGE = 1
ROUND_TRIP_COST_BPS = 10

STATS_NUM_PERIODS = 12
