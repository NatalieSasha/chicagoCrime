"""Crime Intelligence: interactive descriptive analysis dashboard."""
import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from src.data_loader import load_csv
from src.eda import category_frequencies, overview
from src.insights import generate_insights
from src.preprocessing import preprocess_data
from src.visualizations import create_charts

ROOT = Path(__file__).parent
DEFAULT_DATA = ROOT / "data" / "chicago_crime_2026_ytd.csv"
st.set_page_config(page_title="CRIME INTELLIGENCE", page_icon="▦", layout="wide",
                   initial_sidebar_state="expanded")

st.markdown("""
<style>
:root { color-scheme: light; }
.stApp { background:#F7F4EC; color:#292A27; }
[data-testid="stSidebar"] { background:#20211F; border-right:1px solid #343530; min-width:218px!important; max-width:218px!important; }
[data-testid="stSidebar"] > div:first-child { padding:1.1rem .7rem .8rem; }
[data-testid="stHeader"] { background:#F7F4EC; }
[data-testid="stMainBlockContainer"] { padding:1.35rem 2rem 3rem; max-width:1600px; }
h1,h2,h3 { color:#292A27!important; letter-spacing:-.025em; }
p, label, [data-testid="stCaptionContainer"] { color:#77786F; }
.brand { display:flex; gap:10px; align-items:center; padding:4px 5px 17px; border-bottom:1px solid #3B3C37; margin-bottom:13px; }
.brand-mark { width:34px; height:34px; border:1px solid #D88972; border-radius:9px; display:grid; place-items:center; color:#E3A28F; font-size:18px; font-weight:700; }
.brand-name { color:#FFFDF8; font-weight:700; letter-spacing:.06em; font-size:13px; }
.brand-sub { color:#AAA99F; font-size:10px; margin-top:3px; }
[data-testid="stSidebarNav"] { padding:3px 2px 8px; }
[data-testid="stSidebarNav"] ul { gap:3px; }
[data-testid="stSidebarNav"] a { border-radius:8px; color:#B7B6AD; min-height:38px; padding:7px 9px; font-size:12px; }
[data-testid="stSidebarNav"] a:hover { background:#30312D; color:#FFFDF8; }
[data-testid="stSidebarNav"] a[aria-current="page"] { background:#393832; color:#FFFDF8; border-left:3px solid #D88972; }
.page-kicker { color:#9F4350; text-transform:uppercase; letter-spacing:.13em; font-size:10px; font-weight:700; margin:0 0 4px; }
.page-description { color:#77786F; margin:0 0 12px; font-size:13px; }
.dataset-strip { background:#FFFDF8; border:1px solid #E8E3D9; border-radius:9px; padding:9px 13px; color:#77786F; font-size:11px; margin:10px 0 15px; }
.dataset-strip strong { color:#4A4943; font-weight:650; }
.kpi { min-height:98px; border:1px solid #E8E3D9; border-radius:10px; padding:13px 15px 11px; }
.kpi-tone-0 { background:#FFFDF8; }
.kpi-tone-1 { background:#DCD7F4; border-color:#D2CDEB; }
.kpi-tone-2 { background:#D8E5D2; border-color:#CBD9C5; }
.kpi-tone-3 { background:#F3E4A7; border-color:#E9DA9D; }
.kpi-label { color:#77786F; font-size:10px; text-transform:uppercase; letter-spacing:.07em; }
.kpi-value { color:#292A27; font-size:23px; line-height:1.2; font-weight:700; margin:8px 0 3px; overflow-wrap:anywhere; }
.kpi-note { color:#77786F; font-size:10px; }
.finding { min-height:74px; background:#FFFDF8; border:1px solid #E8E3D9; border-left:3px solid #9F4350; border-radius:8px; padding:13px 14px; color:#4A4943; font-size:12px; line-height:1.5; }
.finding-1 { border-left-color:#8D84BE; }
.finding-2 { border-left-color:#9BAE91; }
.section-title { font-size:16px; font-weight:650; color:#292A27; margin:12px 0 2px; }
.section-note { color:#77786F; font-size:11px; margin-bottom:8px; }
[data-testid="stMetric"] { background:#FFFDF8; border:1px solid #E8E3D9; border-radius:9px; padding:12px 14px; }
[data-testid="stMetricLabel"] { color:#77786F; }
[data-testid="stMetricValue"] { color:#292A27; }
[data-testid="stPlotlyChart"] { background:transparent; }
[data-testid="stDataFrame"] { border:1px solid #E8E3D9; border-radius:8px; }
[data-testid="stVerticalBlockBorderWrapper"] { background:#FFFDF8; border-color:#E8E3D9; border-radius:11px; }
div[data-testid="stAlert"] { border-radius:8px; background:#FFFDF8; }
div.stButton > button, div.stDownloadButton > button { border-radius:7px; border:1px solid #DDD7CB; color:#4A4943; background:#FFFDF8; }
div.stButton > button:hover, div.stDownloadButton > button:hover { border-color:#9F4350; color:#9F4350; }
.sidebar-foot { color:#AAA99F; font-size:10px; border-top:1px solid #3B3C37; padding-top:10px; margin-top:16px; }
@media (max-width:900px) { [data-testid="stMainBlockContainer"] { padding:1rem 1.1rem 2rem; } }
@media (max-width:640px) { [data-testid="stMainBlockContainer"] { padding:.8rem .75rem 1.5rem; } }
</style>
""", unsafe_allow_html=True)


