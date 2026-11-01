"""Descriptive summaries that work with partially known schemas."""
import pandas as pd


def overview(frame):
    result = {"records": len(frame), "attributes": len(frame.columns), "categories": int(frame.category.nunique()) if "category" in frame else None,
              "areas": int(frame.area.nunique()) if "area" in frame else None, "date_start": None, "date_end": None,
              "missing": frame.isna().sum(), "duplicates": int(frame.duplicated().sum()), "numeric": frame.select_dtypes("number").describe()}
    if "date" in frame:
        dates = pd.to_datetime(frame.date, errors="coerce").dropna()
        if not dates.empty:
            result["date_start"], result["date_end"] = dates.min(), dates.max()
    return result


def category_frequencies(frame):
    if "category" not in frame:
        return pd.Series(dtype="int64")
    return frame.category.dropna().value_counts()


def temporal_counts(frame, period="D"):
    if "date" not in frame:
        return pd.Series(dtype="int64")
    dates = pd.to_datetime(frame.date, errors="coerce").dropna()
    if dates.empty:
        return pd.Series(dtype="int64")
    return dates.dt.to_period(period).value_counts().sort_index()
