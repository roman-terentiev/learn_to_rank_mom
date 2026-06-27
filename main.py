import pandas as pd
from datetime import datetime, timezone
import time

from pathlib import Path
import shutil
import subprocess
import sys

from modules.prep import drop_sparse_dates
from modules.bt import get_equity, get_spread_curve, get_sym_w
from modules.ltr import train_test_ltr
from modules.stats import get_rets_heat, get_stats
from config import *


if __name__ == "__main__":
    start_time = time.perf_counter()
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    print(f"Run ID: {run_id}")

    runs_dir = Path("runs")
    runs_dir.mkdir(parents=True, exist_ok=True)
    run_dir = runs_dir / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    in_dir = run_dir / "in"
    out_dir = run_dir / "out"
    in_dir.mkdir()
    out_dir.mkdir()

    shutil.copy2("config.py", in_dir / "config.py")
    with (in_dir / "requirements.txt").open("w") as file:
        subprocess.run([sys.executable, "-m", "pip", "freeze"], stdout=file, check=True)

    df = pd.read_csv(DATA_PATH, parse_dates=["date"]).set_index(["date", "sym"])
    df.describe().round(2).to_csv(out_dir / "describe_data.csv")

    df = drop_sparse_dates(df, min_syms=MIN_SYMS_PER_DAY)
    df.describe().round(2).to_csv(out_dir / "describe_drop_sparse.csv")

    df_batches = train_test_ltr(
        df,
        num_train_years=NUM_TRAIN_YEARS,
        num_boost_round=NUM_BOOST_ROUND,
        max_top_liquid=MAX_TOP_LIQUID,
        model_params=MODEL_PARAMS,
        save_dir=out_dir,
    )
    get_spread_curve(df_batches, save_dir=out_dir, num_quantiles=NUM_QUANTILES)

    df_batches = get_sym_w(
        df_batches,
        num_per_side=NUM_PER_SIDE,
        gross_leverage=GROSS_LEVERAGE,
    )
    equity = get_equity(
        df_batches, 
        round_trip_cost_bps=ROUND_TRIP_COST_BPS, 
        save_dir=out_dir
    )

    get_stats(equity, num_periods=STATS_NUM_PERIODS, save_dir=out_dir)
    get_rets_heat(equity, save_dir=out_dir)

    elapsed = time.perf_counter() - start_time
    print(f"Time elapsed: {elapsed:.2f} seconds")