@st.cache_data(show_spinner="Reading dataset…")
def load_and_prepare(path):
    raw_frame = load_csv(path)
    clean_frame, clean_report = preprocess_data(raw_frame)
    return raw_frame, clean_frame, clean_report


def chart(fig, height=340):
    fig.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      font={"family": "Inter, Arial, sans-serif", "color": "#77786F", "size": 11},
                      title={"font": {"size": 14, "color": "#292A27"}, "x": 0.02},
                      margin={"l": 18, "r": 18, "t": 55, "b": 24}, height=height,
                      legend={"bgcolor": "rgba(255,253,248,0)", "font": {"color": "#77786F"}},
                      hoverlabel={"bgcolor": "#FFFDF8", "font_color": "#292A27"})
    fig.update_xaxes(gridcolor="#EEEAE1", zerolinecolor="#EEEAE1", linecolor="#E8E3D9", showline=False)
    fig.update_yaxes(gridcolor="#EEEAE1", zerolinecolor="#EEEAE1", linecolor="#E8E3D9", showline=False)
    st.plotly_chart(fig, width="stretch")


def section(title, note=None):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)
    if note:
        st.markdown(f'<div class="section-note">{note}</div>', unsafe_allow_html=True)


def metric_card(label, value, note, index=0):
    st.markdown(f'<div class="kpi kpi-tone-{index % 4}"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>', unsafe_allow_html=True)


def chart_card(title, note, figure, height=330):
    with st.container(border=True):
        section(title, note)
        chart(figure, height)


def show_empty(message):
    st.info(message)


