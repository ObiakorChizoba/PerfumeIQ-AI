import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="PerfumeIQ AI",
    page_icon="🌸",
    layout="wide"
)

# ---------------------------------------------------
# TITLE
# ---------------------------------------------------

st.title("🌸 PerfumeIQ AI")
st.subheader("AI-Powered Personalized Fragrance Recommendation Agent")

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv("perfume_sales.csv")

pricing_df = pd.read_excel(
    "perfume_pricing_analysis_updated.xlsx"
)

# ---------------------------------------------------
# CLEAN DATA
# ---------------------------------------------------

df["Sales_Type"] = (
    df["Sales_Type"]
    .astype(str)
    .str.strip()
    .str.title()
)

df["Month"] = df["Date"]

# ---------------------------------------------------
# CALCULATIONS
# ---------------------------------------------------

df["Revenue"] = (
    df["Selling_Price (N)"] *
    df["Qty_Sold (Pcs)"]
)

df["Total_Cost"] = (
    df["Cost_Price (N)"] *
    df["Qty_Sold (Pcs)"]
)

df["Profit"] = (
    df["Revenue"] -
    df["Total_Cost"]
)

df["Profit_Margin"] = (
    df["Profit"] / df["Revenue"]
) * 100

# ---------------------------------------------------
# DATA PREVIEW
# ---------------------------------------------------

with st.expander("📂 View Dataset"):
    st.dataframe(df.head())

# ---------------------------------------------------
# KPI SECTION
# ---------------------------------------------------

total_revenue = df["Revenue"].sum()
total_profit = df["Profit"].sum()
total_sales = df["Qty_Sold (Pcs)"].sum()

best_perfume = (
    df.groupby("Perfume_Name")["Qty_Sold (Pcs)"]
    .sum()
    .idxmax()
)

highest_category = (
    df.groupby("Category")["Revenue"]
    .sum()
    .idxmax()
)

highest_perfume = (
    df.groupby("Perfume_Name")["Profit"]
    .sum()
    .idxmax()
)

lowest_perfume = (
    df.groupby("Perfume_Name")["Qty_Sold (Pcs)"]
    .sum()
    .idxmin()
)

profit_margin_avg = df["Profit_Margin"].mean()

if profit_margin_avg >= 50:
    health_score = "Excellent 🟢"
elif profit_margin_avg >= 30:
    health_score = "Good 🟡"
else:
    health_score = "Needs Attention 🔴"

# ---------------------------------------------------
# KPI DISPLAY
# ---------------------------------------------------

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "💰 Total Revenue",
    f"₦{total_revenue:,.0f}"
)

col2.metric(
    "📈 Total Profit",
    f"₦{total_profit:,.0f}"
)

col3.metric(
    "🛒 Units Sold",
    total_sales
)

col4.metric(
    "🏆 Best Seller",
    best_perfume
)

col5.metric(
    "💚 Business Health",
    health_score
)

st.markdown("---")

# ---------------------------------------------------
# MONTHLY REVENUE TREND
# ---------------------------------------------------

st.write("## 📅 Monthly Revenue Trend")

