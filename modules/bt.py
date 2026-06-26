import pandas as pd
import matplotlib.pyplot as plt


def yield_splits(data, num_train_years):
    idx = data.index.get_level_values("date")
    dates = idx.unique()

    year = pd.Series(dates, index=dates).apply(lambda x: x.year if x.month != 12 else x.year + 1)
    start = year.iloc[0]

    # Walk-forward
    while start + num_train_years <= year.max():
        start_train = dates[year == start].min()
        start_test = dates[year == start + num_train_years].min()
        end_test = dates[year == start + num_train_years].max()
        end_train = dates[dates < start_test].max()

        train = data.loc[(idx >= start_train) & (idx <= end_train)]
        test = data.loc[(idx >= start_test) & (idx <= end_test)]

        yield train, test
        start += 1


def get_spread_curve(df_batches, save_dir, num_quantiles):
    spread_curve = df_batches.copy()
    by_date = spread_curve["pred"].groupby(level="date")
    spread_curve["rank"] = by_date.rank(pct=True)
    spread_curve["quantile"] = pd.cut(
        spread_curve["rank"],
        num_quantiles,
        labels=range(num_quantiles, 0, -1),
    )
    spread_curve = (
        spread_curve.groupby("quantile", observed=True)["nmr"].mean() + 1.0
    ) ** 12 - 1.0
    spread_curve = spread_curve * 100

    fig, ax = plt.subplots(figsize=(12, 6))
    spread_curve.plot(ax=ax, marker="o")
    ax.set_title("Spread Curve")
    ax.set_xlabel("Quantile")
    ax.set_ylabel("Annualized Return")
    fig.savefig(save_dir / "spread_curve.png", dpi=300, bbox_inches="tight")
    plt.close(fig)


def get_sym_w(df_batches, num_per_side, gross_leverage):
    df_batches = df_batches.copy()
    by_date = df_batches["pred"].groupby(level="date")
    num_per_date = by_date.transform("size")
    num_per_quantile = pd.Series(num_per_side, index=num_per_date.index)

    rank = by_date.rank(method="first", ascending=False) - 1
    idx_long = df_batches["pred"].index[rank < num_per_quantile]
    idx_short = df_batches["pred"].index[rank >= (num_per_date - num_per_quantile)]

    w = gross_leverage / num_per_quantile.loc[idx_long.union(idx_short)]
    df_batches["w"] = 0.0
    df_batches.loc[idx_long, "w"] = +w.loc[idx_long]
    df_batches.loc[idx_short, "w"] = -w.loc[idx_short]
    return df_batches


def get_equity(df_batches, round_trip_cost_bps, save_dir):
    prev_w = df_batches.groupby(level="sym")["w"].shift(fill_value=0)
    df_batches["turnover"] = (df_batches["w"] - prev_w).abs()
    df_batches["cost_ret"] = df_batches["turnover"] * (round_trip_cost_bps / 10000)
    df_batches["net_ret"] = df_batches["w"] * df_batches["nmr"] - df_batches["cost_ret"]

    has_w = df_batches["w"].groupby(level="date").any().cumsum().astype(bool)
    net_rets = df_batches["net_ret"].groupby(level="date").sum().loc[has_w]
    net_rets = net_rets.shift().dropna()
    equity = (net_rets + 1).cumprod().rename("equity")

    fig, ax = plt.subplots(figsize=(12, 6))
    equity.plot(ax=ax)
    ax.set_title("Equity Curve")
    ax.set_xlabel("Time")
    ax.set_ylabel("Return")
    fig.savefig(save_dir / "equity.png", dpi=300, bbox_inches="tight")
    plt.close(fig)

    equity.to_csv(save_dir / "equity.csv")
    return equity
