import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# PAGE CONFIGURATION

st.set_page_config(
    page_title="Retail Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

# LOAD DATA

@st.cache_data

def load_data():
    df = pd.read_csv("cleaned_sales_data.csv")

    df['Date'] = pd.to_datetime(df['Date'])

    if 'DeliveryDate' in df.columns:
        df['DeliveryDate'] = pd.to_datetime(df['DeliveryDate'])

    if 'DeliveryTime' not in df.columns:
        df['DeliveryTime'] = (
            df['DeliveryDate'] - df['Date']
        ).dt.days

    if 'Quarter' not in df.columns:
        df['Quarter'] = df['Date'].dt.quarter

    return df


# Load dataframe

df = load_data()

# SIDEBAR FILTERS

st.sidebar.title("🔎 Dashboard Filters")

selected_region = st.sidebar.multiselect(
    "Select Region",
    options=df['Region'].unique(),
    default=df['Region'].unique()
)

selected_product = st.sidebar.multiselect(
    "Select Product",
    options=df['Product'].unique(),
    default=df['Product'].unique()
)

selected_customer = st.sidebar.multiselect(
    "Select Customer Type",
    options=df['CustomerType'].unique(),
    default=df['CustomerType'].unique()
)

selected_quarter = st.sidebar.multiselect(
    "Select Quarter",
    options=sorted(df['Quarter'].unique()),
    default=sorted(df['Quarter'].unique())
)

# FILTER DATA

filtered_df = df[
    (df['Region'].isin(selected_region)) &
    (df['Product'].isin(selected_product)) &
    (df['CustomerType'].isin(selected_customer)) &
    (df['Quarter'].isin(selected_quarter))
]

# DASHBOARD TITLE

st.title("📊 AI-Powered Retail Analytics Dashboard")

st.markdown(
    """
    Interactive business intelligence dashboard for retail sales analysis,
    customer insights, and operational performance.
    """
)

# KPI SECTION

st.subheader("📌 Key Performance Indicators")

# KPI Calculations

total_revenue = filtered_df['Revenue'].sum()

total_orders = len(filtered_df)

average_order_value = filtered_df['Revenue'].mean()

return_rate = filtered_df['Returned'].mean() * 100

best_product = (
    filtered_df.groupby('Product')['Revenue']
    .sum()
    .idxmax()
)

best_region = (
    filtered_df.groupby('Region')['Revenue']
    .sum()
    .idxmax()
)

# KPI Layout

col1, col2, col3 = st.columns(3)

col4, col5, col6 = st.columns(3)

col1.metric(
    "💰 Total Revenue",
    f"₹{total_revenue:,.0f}"
)

col2.metric(
    "🛒 Total Orders",
    total_orders
)

col3.metric(
    "📦 Avg Order Value",
    f"₹{average_order_value:,.0f}"
)

col4.metric(
    "⚠ Return Rate",
    f"{return_rate:.2f}%"
)

col5.metric(
    "🏆 Top Product",
    best_product
)

col6.metric(
    "🌍 Best Region",
    best_region
)

# TABS SECTION

tab1, tab2, tab3, tab4 = st.tabs([
    "Overview",
    "Product Analysis",
    "Regional Analysis",
    "Business Insights"
])

# TAB 1 — OVERVIEW

with tab1:

    st.subheader("📈 Revenue Trend")

    weekly_sales = (
        filtered_df
        .resample('W', on='Date')['Revenue']
        .sum()
        .reset_index()
    )

    fig = px.line(
    weekly_sales,
    x='Date',
    y='Revenue',
    markers=True,
    title='Weekly Revenue Trend'
    )

    st.plotly_chart(fig, use_container_width=True)

    # -------------------------------------------------

    st.subheader("💳 Payment Method Distribution")

    payment_data = (
        filtered_df.groupby('PaymentMethod')['Revenue']
        .sum()
        .reset_index()
    )

    fig2 = px.pie(
        payment_data,
        names='PaymentMethod',
        values='Revenue',
        title='Revenue by Payment Method'
    )

    st.plotly_chart(fig2, use_container_width=True)

    # -------------------------------------------------

    st.subheader("📅 Monthly Revenue Trend")

    filtered_df['month_name'] = filtered_df['Date'].dt.strftime('%b')

    monthly_sales = (
        filtered_df.groupby('month_name')['Revenue']
        .sum()
        .reset_index()
    )

    fig_month = px.line(
        monthly_sales,
        x='month_name',
        y='Revenue',
        markers=True,
        title='Monthly Revenue Trend'
    )

    st.plotly_chart(fig_month, use_container_width=True)

    # -------------------------------------------------

    st.subheader("🛍 Customer Type Revenue Distribution")

    customer_data = (
        filtered_df.groupby('CustomerType')['Revenue']
        .sum()
        .reset_index()
    )

    fig_customer = px.pie(
        customer_data,
        names='CustomerType',
        values='Revenue',
        title='Revenue by Customer Type'
    )

    st.plotly_chart(fig_customer, use_container_width=True)

# TAB 2 — PRODUCT ANALYSIS

with tab2:

    st.subheader("📦 Product Revenue Analysis")

    product_sales = (
        filtered_df.groupby('Product')['Revenue']
        .sum()
        .reset_index()
        .sort_values(by='Revenue', ascending=False)
    )

    fig3 = px.bar(
        product_sales,
        x='Product',
        y='Revenue',
        title='Revenue by Product'
    )

    st.plotly_chart(fig3, use_container_width=True)

    # -------------------------------------------------

    st.subheader("⚠ Product Return Rate")

    return_data = (
        filtered_df.groupby('Product')['Returned']
        .mean()
        .reset_index()
        .sort_values(by='Returned', ascending=False)
    )

    fig4 = px.bar(
        return_data,
        x='Product',
        y='Returned',
        title='Return Rate by Product'
    )

    st.plotly_chart(fig4, use_container_width=True)

    # -------------------------------------------------

    st.subheader("📊 Quantity Sold by Product")

    quantity_data = (
        filtered_df.groupby('Product')['Quantity']
        .sum()
        .reset_index()
        .sort_values(by='Quantity', ascending=False)
    )

    fig_quantity = px.bar(
        quantity_data,
        x='Product',
        y='Quantity',
        title='Quantity Sold by Product'
    )

    st.plotly_chart(fig_quantity, use_container_width=True)

    # -------------------------------------------------

    st.subheader("🎯 Promotion Impact on Product Revenue")

    promotion_data = (
        filtered_df.groupby(['Promotion', 'Product'])['Revenue']
        .sum()
        .reset_index()
    )

    fig_promo = px.bar(
        promotion_data,
        x='Promotion',
        y='Revenue',
        color='Product',
        barmode='group',
        title='Promotion Impact on Product Revenue'
    )

    st.plotly_chart(fig_promo, use_container_width=True)

# TAB 3 — REGIONAL ANALYSIS

with tab3:

    st.subheader("🌍 Revenue by Region")

    region_sales = (
        filtered_df.groupby('Region')['Revenue']
        .sum()
        .reset_index()
        .sort_values(by='Revenue', ascending=False)
    )

    fig5 = px.bar(
        region_sales,
        x='Region',
        y='Revenue',
        title='Revenue by Region'
    )

    st.plotly_chart(fig5, use_container_width=True)

    # -------------------------------------------------

    st.subheader("🔥 Region vs Product Heatmap")

    heatmap_data = filtered_df.pivot_table(
        values='Revenue',
        index='Region',
        columns='Product',
        aggfunc='sum'
    )

    fig6 = px.imshow(
        heatmap_data,
        text_auto=True,
        aspect='auto',
        title='Region vs Product Revenue Heatmap'
    )

    st.plotly_chart(fig6, use_container_width=True)

    # -------------------------------------------------

    st.subheader("🏬 Store Revenue Comparison")

    store_region = (
        filtered_df.groupby(['Region', 'StoreLocation'])['Revenue']
        .sum()
        .reset_index()
    )

    fig_store = px.bar(
        store_region,
        x='Region',
        y='Revenue',
        color='StoreLocation',
        barmode='group',
        title='Store Revenue Comparison by Region'
    )

    st.plotly_chart(fig_store, use_container_width=True)

    # -------------------------------------------------

    st.subheader("🚚 Average Delivery Time by Region")

    delivery_region = (
        filtered_df.groupby('Region')['DeliveryTime']
        .mean()
        .reset_index()
    )

    fig_delivery = px.bar(
        delivery_region,
        x='Region',
        y='DeliveryTime',
        title='Average Delivery Time by Region'
    )

    st.plotly_chart(fig_delivery, use_container_width=True)

# TAB 4 — BUSINESS INSIGHTS

with tab4:

    st.subheader("🧠 Automated Business Insights")

    top_region = (
        filtered_df.groupby('Region')['Revenue']
        .sum()
        .idxmax()
    )

    top_product = (
        filtered_df.groupby('Product')['Revenue']
        .sum()
        .idxmax()
    )

    high_return_product = (
        filtered_df.groupby('Product')['Returned']
        .mean()
        .idxmax()
    )

    underperforming_store = (
        filtered_df.groupby('StoreLocation')['Revenue']
        .sum()
        .idxmin()
    )

    avg_delivery = filtered_df['DeliveryTime'].mean()

    st.info(
        f"""
        📌 Top Revenue Region: {top_region}

        📌 Best Performing Product: {top_product}

        ⚠ Highest Return Product: {high_return_product}

        📉 Underperforming Store: {underperforming_store}

        🚚 Average Delivery Time: {avg_delivery:.2f} days
        """
    )

    # -------------------------------------------------

    st.subheader("🏬 Store Performance")

    store_sales = (
        filtered_df.groupby('StoreLocation')['Revenue']
        .sum()
        .reset_index()
        .sort_values(by='Revenue', ascending=False)
    )

    fig7 = px.bar(
        store_sales,
        x='StoreLocation',
        y='Revenue',
        title='Revenue by Store'
    )

    st.plotly_chart(fig7, use_container_width=True)

    # -------------------------------------------------

    st.subheader("📉 Return Rate by Region")

    return_region = (
        filtered_df.groupby('Region')['Returned']
        .mean()
        .reset_index()
    )

    fig_return_region = px.bar(
        return_region,
        x='Region',
        y='Returned',
        title='Return Rate by Region'
    )

    st.plotly_chart(fig_return_region, use_container_width=True)

    # -------------------------------------------------

    st.subheader("🎁 Promotion Performance")

    promo_performance = (
        filtered_df.groupby('Promotion')['Revenue']
        .sum()
        .reset_index()
    )

    fig_promo_perf = px.pie(
        promo_performance,
        names='Promotion',
        values='Revenue',
        title='Promotion Contribution to Revenue'
    )

    st.plotly_chart(fig_promo_perf, use_container_width=True)

    # -------------------------------------------------

    st.subheader("📦 Quarterly Product Demand")

    quarter_product = (
        filtered_df.groupby(['Quarter', 'Product'])['Quantity']
        .sum()
        .reset_index()
    )

    fig_quarter = px.line(
        quarter_product,
        x='Quarter',
        y='Quantity',
        color='Product',
        markers=True,
        title='Quarterly Product Demand'
    )

    st.plotly_chart(fig_quarter, use_container_width=True)

st.markdown("---")

st.markdown(
    "Developed using Streamlit, Plotly, Pandas, and Prophet"
)