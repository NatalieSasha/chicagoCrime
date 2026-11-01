"""Generate restrained observations directly from the selected records."""
from src.eda import category_frequencies


def generate_insights(frame):
    notes = []
    total = len(frame)
    counts = category_frequencies(frame)
    if total and not counts.empty:
        name, n = counts.index[0], int(counts.iloc[0])
        notes.append(f"'{name}' is the most frequently recorded category ({n:,} records, {n / total:.1%} of filtered records).")
    if total and "area" in frame and frame.area.notna().any():
        counts_area = frame.area.value_counts()
        notes.append(f"'{counts_area.index[0]}' has the most recorded incidents among available areas ({int(counts_area.iloc[0]):,}).")
    if total and "date" in frame:
        dates = frame.date.dropna()
        if len(dates) >= 7:
            day = dates.dt.day_name().value_counts()
            notes.append(f"{day.index[0]} has the highest recorded count among weekdays ({int(day.iloc[0]):,}).")
    return notes or ["Not enough complete filtered data is available to generate a stable descriptive observation."]
