"""Export reproducible static plots using Matplotlib and Seaborn."""
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from src.eda import category_frequencies


def create_charts(frame, output_dir="outputs"):
    out = Path(output_dir); out.mkdir(parents=True, exist_ok=True)
    saved = []
    sns.set_theme(style="whitegrid")
    counts = category_frequencies(frame).head(12)
    if not counts.empty:
        fig, ax = plt.subplots(figsize=(9, 5)); counts.sort_values().plot.barh(ax=ax, color="#3178a8")
        ax.set(title="Most frequently recorded crime categories", xlabel="Recorded incidents", ylabel="Category")
        fig.tight_layout(); path=out / "crime_categories.png"; fig.savefig(path, dpi=160); plt.close(fig); saved.append(path)
    if "date" in frame and pd.to_datetime(frame.date, errors="coerce").notna().any():
        dates=pd.to_datetime(frame.date, errors="coerce").dropna()
        monthly=dates.dt.to_period("M").value_counts().sort_index()
        fig, ax=plt.subplots(figsize=(10,4)); monthly.plot(ax=ax, marker="o", color="#d06b36")
        ax.set(title="Recorded incidents by month", xlabel="Month", ylabel="Recorded incidents"); fig.tight_layout()
        path=out / "incidents_by_month.png"; fig.savefig(path,dpi=160); plt.close(fig); saved.append(path)
        if dates.dt.year.nunique() > 1:
            yearly=dates.dt.year.value_counts().sort_index()
            fig, ax=plt.subplots(figsize=(9,4)); yearly.plot(ax=ax, marker="o", color="#3178a8")
            ax.set(title="Recorded incidents by year", xlabel="Year", ylabel="Recorded incidents"); fig.tight_layout()
            path=out / "incidents_by_year.png"; fig.savefig(path,dpi=160); plt.close(fig); saved.append(path)
        weekday_order=["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
        weekday=dates.dt.day_name().value_counts().reindex(weekday_order,fill_value=0)
        fig, ax=plt.subplots(figsize=(9,4)); weekday.plot.bar(ax=ax,color="#3178a8")
        ax.set(title="Recorded incidents by weekday",xlabel="Weekday",ylabel="Recorded incidents"); fig.tight_layout()
        path=out / "incidents_by_weekday.png"; fig.savefig(path,dpi=160); plt.close(fig); saved.append(path)
    if "latitude" in frame and "longitude" in frame:
        points=frame[["latitude","longitude"]].dropna()
        if not points.empty:
            fig,ax=plt.subplots(figsize=(7,6)); ax.scatter(points.longitude,points.latitude,s=10,alpha=.45)
            ax.set(title="Incident coordinates",xlabel="Longitude",ylabel="Latitude"); fig.tight_layout()
            path=out / "incident_coordinates.png"; fig.savefig(path,dpi=160); plt.close(fig); saved.append(path)
    return saved