def render_overview(frame):
    summary = overview(frame)
    categories = category_frequencies(frame)
    coverage = f"{summary['date_start']:%Y} – {summary['date_end']:%Y}" if summary["date_start"] is not None else "Unavailable"
    values = [len(frame), summary["categories"] or 0, summary["areas"] or 0,
              categories.index[0] if not categories.empty else "Unavailable"]
    notes = ["Rows in current selection", "Distinct recorded labels", "Distinct named areas", "Highest recorded frequency"]
    labels = ["Recorded incidents", "Crime categories", "Geographical areas", "Most frequent category"]
    for index, (col, label, value, note) in enumerate(zip(st.columns(4), labels, values, notes)):
        with col:
            metric_card(label, f"{value:,}" if isinstance(value, int) else str(value), note, index)
    st.caption(f"Date coverage in the filtered records: {coverage}. Counts represent records, not population-adjusted crime rates.")

    left, right = st.columns([1.2, 1])
    with left:
        if "date" in frame and frame.date.notna().any():
            daily = frame.dropna(subset=["date"]).set_index("date").resample("D").size().rename("Incidents").reset_index()
            chart_card("Crime Trends Over Time", "Daily recorded incidents in the current selection.",
                       px.line(daily, x="date", y="Incidents", title="Daily incident count",
                               color_discrete_sequence=["#9F4350"], labels={"date": "Date"}), 325)
        else:
            with st.container(border=True):
                section("Crime Trends Over Time")
                show_empty("A trend chart needs valid incident dates.")
    with right:
        counts = category_frequencies(frame).head(10)
        if not counts.empty:
            chart_card("Crime Category Distribution", "Ten most frequent categories in the current selection.",
                       px.bar(counts.sort_values().rename_axis("Category").reset_index(name="Incidents"),
                              x="Incidents", y="Category", orientation="h", title="Recorded incidents",
                              color_discrete_sequence=["#D88972"]), 325)
        else:
            with st.container(border=True):
                section("Crime Category Distribution")
                show_empty("No category field is available.")

    left, right = st.columns(2)
    with left:
        if "area" in frame and frame.area.notna().any():
            areas = frame.area.value_counts().head(10).sort_values().rename_axis("Area").reset_index(name="Incidents")
            chart_card("Incidents by Geographical Area", "Recorded counts; not adjusted for population.",
                       px.bar(areas, x="Incidents", y="Area", orientation="h", title="Leading areas",
                              color_discrete_sequence=["#9BAE91"]), 300)
        else:
            with st.container(border=True):
                section("Incidents by Geographical Area")
                show_empty("Area information is unavailable in this dataset.")
    with right:
        if "date" in frame and frame.date.notna().any():
            weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            weekday = frame.date.dropna().dt.day_name().value_counts().reindex(weekday_order, fill_value=0)
            weekday_data = weekday.rename_axis("Weekday").rename("Incidents").reset_index()
            chart_card("Crime Patterns by Day", "Distribution by day of the week.",
                       px.bar(weekday_data, x="Weekday", y="Incidents", title="Recorded incidents by weekday",
                              color_discrete_sequence=["#8D84BE"]), 300)
        else:
            with st.container(border=True):
                section("Crime Patterns by Day")
                show_empty("Weekday patterns need valid incident dates.")

    section("Key Findings", "Calculated from the current filtered records.")
    findings = generate_insights(frame)[:3]
    for col, finding, index in zip(st.columns(max(1, len(findings))), findings, range(len(findings))):
        with col:
            st.markdown(f'<div class="finding finding-{index}">{finding}</div>', unsafe_allow_html=True)


def render_categories(frame):
    section("Crime Categories", "Compare category frequency and share in the selected records.")
    counts = category_frequencies(frame)
    if counts.empty:
        show_empty("Category analysis is unavailable because the dataset has no recognized category column."); return
    limit = st.slider("Categories to display", 3, max(3, min(30, len(counts))), min(12, max(3, len(counts))))
    shown = counts.head(limit)
    left, right = st.columns([1.2, .8])
    with left:
        chart_card("Category Ranking", "Sorted from the most to least frequently recorded.",
                   px.bar(shown.sort_values().rename_axis("Category").reset_index(name="Incidents"),
                          x="Incidents", y="Category", orientation="h", title="Recorded incidents",
                          color_discrete_sequence=["#9F4350"]), max(340, 26 * len(shown) + 100))
    with right:
        share = (shown / max(1, len(frame)) * 100).sort_values().rename("Share (%)").rename_axis("Category").reset_index()
        chart_card("Category Share", "Percentage of all filtered incident records.",
                   px.bar(share, x="Share (%)", y="Category", orientation="h", title="Share by category",
                          color_discrete_sequence=["#D88972"]), max(340, 26 * len(shown) + 100))
    table = counts.rename("Incidents").rename_axis("Category").rename_axis(index=None).reset_index()
    table["Share"] = (table.Incidents / max(1, len(frame)) * 100).round(2)
    section("Frequency and percentage")
    st.dataframe(table, hide_index=True, width="stretch")
    if {"area", "category"}.issubset(frame.columns) and frame.area.notna().any():
        section("Category comparison across areas")
        cross = frame.groupby(["area", "category"], observed=True).size().rename("Incidents").reset_index()
        chart(px.bar(cross, x="area", y="Incidents", color="category", barmode="stack", title="Recorded categories by area",
                     color_discrete_sequence=["#9F4350", "#D88972", "#8D84BE", "#9BAE91", "#D1B153", "#6D9BB8"]), 390)


