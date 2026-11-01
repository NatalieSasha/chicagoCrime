"""Reusable, conservative data cleaning helpers."""
import pandas as pd


def preprocess_data(frame):
    """Return cleaned data and a report; retain rows with missing optional values."""
    original = frame.copy(deep=True)
    clean = frame.copy(deep=True)
    clean.columns = ["_".join(str(c).strip().lower().replace("-", " ").split()) for c in clean.columns]
    before = len(clean)
    duplicates = int(clean.duplicated().sum())
    clean = clean.drop_duplicates().copy()
    if "date" in clean:
        clean["date"] = pd.to_datetime(clean["date"], errors="coerce")
    for col in ("category", "area"):
        if col in clean:
            clean[col] = clean[col].astype("string").str.strip().replace("", pd.NA)
    for col in ("latitude", "longitude"):
        if col in clean:
            clean[col] = pd.to_numeric(clean[col], errors="coerce")
    if "latitude" in clean:
        clean.loc[~clean.latitude.between(-90, 90), "latitude"] = pd.NA
    if "longitude" in clean:
        clean.loc[~clean.longitude.between(-180, 180), "longitude"] = pd.NA
    report = {"records_before": before, "records_after": len(clean), "exact_duplicates_removed": duplicates,
              "invalid_dates": int(clean["date"].isna().sum()) if "date" in clean else None,
              "missing": clean.isna().sum().to_dict(), "missing_percent": (clean.isna().mean() * 100).round(2).to_dict(),
              "original": original}
    return clean.reset_index(drop=True), report
