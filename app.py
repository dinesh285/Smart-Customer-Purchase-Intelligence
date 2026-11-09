from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="PIGMENT | Customer Purchase Intelligence",
    page_icon="✦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------------------------------------
# CUSTOM STYLING
# ---------------------------------------------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: linear-gradient(135deg, #0b1020 0%, #111a2e 55%, #101827 100%);
        color: #eef2ff;
    }

    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    [data-testid="stSidebar"] {
        background: #0c1425;
        border-right: 1px solid #26334c;
    }

    .hero {
        padding: 30px 34px;
        border: 1px solid #2a3955;
        border-radius: 24px;
        background: linear-gradient(110deg, rgba(48,71,111,.58), rgba(23,36,59,.76));
        margin-bottom: 22px;
    }

    .eyebrow {
        color: #a5b4fc;
        text-transform: uppercase;
        letter-spacing: 2px;
        font-size: 11px;
        font-weight: 700;
    }

    .hero-title {
        font-family: 'Manrope', sans-serif;
        font-size: clamp(25px, 3vw, 36px);
        font-weight: 800;
        letter-spacing: -1.2px;
        margin: 8px 0;
        color: #ffffff;
    }

    .hero-sub {
        color: #b8c5dc;
        font-size: 14px;
        line-height: 1.7;
    }

    .metric {
        background: linear-gradient(145deg, #17243a, #111c30);
        border: 1px solid #2a3a56;
        border-radius: 18px;
        padding: 18px 20px;
        min-height: 112px;
    }

    .metric-label {
        font-size: 11px;
        color: #9aabc5;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .metric-value {
        font-family: 'Manrope', sans-serif;
        font-size: 27px;
        font-weight: 800;
        color: #f8fafc;
        margin-top: 7px;
    }

    .metric-note {
        font-size: 11px;
        color: #8ee3cf;
        margin-top: 3px;
    }

    .section-title {
        font-family: 'Manrope', sans-serif;
        font-weight: 700;
        font-size: 19px;
        margin: 22px 0 10px;
        color: #e8edfa;
    }

    .upload-panel {
        background: rgba(23, 36, 58, .72);
        border: 1px solid #344866;
        border-radius: 18px;
        padding: 20px 22px;
        margin: 16px 0 22px;
    }

    .hint {
        color: #aebed5;
        font-size: 13px;
        line-height: 1.7;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #293954;
        border-radius: 14px;
        overflow: hidden;
    }

    .stButton button, .stDownloadButton button {
        border-radius: 10px;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------
st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">DATA SCIENCE • BIG DATA ANALYTICS</div>
        <div class="hero-title">Customer Purchase Intelligence</div>
        <div class="hero-sub">
            Explore customer buying behaviour, product performance, revenue trends,
            and city-wise sales. Upload your own retail CSV file to generate the dashboard.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# DATA UPLOAD
# ---------------------------------------------------------
st.sidebar.markdown("## ✦ PIGMENT")
st.sidebar.caption("Customer Purchase Intelligence")
st.sidebar.markdown("---")
st.sidebar.markdown("### Upload your dataset")

uploaded_file = st.sidebar.file_uploader(
    "Choose a retail transactions CSV",
    type=["csv"],
    help="Upload a CSV containing the required transaction columns.",
)

required_columns = [
    "transaction_id",
    "customer_id",
    "transaction_date",
    "product_id",
    "product_name",
    "category",
    "quantity",
    "unit_price",
    "total_amount",
    "payment_method",
    "city",
]

st.sidebar.markdown("---")
st.sidebar.caption("Your file is processed in this app session. No CSV is bundled with this project.")

if uploaded_file is None:
    st.markdown(
        """
        <div class="upload-panel">
            <div class="section-title" style="margin-top:0">Start by uploading your dataset</div>
            <div class="hint">
                Use the <b>Choose a retail transactions CSV</b> control in the left sidebar.
                Once your CSV is uploaded, the dashboard will automatically display KPIs,
                revenue charts, product insights, city comparisons, and transaction records.
                <br><br>
                <b>Required columns:</b> transaction_id, customer_id, transaction_date,
                product_id, product_name, category, quantity, unit_price, total_amount,
                payment_method, city.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("View an example CSV header"):
        st.code(
            "transaction_id,customer_id,transaction_date,product_id,product_name,"
            "category,quantity,unit_price,total_amount,payment_method,city",
            language="text",
        )

    st.info("Upload a CSV from the sidebar to open the analytics dashboard.")
    st.stop()

# ---------------------------------------------------------
# READ AND VALIDATE UPLOADED CSV
# ---------------------------------------------------------
try:
    uploaded_file.seek(0)
    df = pd.read_csv(uploaded_file)
except Exception as exc:
    st.error(f"Unable to read this CSV file: {exc}")
    st.stop()

# Normalize headers to avoid issues caused by spaces/capital letters.
df.columns = [str(column).strip().lower() for column in df.columns]

missing_columns = [column for column in required_columns if column not in df.columns]
if missing_columns:
    st.error("Your CSV is missing required columns:")
    st.code(", ".join(missing_columns))
    st.markdown("Please upload a CSV with all 11 required columns. Check the example header in the sidebar.")
    st.stop()

if df.empty:
    st.error("The uploaded CSV has column headers but no transaction records.")
    st.stop()

# Clean types used by the dashboard.
df["transaction_date"] = pd.to_datetime(df["transaction_date"], errors="coerce")
for numeric_column in ["quantity", "unit_price", "total_amount"]:
    df[numeric_column] = pd.to_numeric(df[numeric_column], errors="coerce")

df = df.dropna(
    subset=[
        "transaction_id",
        "customer_id",
        "transaction_date",
        "product_name",
        "category",
        "quantity",
        "total_amount",
        "city",
    ]
).copy()

if df.empty:
    st.error("No valid transaction rows remain after checking dates and numeric values.")
    st.stop()

# ---------------------------------------------------------
# SIDEBAR FILTERS
# ---------------------------------------------------------
st.sidebar.markdown("### Dashboard filters")

cities = ["All"] + sorted(df["city"].astype(str).unique().tolist())
selected_city = st.sidebar.selectbox("City", cities)

available_categories = sorted(df["category"].astype(str).unique().tolist())
selected_categories = st.sidebar.multiselect(
    "Product categories",
    available_categories,
    default=available_categories,
)

date_min = df["transaction_date"].min().date()
date_max = df["transaction_date"].max().date()

selected_dates = st.sidebar.date_input(
    "Transaction period",
    value=(date_min, date_max),
    min_value=date_min,
    max_value=date_max,
)

filtered = df[df["category"].astype(str).isin(selected_categories)].copy()

if selected_city != "All":
    filtered = filtered[filtered["city"].astype(str) == selected_city]

if isinstance(selected_dates, (tuple, list)):
    if len(selected_dates) == 2:
        start_date, end_date = selected_dates
        filtered = filtered[
            filtered["transaction_date"].dt.date.between(start_date, end_date)
        ]
    elif len(selected_dates) == 1:
        filtered = filtered[
            filtered["transaction_date"].dt.date == selected_dates[0]
        ]
else:
    filtered = filtered[
        filtered["transaction_date"].dt.date == selected_dates
    ]

if filtered.empty:
    st.warning("No transactions match these filters. Change the city, category, or date selection.")
    st.stop()

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------
st.markdown('<div class="section-title">Business overview</div>', unsafe_allow_html=True)

total_revenue = filtered["total_amount"].sum()
total_orders = filtered["transaction_id"].nunique()
total_customers = filtered["customer_id"].nunique()
average_order_value = total_revenue / total_orders if total_orders else 0

kpi_columns = st.columns(4)
kpis = [
    ("TOTAL REVENUE", f"₹{total_revenue:,.2f}", "Revenue in selected data"),
    ("TOTAL ORDERS", f"{total_orders:,}", "Unique transactions"),
    ("CUSTOMERS", f"{total_customers:,}", "Unique buyers"),
    ("AVERAGE ORDER", f"₹{average_order_value:,.2f}", "Revenue per transaction"),
]

for column, (label, value, note) in zip(kpi_columns, kpis):
    column.markdown(
        f"""
        <div class="metric">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ---------------------------------------------------------
# REVENUE CHARTS
# ---------------------------------------------------------
st.markdown('<div class="section-title">Revenue & buying behaviour</div>', unsafe_allow_html=True)

left, right = st.columns([1.35, 1])

monthly = (
    filtered.assign(month=filtered["transaction_date"].dt.to_period("M").astype(str))
    .groupby("month", as_index=False)["total_amount"]
    .sum()
)

monthly_fig = px.area(
    monthly,
    x="month",
    y="total_amount",
    markers=True,
    title="Monthly revenue",
    color_discrete_sequence=["#8b9cff"],
)
monthly_fig.update_traces(fill="tozeroy", line_width=3)
monthly_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#dbe5f5",
    margin=dict(l=10, r=10, t=50, b=10),
    xaxis_title="",
    yaxis_title="Revenue (₹)",
)
left.plotly_chart(monthly_fig, use_container_width=True)

category_sales = (
    filtered.groupby("category", as_index=False)["total_amount"]
    .sum()
    .sort_values("total_amount", ascending=False)
)

category_fig = px.pie(
    category_sales,
    names="category",
    values="total_amount",
    hole=0.62,
    title="Revenue by category",
    color_discrete_sequence=["#8b9cff", "#55d6be", "#ffbd69", "#ed8ca8", "#b79ced"],
)
category_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="#dbe5f5",
    margin=dict(l=10, r=10, t=50, b=10),
    legend_title="",
)
category_fig.update_traces(textposition="inside", textinfo="percent")
right.plotly_chart(category_fig, use_container_width=True)

# ---------------------------------------------------------
# PRODUCT AND CITY INSIGHTS
# ---------------------------------------------------------
st.markdown('<div class="section-title">Product & location insights</div>', unsafe_allow_html=True)

left, right = st.columns(2)

top_products = (
    filtered.groupby("product_name", as_index=False)
    .agg(units_sold=("quantity", "sum"), revenue=("total_amount", "sum"))
    .sort_values("revenue", ascending=False)
    .head(10)
    .sort_values("revenue", ascending=True)
)

product_fig = px.bar(
    top_products,
    x="revenue",
    y="product_name",
    orientation="h",
    title="Top products by revenue",
    color="revenue",
    color_continuous_scale=["#34466e", "#8b9cff"],
)
product_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#dbe5f5",
    margin=dict(l=10, r=10, t=50, b=10),
    xaxis_title="Revenue (₹)",
    yaxis_title="",
    coloraxis_showscale=False,
)
left.plotly_chart(product_fig, use_container_width=True)