def render_temporal(frame):
    section("Temporal Analysis", "Explore recorded dates and time-of-day patterns. The date range filter is shared with all pages.")
    if "date" not in frame or not frame.date.notna().any():
        show_empty("Temporal analysis is unavailable because no valid date field was detected."); return
    timed = frame.dropna(subset=["date"]).copy()
    a, b = st.columns(2)
    with a:
        daily = timed.set_index("date").resample("D").size().rename("Incidents").reset_index()
        chart(px.line(daily, x="date", y="Incidents", title="Recorded incidents over time", labels={"date": "Date"},
                      color_discrete_sequence=["#9F4350"]), 330)
    with b:
        month_counts = timed.date.dt.month.value_counts().sort_index().reindex(range(1, 13), fill_value=0)
        month_names = [pd.Timestamp(2000, m, 1).strftime("%b") for m in range(1, 13)]
        month_data = pd.DataFrame({"Month": month_names, "Incidents": month_counts.values})
        chart(px.bar(month_data, x="Month", y="Incidents", title="Distribution by calendar month",
                     color_discrete_sequence=["#D88972"]), 330)
    c, d = st.columns(2)
    weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    with c:
        weekdays = timed.date.dt.day_name().value_counts().reindex(weekday_order, fill_value=0).rename_axis("Weekday").rename("Incidents").reset_index()
        chart(px.bar(weekdays, x="Weekday", y="Incidents", title="Recorded incidents by weekday",
                     color_discrete_sequence=["#8D84BE"]), 330)
    with d:
        timed["hour"] = timed.date.dt.hour
        chart(px.histogram(timed, x="hour", nbins=24, title="Distribution by hour of day", labels={"hour": "Hour (0–23)"},
                           color_discrete_sequence=["#D1B153"]), 330)
    if timed.date.dt.year.nunique() > 1:
        yearly = timed.date.dt.year.value_counts().sort_index().rename_axis("Year").rename("Incidents").reset_index()
        chart(px.bar(yearly, x="Year", y="Incidents", title="Recorded incidents by year",
                     color_discrete_sequence=["#9F4350"]), 300)
    section("Weekday and hour pattern")
    timed["weekday"] = timed.date.dt.day_name()
    heat = timed.groupby(["weekday", "hour"]).size().rename("Incidents").reset_index()
    chart(px.density_heatmap(heat, x="hour", y="weekday", z="Incidents", histfunc="sum",
                             category_orders={"weekday": weekday_order}, title="Recorded incidents by weekday and hour",
                             labels={"hour": "Hour (0–23)"}, color_continuous_scale=[[0, "#F3E4A7"], [.5, "#D88972"], [1, "#9F4350"]]), 370)
    timed["Period"] = timed.date.dt.day_name().map(lambda day: "Weekend" if day in ("Saturday", "Sunday") else "Weekday")
    comp = timed.Period.value_counts().reindex(["Weekday", "Weekend"], fill_value=0).rename_axis("Period").rename("Incidents").reset_index()
    chart(px.bar(comp, x="Period", y="Incidents", title="Weekday versus weekend counts",
                 color="Period", color_discrete_map={"Weekday": "#8D84BE", "Weekend": "#D88972"}), 290)
    st.caption("The displayed time patterns summarize this dataset’s recorded dates and should not be interpreted as seasonal effects without sufficient multi-year coverage.")