monthly_sales = (
    df.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

fig1 = px.line(
    monthly_sales,
    x="Month",
    y="Revenue",
    markers=True,
    title="Monthly Revenue Trend"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ---------------------------------------------------
# MONTHLY PROFIT TREND
# ---------------------------------------------------

st.write("## 📈 Monthly Profit Trend")

monthly_profit = (
    df.groupby("Month")["Profit"]
    .sum()
    .reset_index()
)

fig2 = px.line(
    monthly_profit,
    x="Month",
    y="Profit",
    markers=True,
    title="Monthly Profit Trend"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# ---------------------------------------------------
# TOP SELLING PERFUMES
# ---------------------------------------------------

st.write("## 🌟 Top Selling Perfumes")

top_perfumes = (
    df.groupby("Perfume_Name")["Qty_Sold (Pcs)"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig3 = px.bar(
    top_perfumes,
    x="Perfume_Name",
    y="Qty_Sold (Pcs)",
    title="Top 10 Selling Perfumes"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# ---------------------------------------------------
# CATEGORY ANALYSIS
# ---------------------------------------------------

st.write("## 🧴 Revenue by Category")

category_sales = (
    df.groupby("Category")["Revenue"]
    .sum()
    .reset_index()
)

fig4 = px.pie(
    category_sales,
    names="Category",
    values="Revenue",
    title="Revenue Distribution by Category"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# ---------------------------------------------------
# SALES TYPE ANALYSIS
# ---------------------------------------------------

st.write("## 🏪 Sales Type Distribution")

sales_type = (
    df.groupby("Sales_Type")["Revenue"]
    .sum()
    .reset_index()
)

fig5 = px.pie(
    sales_type,
    names="Sales_Type",
    values="Revenue",
    title="Wholesale vs Retail Revenue"
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# ---------------------------------------------------
# TOP CUSTOMERS
# ---------------------------------------------------

st.write("## 👑 Top Customers")

top_customers = (
    df.groupby("Customer_Name")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig6 = px.bar(
    top_customers,
    x="Customer_Name",
    y="Revenue",
    title="Top Customers by Revenue"
)

st.plotly_chart(
    fig6,
    use_container_width=True
)

# ---------------------------------------------------
# CUSTOMER PREFERENCE INSIGHTS
# ---------------------------------------------------

st.write("## 🧠 Customer Preference Insights")

top_notes = (
    df.groupby("Preferred_Notes")["Qty_Sold (Pcs)"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.info(
    f"🔥 Most popular fragrance note: {top_notes.index[0]}"
)

top_budget = (
    df.groupby("Budget_Level")["Revenue"]
    .sum()
    .idxmax()
)

st.info(
    f"💰 Highest performing budget segment: {top_budget}"
)

# ---------------------------------------------------
# AI BUSINESS RECOMMENDATIONS
# ---------------------------------------------------

st.write("## 🤖 AI Business Recommendations")

st.success(
    f"✅ Focus more marketing on '{highest_category}' fragrances because they generate the highest revenue."
)

st.success(
    f"✅ '{highest_perfume}' is your most profitable perfume. Consider increasing inventory."
)

st.warning(
    f"⚠️ '{lowest_perfume}' has the lowest sales performance. Consider reducing stock or offering promotions."
)

# ---------------------------------------------------
# ADMIN PRICING INTELLIGENCE
# ---------------------------------------------------

st.markdown("---")

show_admin = st.checkbox(
    "🔐 Show Admin Pricing Intelligence"
)

if show_admin:

    st.write("## 💰 Internal Pricing Intelligence Dashboard")

    selected_perfume = st.selectbox(
        "Select Perfume",
        pricing_df["Fragrance_Name"].unique()
    )

    selected_size = st.selectbox(
        "Select Bottle Size",
        pricing_df["Bottle_Size"].unique()
    )

    filtered_price = pricing_df[
        (pricing_df["Fragrance_Name"] == selected_perfume) &
        (pricing_df["Bottle_Size"] == selected_size)
    ]

    if not filtered_price.empty:

        row = filtered_price.iloc[0]

        retail_profit = (
            row["Retail_Selling_Price_N"] -
            row["Original_Cost_Price_N"]
        )

        st.success(
            f"💎 Original Cost Price: ₦{row['Original_Cost_Price_N']:,.0f}"
        )

        st.info(
            f"🛍️ Retail Selling Price: ₦{row['Retail_Selling_Price_N']:,.0f}"
        )

        st.warning(
            f"📈 Estimated Retail Profit: ₦{retail_profit:,.0f}"
        )

        st.write("### 📦 Product Insights")

        st.write(
            f"""
            - Fragrance: {selected_perfume}
            - Bottle Size: {selected_size}
            - Bottle Cost: ₦{row['Bottle_Cost_N']:,.0f}
            - Fragrance Cost: ₦{row['Fragrance_Cost_Per_Bottle_N']:,.0f}
            """
        )

# ---------------------------------------------------
# CUSTOMER RETAIL PRICING
# ---------------------------------------------------

st.markdown("---")

st.write("## 🛍️ Retail Perfume Pricing")

customer_perfume = st.selectbox(
    "Choose a Perfume",
    pricing_df["Fragrance_Name"].unique(),
    key="customer_perfume"
)

customer_size = st.selectbox(
    "Choose Bottle Size",
    pricing_df["Bottle_Size"].unique(),
    key="customer_size"
)

customer_price = pricing_df[
    (pricing_df["Fragrance_Name"] == customer_perfume) &
    (pricing_df["Bottle_Size"] == customer_size)
]

if not customer_price.empty:

    row = customer_price.iloc[0]

    st.success(
        f"✨ Retail Price: ₦{row['Retail_Selling_Price_N']:,.0f}"
    )

# ---------------------------------------------------
# AI CHATBOT
# ---------------------------------------------------

st.markdown("---")

st.write("## 💬 PerfumeIQ AI Assistant")

user_question = st.text_input(
    "Ask a perfume recommendation or business question:"
)

if user_question:

    available_perfumes = (
        df["Perfume_Name"]
        .dropna()
        .unique()
        .tolist()
    )

    perfume_notes = (
        df[[
            "Perfume_Name",
            "Preferred_Notes",
            "Budget_Level",
            "Gender_Target"
        ]]
        .drop_duplicates()
        .to_dict(orient="records")
    )

    business_summary = f"""
    Available Perfumes:
    {available_perfumes}

    Perfume Metadata:
    {perfume_notes}

    Business Statistics:
    Total Revenue: {total_revenue}
    Total Profit: {total_profit}
    Best Selling Perfume: {best_perfume}
    Highest Revenue Category: {highest_category}
    Most Profitable Perfume: {highest_perfume}
    Lowest Selling Perfume: {lowest_perfume}
    """

    prompt = f"""
    You are PerfumeIQ AI, an intelligent fragrance recommendation and perfume business assistant.

    Your responsibilities:
    - Recommend perfumes based on scent preferences
    - Suggest perfumes by gender and budget
    - Recommend alternatives and similar fragrances
    - Help customers discover fragrances they may like
    - Give business recommendations for perfume sales
    - Understand luxury, affordable, sweet, oud, floral, woody, and fresh fragrance profiles

    IMPORTANT RULES:
    - ONLY recommend perfumes from the provided Available Perfumes list
    - NEVER invent perfume names
    - NEVER recommend perfumes outside the dataset
    - Use the provided Perfume Metadata for reasoning
    - If a perfume is unavailable, suggest the closest available alternative
    - Keep recommendations personalized and conversational

    BUSINESS DATA:
    {business_summary}

    USER QUESTION:
    {user_question}

    Give a detailed but concise recommendation.
    """

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": "Bearer " + st.secrets["OPENROUTER_API_KEY"],
        "Content-Type": "application/json"
    }

    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(data)
    )

    result = response.json()

    try:

        if "choices" in result:

            ai_response = (
                result["choices"][0]
                ["message"]["content"]
            )

            st.write("## 🤖 AI Response")

            st.success(ai_response)

        else:

            st.error(
                "AI service temporarily unavailable."
            )

            st.write("API Response:")

            st.json(result)

    except Exception as e:

        st.error(
            f"Error generating response: {e}"
        )

        st.write("Full API Response:")

        st.json(result)

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "PerfumeIQ AI © 2026 | DSN X BCT LLM Agent Challenge"
)