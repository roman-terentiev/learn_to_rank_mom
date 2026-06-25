import pandas as pd
import xgboost as xgb

from pathlib import Path

from modules.bt import yield_splits


def train_test_ltr(
    data, 
    num_train_years, 
    num_boost_round, 
    max_top_liquid, 
    model_params, 
    save_dir,
):
    cols = [
        col for col in data.columns
        if any(feat in col for feat in ("ret", "norm", "macd"))
    ]
    batches = []
    model = None

    for train, test in yield_splits(data, num_train_years):
        train = train.copy()
        train["rank"] = (
            train["nmr"]
            .groupby(level="date")
            .rank(method="dense", ascending=True)
            .astype(int)
        )
        X, y = train[cols], train["rank"]
        dmat = xgb.DMatrix(X, label=y, feature_names=cols)
        qid = train.groupby(level="date").size().to_list()
        dmat.set_group(qid)
        model = xgb.train(model_params, dmat, num_boost_round=num_boost_round)

        test = test.copy()
        test = (
            test
            .reset_index()
            .sort_values(["date", "adv63"], ascending=[True, False])
            .groupby("date", sort=False)
            .head(max_top_liquid)
            .set_index(["date", "sym"])
            .sort_index()
        )

        X = test[cols]
        dmat = xgb.DMatrix(X, feature_names=cols)
        qid = test.groupby(level="date").size().to_list()
        dmat.set_group(qid)
        test["pred"] = model.predict(dmat)
        batches.append(test)
    
    if save_dir is not None and model is not None:
        save_dir = Path(save_dir)
        model.save_model(save_dir / "model.json")

    return pd.concat(batches, axis=0).sort_index()