def render_geography(frame):
    section("Geographical Analysis", "Compare named areas and supplied coordinates where available.")
    if "area" not in frame:
        show_empty("No recognized district, city, neighborhood, or area column is available."); return
    areas = frame.area.value_counts().rename_axis("Area").rename("Incidents").reset_index()
    if areas.empty:
        show_empty("Area values are missing in the current selection."); return
    focus_area = st.selectbox("Focus area", areas.Area.tolist(), key="geography_focus_area")
    focus_rows = frame[frame.area.astype(str) == str(focus_area)]
    focus_category = focus_rows.category.value_counts().index[0] if "category" in focus_rows and not focus_rows.category.dropna().empty else "Unavailable"
    m1, m2, m3 = st.columns(3)
    m1.metric("Selected area", focus_area)
    m2.metric("Recorded incidents", f"{len(focus_rows):,}")
    m3.metric("Most frequent category", focus_category)
    left, right = st.columns([1, 1])
    with left:
        chart(px.bar(areas.head(15).sort_values("Incidents"), x="Incidents", y="Area", orientation="h",
                     title="Ranked recorded incidents by area", color_discrete_sequence=["#9F4350"]), 390)
    with right:
        section("Area frequency table")
        areas["Share of filtered records (%)"] = (areas.Incidents / max(1, len(frame)) * 100).round(2)
        st.dataframe(areas, hide_index=True, width="stretch", height=390)
    if "category" in frame:
        cross = frame.groupby(["area", "category"], observed=True).size().rename("Incidents").reset_index()
        chart(px.bar(cross, x="area", y="Incidents", color="category", barmode="stack",
                     title="Category composition by area"), 390)
    if {"latitude", "longitude"}.issubset(frame.columns):
        points = frame.dropna(subset=["latitude", "longitude"])
        if not points.empty:
            points = points.assign(latitude_plot=points.latitude.round(2), longitude_plot=points.longitude.round(2))
            grouped_points = points.groupby(["latitude_plot", "longitude_plot"], as_index=False).size().rename(columns={"size": "Incidents"})
            map_fig = px.scatter_map(grouped_points, lat="latitude_plot", lon="longitude_plot", size="Incidents",
                                     hover_data={"Incidents": True, "latitude_plot": False, "longitude_plot": False}, zoom=9,
                                     title="Supplied incident coordinates", map_style="carto-positron")
            map_fig.update_layout(paper_bgcolor="#FFFDF8", font_color="#77786F", margin={"l": 8, "r": 8, "t": 50, "b": 8}, height=500)
            st.plotly_chart(map_fig, width="stretch")
            st.caption("Coordinates are approximate, rounded for display, and must not be used to infer a specific address.")
        else:
            show_empty("No valid latitude/longitude pairs remain after validation; no map is shown.")
    else:
        st.caption("Only named area-level comparisons are shown. No exact incident map is generated without valid supplied coordinates.")


def render_insights(frame):
    section("Statistical Insights", "Descriptive results from the current filtered dataset.")
    for item in generate_insights(frame):
        st.markdown(f"- {item}")
    left, right = st.columns(2)
    with left:
        section("Dataset overview")
        stats = overview(frame)
        stat_values = [stats["records"], stats["attributes"], stats["categories"] or "Unavailable",
                       stats["areas"] or "Unavailable",
                       stats["date_start"].isoformat() if stats["date_start"] is not None else "Unavailable",
                       stats["date_end"].isoformat() if stats["date_end"] is not None else "Unavailable"]
        st.dataframe(pd.DataFrame({"Measure": ["Records", "Available attributes", "Crime categories", "Geographical areas", "Date start", "Date end"],
                                   "Value": stat_values}), hide_index=True, width="stretch")
        numerical = frame.select_dtypes(include="number")
        if not numerical.empty:
            section("Numerical descriptive statistics")
            st.dataframe(numerical.describe().T, width="stretch")
    with right:
        section("Numerical correlation", "Association between numeric columns; correlation does not establish causation.")
        numerical = frame.select_dtypes(include="number")
        if len(numerical.columns) >= 2:
            chart(px.imshow(numerical.corr(), text_auto=".2f", color_continuous_scale=["#9F4350", "#FFFDF8", "#6D9BB8"], zmin=-1, zmax=1,
                            title="Correlation matrix"), 380)
        else:
            show_empty("At least two numeric columns are needed for correlation analysis.")
    if {"category", "area"}.issubset(frame.columns):
        section("Category and area cross-tabulation")
        table = pd.crosstab(frame.area, frame.category)
        st.dataframe(table, width="stretch")
    st.info("Recorded incident counts are shaped by reporting practices, population differences, data coverage, and collection methods. They are not population-adjusted rates, and findings should not be treated as causal or operational conclusions.")