city_sales = (
    filtered.groupby("city", as_index=False)["total_amount"]
    .sum()
    .sort_values("total_amount", ascending=False)
)

city_fig = px.bar(
    city_sales,
    x="city",
    y="total_amount",
    title="Revenue by city",
    color_discrete_sequence=["#55d6be"],
)
city_fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="#dbe5f5",
    margin=dict(l=10, r=10, t=50, b=10),
    xaxis_title="",
    yaxis_title="Revenue (₹)",
)
right.plotly_chart(city_fig, use_container_width=True)

# ---------------------------------------------------------
# TRANSACTION TABLE AND EXPORT
# ---------------------------------------------------------
st.markdown('<div class="section-title">Transaction explorer</div>', unsafe_allow_html=True)

search_text = st.text_input(
    "Search product or customer",
    placeholder="Enter a product name or customer ID",
)

transaction_view = filtered.copy()

if search_text.strip():
    search_mask = (
        transaction_view["product_name"].astype(str).str.contains(
            search_text, case=False, na=False
        )
        | transaction_view["customer_id"].astype(str).str.contains(
            search_text, case=False, na=False
        )
    )
    transaction_view = transaction_view[search_mask]

st.caption(f"Showing {len(transaction_view):,} transaction rows")
st.dataframe(
    transaction_view.sort_values("transaction_date", ascending=False),
    use_container_width=True,
    hide_index=True,
)

st.download_button(
    label="Download filtered transactions",
    data=transaction_view.to_csv(index=False).encode("utf-8"),
    file_name="filtered_customer_transactions.csv",
    mime="text/csv",
)

st.markdown("---")
st.caption(
    "PIGMENT | Customer Purchase Intelligence | Academic Project Demo "
    "| Streamlit dashboard with CSV upload"
)
