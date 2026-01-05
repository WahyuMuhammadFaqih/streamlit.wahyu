import pandas as pd
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency

# =========================
# HELPER FUNCTIONS
# =========================
def create_daily_orders_df(df):
    daily_orders_df = df.resample("D", on="order_date").agg({
        "order_id": "nunique",
        "total_price": "sum"
    }).reset_index()

    daily_orders_df.rename(columns={
        "order_id": "order_count",
        "total_price": "revenue"
    }, inplace=True)

    return daily_orders_df


def create_sum_order_items_df(df):
    return (
        df.groupby("product_name")
        .quantity_x.sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def create_bygender_df(df):
    return (
        df.groupby("gender")
        .customer_id.nunique()
        .reset_index(name="customer_count")
    )


def create_byage_df(df):
    byage_df = (
        df.groupby("age_group")
        .customer_id.nunique()
        .reset_index(name="customer_count")
    )
    byage_df["age_group"] = pd.Categorical(
        byage_df["age_group"],
        ["Youth", "Adults", "Seniors"],
        ordered=True
    )
    return byage_df


def create_bystate_df(df):
    return (
        df.groupby("state")
        .customer_id.nunique()
        .reset_index(name="customer_count")
    )


def create_rfm_df(df):
    rfm_df = df.groupby("customer_id", as_index=False).agg({
        "order_date": "max",
        "order_id": "nunique",
        "total_price": "sum"
    })

    rfm_df.columns = ["customer_id", "max_order_timestamp", "frequency", "monetary"]
    rfm_df["max_order_timestamp"] = rfm_df["max_order_timestamp"].dt.date

    recent_date = df["order_date"].dt.date.max()
    rfm_df["recency"] = rfm_df["max_order_timestamp"].apply(
        lambda x: (recent_date - x).days
    )

    return rfm_df.drop(columns="max_order_timestamp")


# =========================
# LOAD DATA
# =========================
all_df = pd.read_csv("tugas_13/all_data.csv")

for col in ["order_date", "delivery_date"]:
    all_df[col] = pd.to_datetime(all_df[col])

all_df.sort_values("order_date", inplace=True)

# =========================
# SIDEBAR
# =========================
min_date = all_df["order_date"].min().date()
max_date = all_df["order_date"].max().date()

with st.sidebar:
    st.image(
        "https://raw.githubusercontent.com/mhvvn/dashboard_streamlit/refs/heads/main/img/tshirt.png",
        width=80
    )
    start_date, end_date = st.date_input(
        "Rentang Waktu",
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )

# =========================
# FILTER DATA
# =========================
main_df = all_df[
    (all_df["order_date"].dt.date >= start_date) &
    (all_df["order_date"].dt.date <= end_date)
]

# =========================
# PREPARE DATA
# =========================
daily_orders_df = create_daily_orders_df(main_df)
sum_order_items_df = create_sum_order_items_df(main_df)
bygender_df = create_bygender_df(main_df)
byage_df = create_byage_df(main_df)
bystate_df = create_bystate_df(main_df)
rfm_df = create_rfm_df(main_df)

# =========================
# DASHBOARD
# =========================
st.header("My Collection Dashboard ✨")

# ===== Daily Orders =====
st.subheader("Daily Orders")

col1, col2 = st.columns(2)
col1.metric("Total Orders", daily_orders_df.order_count.sum())
col2.metric(
    "Total Revenue",
    format_currency(daily_orders_df.revenue.sum(), "AUD", locale="es_CO")
)

fig = px.line(
    daily_orders_df,
    x="order_date",
    y="order_count",
    markers=True,
    title="Daily Order Trend"
)
st.plotly_chart(fig, use_container_width=True)

# ===== Best & Worst Products =====
st.subheader("Best & Worst Performing Product")

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        sum_order_items_df.head(5),
        x="quantity_x",
        y="product_name",
        orientation="h",
        title="Best Performing Product"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        sum_order_items_df.sort_values("quantity_x").head(5),
        x="quantity_x",
        y="product_name",
        orientation="h",
        title="Worst Performing Product"
    )
    fig.update_layout(xaxis_autorange="reversed")
    st.plotly_chart(fig, use_container_width=True)

# ===== Customer Demographics =====
st.subheader("Customer Demographics")

col1, col2 = st.columns(2)

with col1:
    fig = px.bar(
        bygender_df,
        x="gender",
        y="customer_count",
        title="Customer by Gender"
    )
    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        byage_df,
        x="age_group",
        y="customer_count",
        title="Customer by Age Group"
    )
    st.plotly_chart(fig, use_container_width=True)

fig = px.bar(
    bystate_df.sort_values("customer_count", ascending=False),
    x="customer_count",
    y="state",
    title="Customer by State",
    orientation="h"
)
st.plotly_chart(fig, use_container_width=True)

# ===== RFM =====
st.subheader("Best Customer Based on RFM Parameters")

col1, col2, col3 = st.columns(3)
col1.metric("Avg Recency (days)", round(rfm_df.recency.mean(), 1))
col2.metric("Avg Frequency", round(rfm_df.frequency.mean(), 2))
col3.metric(
    "Avg Monetary",
    format_currency(rfm_df.monetary.mean(), "AUD", locale="es_CO")
)

col1, col2, col3 = st.columns(3)

col1.plotly_chart(
    px.bar(
        rfm_df.sort_values("recency").head(5),
        x="customer_id",
        y="recency",
        title="By Recency"
    ),
    use_container_width=True
)

col2.plotly_chart(
    px.bar(
        rfm_df.sort_values("frequency", ascending=False).head(5),
        x="customer_id",
        y="frequency",
        title="By Frequency"
    ),
    use_container_width=True
)

col3.plotly_chart(
    px.bar(
        rfm_df.sort_values("monetary", ascending=False).head(5),
        x="customer_id",
        y="monetary",
        title="By Monetary"
    ),
    use_container_width=True
)

st.caption("© My Collection 2025")