def render_quality(raw_frame, clean_frame, report):
    section("Data Quality", "Preprocessing summary and quality checks for the loaded dataset.")
    before, after, dup, invalid = st.columns(4)
    before.metric("Records before cleaning", f"{report['records_before']:,}")
    after.metric("Records after cleaning", f"{report['records_after']:,}")
    dup.metric("Exact duplicates removed", f"{report['exact_duplicates_removed']:,}")
    invalid.metric("Invalid or missing dates", f"{report['invalid_dates']:,}" if report["invalid_dates"] is not None else "N/A")
    quality = pd.DataFrame({"Column": raw_frame.columns, "Data type": raw_frame.dtypes.astype(str).values,
                            "Missing before cleaning": raw_frame.isna().sum().values,
                            "Missing after cleaning": clean_frame.isna().sum().reindex(raw_frame.columns, fill_value=0).values,
                            "Missing after (%)": (clean_frame.isna().mean().reindex(raw_frame.columns, fill_value=0) * 100).round(2).values})
    st.dataframe(quality, hide_index=True, width="stretch")
    section("Preprocessing performed")
    st.markdown("- Standardized column labels and mapped recognized schema aliases.\n- Parsed date values safely; unparseable values are retained as missing.\n- Trimmed category and area labels.\n- Converted coordinates to numeric values and marked out-of-range coordinates missing.\n- Removed exact duplicate rows while retaining other potentially repeated incidents.")
    st.caption("Missing values are reported rather than imputed or dropped so that dataset-specific choices remain transparent.")


