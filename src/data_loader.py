"""CSV loading and flexible crime schema detection."""
from pathlib import Path
import pandas as pd


ALIASES = {
    "date": ["date", "incident_date", "datetime", "date_time", "occurred_on"],
    "category": ["category", "crime_type", "primary_type", "offense", "crime_category"],
    "area": ["area", "district", "neighborhood", "city", "borough", "location"],
    "latitude": ["latitude", "lat"], "longitude": ["longitude", "lon", "lng"],
    "incident_id": ["incident_id", "id", "case_number", "record_id"],
}


def standardize_columns(frame):
    """Convert headers to lowercase snake_case and normalize common aliases."""
    result = frame.copy()
    result.columns = ["_".join(str(c).strip().lower().replace("-", " ").split()) for c in result.columns]
    rename = {}
    for canonical, aliases in ALIASES.items():
        for col in result.columns:
            if col in aliases:
                rename[col] = canonical
                break
    return result.rename(columns=rename)


def load_csv(path):
    """Load a CSV, raising an actionable error for absent or invalid input."""
    source = Path(path).expanduser()
    if not source.is_file():
        raise FileNotFoundError(f"Dataset not found: {source}. Set CRIME_DATA_PATH to a valid CSV file.")
    try:
        frame = pd.read_csv(source)
    except Exception as exc:
        raise ValueError(f"Could not read CSV '{source}': {exc}") from exc
    if frame.empty or len(frame.columns) == 0:
        raise ValueError("The CSV contains no usable rows or columns.")
    return standardize_columns(frame)