def render_explorer(frame):
    section("Dataset Explorer", "Search and inspect records after applying the shared filters.")
    query = st.text_input("Search visible columns", placeholder="Search category, area, description…")
    visible = frame
    if query.strip():
        mask = visible.astype("string").apply(lambda column: column.str.contains(query.strip(), case=False, na=False)).any(axis=1)
        visible = visible[mask]
    limit = st.selectbox("Rows per view", [25, 50, 100, 250, "All"], index=1)
    page = 1
    if limit != "All":
        page_count = max(1, (len(visible) + limit - 1) // limit)
        page = st.number_input("Page", min_value=1, max_value=page_count, value=1, step=1)
        display = visible.iloc[(page - 1) * limit:page * limit]
    else:
        display = visible
    st.caption(f"Showing {len(display):,} of {len(visible):,} matching rows ({len(frame):,} rows after shared filters).")
    st.dataframe(display, hide_index=True, width="stretch")
    st.download_button("Download filtered CSV", visible.to_csv(index=False), "filtered_crime_data.csv", "text/csv")


def overview_page():
    render_overview(filtered)


def category_page():
    render_categories(filtered)


def temporal_page():
    render_temporal(filtered)


def geography_page():
    render_geography(filtered)


def insights_page():
    render_insights(filtered)


def quality_page():
    render_quality(raw, clean, preprocessing)


def explorer_page():
    render_explorer(filtered)


with st.sidebar:
    st.markdown('<div class="brand"><div class="brand-mark">⌖</div><div><div class="brand-name">CRIME INTELLIGENCE</div><div class="brand-sub">Crime Data Analysis</div></div></div>', unsafe_allow_html=True)
    selected_page = st.navigation([
        st.Page(overview_page, title="Overview", icon=":material/dashboard:", default=True),
        st.Page(category_page, title="Crime Categories", icon=":material/category:"),
        st.Page(temporal_page, title="Temporal Analysis", icon=":material/calendar_month:"),
        st.Page(geography_page, title="Geographical Analysis", icon=":material/map:"),
        st.Page(insights_page, title="Statistical Insights", icon=":material/analytics:"),
        st.Page(quality_page, title="Data Quality", icon=":material/fact_check:"),
        st.Page(explorer_page, title="Dataset Explorer", icon=":material/table_view:"),
    ], position="sidebar")
    st.markdown("<div class='page-kicker' style='margin-top:12px'>Dataset</div>", unsafe_allow_html=True)
    dataset_path = st.text_input("CSV dataset path", os.getenv("CRIME_DATA_PATH", str(DEFAULT_DATA)), key="dataset_path", label_visibility="collapsed")

try:
    raw, clean, preprocessing = load_and_prepare(dataset_path)
except (FileNotFoundError, ValueError) as error:
    st.error(str(error)); st.stop()

dataset_name = Path(dataset_path).name.lower()
synthetic = dataset_name == "sample_crime_data.csv"
public_snapshot = dataset_name.startswith("chicago_crime_")
dates = clean.date.dropna() if "date" in clean else pd.Series(dtype="datetime64[ns]")
coverage = f"{dates.min():%Y-%m-%d} to {dates.max():%Y-%m-%d}" if not dates.empty else "Date coverage unavailable"
date_bounds = (dates.min().date(), dates.max().date()) if not dates.empty else None
category_options = sorted(clean.category.dropna().astype(str).unique()) if "category" in clean else []
area_options = sorted(clean.area.dropna().astype(str).unique()) if "area" in clean else []
weekday_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
day_options = [day for day in weekday_order if "date" in clean and day in clean.date.dropna().dt.day_name().values]

if st.session_state.get("filter_dataset_path") != dataset_path:
    st.session_state["filter_dataset_path"] = dataset_path
    st.session_state["filter_dates"] = date_bounds
    st.session_state["filter_categories"] = category_options
    st.session_state["filter_areas"] = area_options
    st.session_state["filter_days"] = day_options

with st.sidebar:
    with st.expander("Filters", expanded=False):
        if st.button("Clear all filters", key="clear_all_filters", width="stretch"):
            st.session_state["filter_dates"] = date_bounds
            st.session_state["filter_categories"] = category_options
            st.session_state["filter_areas"] = area_options
            st.session_state["filter_days"] = day_options
            st.rerun()
        if date_bounds:
            date_selection = st.date_input("Date range", min_value=date_bounds[0], max_value=date_bounds[1], key="filter_dates")
        else:
            date_selection = None
        selected_categories = st.multiselect("Crime categories", category_options, key="filter_categories") if category_options else []
        selected_areas = st.multiselect("Geographical areas", area_options, key="filter_areas") if area_options else []
        selected_days = st.multiselect("Weekdays", day_options, key="filter_days") if day_options else []
    st.markdown("<div class='sidebar-foot'>2026 public-data snapshot<br>Counts describe supplied records.</div>", unsafe_allow_html=True)

filtered = clean.copy()
if date_selection and isinstance(date_selection, tuple) and len(date_selection) == 2 and "date" in filtered:
    start, end = map(pd.Timestamp, date_selection)
    filtered = filtered[filtered.date.between(start, end + pd.Timedelta(days=1) - pd.Timedelta(microseconds=1))]
if "category" in filtered:
    filtered = filtered[filtered.category.astype(str).isin(selected_categories)]
if "area" in filtered:
    filtered = filtered[filtered.area.astype(str).isin(selected_areas)]
if "date" in filtered and selected_days:
    filtered = filtered[filtered.date.dt.day_name().isin(selected_days)]

titles = {"Overview": ("Crime Intelligence", "Overview of recorded incidents, category distributions, and geographical patterns."),
          "Crime Categories": ("Crime Categories", "Compare the frequency and share of recorded categories."),
          "Temporal Analysis": ("Temporal Analysis", "Explore how recorded incidents are distributed across time."),
          "Geographical Analysis": ("Geographical Analysis", "Compare named areas and supplied approximate coordinates."),
          "Statistical Insights": ("Statistical Insights", "Descriptive statistics and dynamically calculated findings."),
          "Data Quality": ("Data Quality", "Understand missing values, duplicates, and preprocessing effects."),
          "Dataset Explorer": ("Dataset Explorer", "Search, inspect, and export the filtered records.")}
title, description = titles[selected_page.title]
st.markdown("<div class='page-kicker'>CRIME DATA ANALYSIS</div>", unsafe_allow_html=True)
st.title(title)
st.markdown(f"<div class='page-description'>{description}</div>", unsafe_allow_html=True)
status = "Synthetic demonstration data" if synthetic else "Public dataset snapshot" if public_snapshot else "User-supplied dataset"
st.markdown(f"<div class='dataset-strip'><strong>Dataset</strong> &nbsp;{Path(dataset_path).name} &nbsp;&nbsp;·&nbsp;&nbsp; <strong>Coverage</strong> &nbsp;{coverage} &nbsp;&nbsp;·&nbsp;&nbsp; <strong>Status</strong> &nbsp;{status} &nbsp;&nbsp;·&nbsp;&nbsp; <strong>Filtered records</strong> &nbsp;{len(filtered):,}</div>", unsafe_allow_html=True)

selected_page.run()

with st.sidebar:
    if st.button("Export static charts", width="stretch"):
        try:
            saved_paths = create_charts(filtered, ROOT / "outputs")
            st.success(f"Saved {len(saved_paths)} chart(s) in outputs/.")
        except (ImportError, OSError, ValueError) as error:
            st.error(f"Chart export failed: {error}")
