import streamlit as st
import pandas as pd
import plotly.express as px
import requests
import json
import os

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------

st.set_page_config(
    page_title="PerfumeIQ AI",
    page_icon="🌸",
    layout="wide"
)

# ---------------------------------------------------
# LUXURY UI STYLING
# ---------------------------------------------------

st.markdown(
    """
    <style>

    .stApp {
        background-color: #0f0f0f;
        color: white;
    }

    h1, h2, h3, h4 {
        color: #f5c542;
    }

    .stButton>button {
        background-color: #f5c542;
        color: black;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        padding: 10px 20px;
    }

    .stButton>button:hover {
        background-color: white;
        color: black;
    }

    .stMetric {
        background-color: #1c1c1c;
        padding: 15px;
        border-radius: 12px;
    }

    .stDataFrame {
        background-color: #1c1c1c;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------

df = pd.read_csv("perfume_sales.csv")

pricing_df = pd.read_excel(
    "perfume_pricing_analysis_updated.xlsx"
)

inventory_df = pd.read_csv(
    "inventory.csv"
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

# ---------------------------------------------------
# BUSINESS METRICS
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

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

st.sidebar.title("🌸 PerfumeIQ AI")

page = st.sidebar.radio(
    "Navigate",
    [
        "Customer Dashboard",
        "Wholesale Pricing",
        "AI Assistant",
        "Admin Dashboard"
    ]
)

# ---------------------------------------------------
# CUSTOMER DASHBOARD
# ---------------------------------------------------

if page == "Customer Dashboard":

    st.markdown(
        """
        <div style="
            background: linear-gradient(
                to right,
                #1a1a1a,
                #2d2d2d
            );
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 30px;
        ">

        <h1 style="
            color:#f5c542;
            font-size:50px;
        ">
            🌸 PerfumeIQ AI
        </h1>

        <h3 style="
            color:white;
        ">
            AI-Powered Luxury Fragrance Intelligence Platform
        </h3>

        <p style="
            color:#cccccc;
            font-size:18px;
        ">
            Discover personalized perfumes,
            intelligent recommendations,
            wholesale deals, and luxury fragrance insights.
        </p>

        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns(2)

    col1.metric(
        "🏆 Best Seller",
        best_perfume
    )

    col2.metric(
        "🛒 Units Sold",
        total_sales
    )

    st.markdown("---")

    # -----------------------------------------------
    # SMART SEARCH ENGINE
    # -----------------------------------------------

    st.write("## 🔎 Smart Perfume Search")

    search_term = st.text_input(
        "Search Perfume Name"
    )

    selected_note_filter = st.selectbox(
        "Filter by Fragrance Note",
        ["All"] +
        sorted(
            df["Preferred_Notes"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    selected_gender_filter = st.selectbox(
        "Filter by Gender",
        ["All"] +
        sorted(
            df["Gender_Target"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    selected_budget_filter = st.selectbox(
        "Filter by Budget",
        ["All"] +
        sorted(
            df["Budget_Level"]
            .dropna()
            .unique()
            .tolist()
        )
    )

    search_df = df.copy()

    if search_term:

        search_df = search_df[
            search_df["Perfume_Name"]
            .str.contains(
                search_term,
                case=False,
                na=False
            )
        ]

    if selected_note_filter != "All":

        search_df = search_df[
            search_df["Preferred_Notes"] ==
            selected_note_filter
        ]

    if selected_gender_filter != "All":

        search_df = search_df[
            search_df["Gender_Target"] ==
            selected_gender_filter
        ]

    if selected_budget_filter != "All":

        search_df = search_df[
            search_df["Budget_Level"] ==
            selected_budget_filter
        ]

    st.write("## 🌸 Search Results")

    results = (
        search_df["Perfume_Name"]
        .drop_duplicates()
        .tolist()
    )

    if results:

        cols = st.columns(3)

        for idx, perfume in enumerate(results[:12]):

            with cols[idx % 3]:

                perfume_data = search_df[
                    search_df["Perfume_Name"] == perfume
                ].iloc[0]

                image_name = (
                    perfume.replace(" ", "_")
                    .upper() + ".jpg"
                )

                image_path = os.path.join(
                    "images",
                    image_name
                )

                if os.path.exists(image_path):

                    st.image(
                        image_path,
                        use_container_width=True
                    )

                st.markdown(
                    f"""
                    <div style="
                        background-color:#1c1c1c;
                        padding:15px;
                        border-radius:15px;
                        margin-bottom:15px;
                        text-align:center;
                        border:1px solid #f5c542;
                    ">

                    <h3 style="color:#f5c542;">
                        🌸 {perfume}
                    </h3>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write(
                    f"**Note:** {perfume_data['Preferred_Notes']}"
                )

                st.write(
                    f"**Budget:** {perfume_data['Budget_Level']}"
                )

                st.write(
                    f"**Gender:** {perfume_data['Gender_Target']}"
                )

    # -----------------------------------------------
    # RETAIL PRICING
    # -----------------------------------------------

    st.markdown("---")

    st.write("## 🛍️ Retail Pricing")

    customer_perfume = st.selectbox(
        "Choose Perfume",
        pricing_df["Fragrance_Name"].unique()
    )

    customer_size = st.selectbox(
        "Choose Bottle Size",
        pricing_df["Bottle_Size"].unique()
    )

    customer_price = pricing_df[
        (pricing_df["Fragrance_Name"] == customer_perfume) &
        (pricing_df["Bottle_Size"] == customer_size)
    ]

    if not customer_price.empty:

        row = customer_price.iloc[0]

        st.success(
            f"Retail Price: ₦{row['Retail_Selling_Price_N']:,.0f}"
        )

        # -----------------------------------------------
        # SHOPPING CART
        # -----------------------------------------------

        st.write("## 🛒 Shopping Cart")

        quantity = st.number_input(
            "Select Quantity",
            min_value=1,
            step=1
        )

        total_price = (
            row["Retail_Selling_Price_N"] *
            quantity
        )

        st.info(
            f"""
            Perfume: {customer_perfume}

            Bottle Size: {customer_size}

            Quantity: {quantity}

            Total Price: ₦{total_price:,.0f}
            """
        )

        customer_name = st.text_input(
            "Enter Your Name"
        )

        delivery_address = st.text_area(
            "Enter Delivery Address"
        )

        payment_method = st.selectbox(
            "Payment Method",
            [
                "Transfer",
                "Cash on Delivery",
                "Card Payment"
            ]
        )

        if st.button("Place Order"):

            order_data = pd.DataFrame({

                "Customer_Name": [customer_name],

                "Perfume": [customer_perfume],

                "Bottle_Size": [customer_size],

                "Quantity": [quantity],

                "Total_Price": [total_price],

                "Payment_Method": [payment_method]

            })

            inventory_df.loc[
                inventory_df["Perfume_Name"] ==
                customer_perfume,
                "Stock"
            ] -= quantity

            inventory_df.to_csv(
                "inventory.csv",
                index=False
            )

            order_data.to_csv(
                "orders.csv",
                mode="a",
                header=False,
                index=False
            )

            st.success(
                "🎉 Order placed successfully."
            )

# ---------------------------------------------------
# WHOLESALE PRICING
# ---------------------------------------------------

if page == "Wholesale Pricing":

    st.title("📦 Wholesale Pricing")

    bottle_size = st.selectbox(
        "Select Bottle Size",
        [
            "3ml",
            "6ml",
            "10ml",
            "12ml",
            "15ml",
            "20ml",
            "30ml",
            "50ml",
            "100ml"
        ]
    )

    quantity = st.number_input(
        "Enter Quantity",
        min_value=1
    )

    wholesale_prices = {
        "3ml": 407,
        "6ml": 800,
        "10ml": 1800,
        "12ml": 2000,
        "15ml": 2500,
        "20ml": 3000,
        "30ml": 4000,
        "50ml": 6500,
        "100ml": 12000
    }

    moq = {
        "3ml": 27,
        "6ml": 12,
        "10ml": 5,
        "12ml": 5,
        "15ml": 5,
        "20ml": 5,
        "30ml": 5,
        "50ml": 5,
        "100ml": 5
    }

    if quantity >= moq[bottle_size]:

        total = (
            wholesale_prices[bottle_size] *
            quantity
        )

        st.success(
            f"Wholesale Total: ₦{total:,.0f}"
        )

    else:

        st.warning(
            f"""
            Add {moq[bottle_size] - quantity}
            more bottles to qualify.
            """
        )

# ---------------------------------------------------
# AI ASSISTANT
# ---------------------------------------------------

if page == "AI Assistant":

    st.title("💬 PerfumeIQ AI Assistant")

    selected_gender = st.selectbox(
        "Select Gender",
        ["Male", "Female", "Unisex"]
    )

    selected_note = st.selectbox(
        "Select Preferred Fragrance Note",
        sorted(
            df["Preferred_Notes"]
            .dropna()
            .unique()
        )
    )

    selected_budget = st.selectbox(
        "Select Budget Level",
        ["Affordable", "Mid-Range", "Luxury"]
    )

    filtered_perfumes = df[
        (df["Gender_Target"] == selected_gender) &
        (df["Preferred_Notes"] == selected_note) &
        (df["Budget_Level"] == selected_budget)
    ]

    recommended_perfumes = (
        filtered_perfumes["Perfume_Name"]
        .drop_duplicates()
        .tolist()
    )

    # -----------------------------------------------
    # CUSTOMER PERSONA
    # -----------------------------------------------

    customer_persona = "General Fragrance Buyer"

    if (
        selected_note.lower() in
        ["oud", "woody", "amber"]
        and selected_budget == "Luxury"
    ):

        customer_persona = (
            "🖤 Luxury Oud Collector"
        )

    elif (
        selected_note.lower() in
        ["sweet", "vanilla", "floral"]
        and selected_budget == "Affordable"
    ):

        customer_persona = (
            "🌸 Sweet Fragrance Lover"
        )

    elif (
        selected_note.lower() in
        ["fresh", "aquatic", "citrus"]
        and selected_gender == "Male"
    ):

        customer_persona = (
            "❄️ Fresh Masculine Explorer"
        )

    st.success(customer_persona)

    # -----------------------------------------------
    # MATCH SCORE ENGINE
    # -----------------------------------------------

    perfume_scores = []

    for perfume in recommended_perfumes:

        perfume_data = filtered_perfumes[
            filtered_perfumes["Perfume_Name"] == perfume
        ].iloc[0]

        score = 0

        if (
            perfume_data["Preferred_Notes"] ==
            selected_note
        ):
            score += 40

        if (
            perfume_data["Gender_Target"] ==
            selected_gender
        ):
            score += 30

        if (
            perfume_data["Budget_Level"] ==
            selected_budget
        ):
            score += 30

        perfume_scores.append({

            "Perfume": perfume,

            "Score": score

        })

    perfume_scores = sorted(
        perfume_scores,
        key=lambda x: x["Score"],
        reverse=True
    )

    st.write("## 🌸 Recommended Perfumes")

    if perfume_scores:

        cols = st.columns(3)

        for idx, item in enumerate(perfume_scores):

            perfume = item["Perfume"]

            score = item["Score"]

            with cols[idx % 3]:

                perfume_data = filtered_perfumes[
                    filtered_perfumes["Perfume_Name"] == perfume
                ].iloc[0]

                image_name = (
                    perfume.replace(" ", "_")
                    .upper() + ".jpg"
                )

                image_path = os.path.join(
                    "images",
                    image_name
                )

                if os.path.exists(image_path):

                    st.image(
                        image_path,
                        use_container_width=True
                    )

                st.markdown(
                    f"""
                    <div style="
                        background-color:#1c1c1c;
                        padding:15px;
                        border-radius:15px;
                        margin-bottom:15px;
                        text-align:center;
                        border:1px solid #f5c542;
                    ">

                    <h3 style="color:#f5c542;">
                        🌸 {perfume}
                    </h3>

                    </div>
                    """,
                    unsafe_allow_html=True
                )

                st.write(
                    f"**Note:** {perfume_data['Preferred_Notes']}"
                )

                st.write(
                    f"**Budget:** {perfume_data['Budget_Level']}"
                )

                st.write(
                    f"**Gender:** {perfume_data['Gender_Target']}"
                )

                st.progress(score / 100)

                st.success(
                    f"⭐ AI Match Score: {score}%"
                )

                favorite_customer = st.text_input(
                    f"Enter Name for {perfume}",
                    key=f"fav_{perfume}"
                )

                if st.button(
                    f"❤️ Save {perfume}",
                    key=f"btn_{perfume}"
                ):

                    favorite_data = pd.DataFrame({

                        "Customer_Name": [
                            favorite_customer
                        ],

                        "Favorite_Perfume": [
                            perfume
                        ]

                    })

                    favorite_data.to_csv(
                        "favorites.csv",
                        mode="a",
                        header=False,
                        index=False
                    )

                    st.success(
                        f"{perfume} added to favorites."
                    )

# ---------------------------------------------------
# ADMIN DASHBOARD
# ---------------------------------------------------

if page == "Admin Dashboard":

    st.title("🔐 Admin Dashboard")

    admin_password = st.text_input(
        "Enter Admin Password",
        type="password"
    )

    if admin_password == "admin123":

        st.success("Admin Access Granted")

        # -------------------------------------------
        # AI INSIGHTS
        # -------------------------------------------

        st.write("## 🧠 AI Trend Insights")

        top_category = (
            df.groupby("Category")["Revenue"]
            .sum()
            .idxmax()
        )

        top_note = (
            df.groupby("Preferred_Notes")
            ["Qty_Sold (Pcs)"]
            .sum()
            .idxmax()
        )

        low_stock_count = len(
            inventory_df[
                inventory_df["Stock"] <= 20
            ]
        )

        st.info(
            f"📈 Highest Revenue Category: {top_category}"
        )

        st.success(
            f"🌸 Most Preferred Note: {top_note}"
        )

        st.error(
            f"⚠️ Low Stock Perfumes: {low_stock_count}"
        )

        # -------------------------------------------
        # METRICS
        # -------------------------------------------

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "💰 Revenue",
            f"₦{total_revenue:,.0f}"
        )

        col2.metric(
            "📈 Profit",
            f"₦{total_profit:,.0f}"
        )

        col3.metric(
            "🏆 Best Perfume",
            highest_perfume
        )

        # -------------------------------------------
        # FORECASTING
        # -------------------------------------------

        st.write("## 📈 Sales Forecasting")

        monthly_forecast = (
            df.groupby("Month")["Revenue"]
            .sum()
            .reset_index()
        )

        monthly_forecast["Predicted_Revenue"] = (
            monthly_forecast["Revenue"]
            .rolling(window=2)
            .mean()
        )

        fig_forecast = px.line(
            monthly_forecast,
            x="Month",
            y=[
                "Revenue",
                "Predicted_Revenue"
            ],
            markers=True
        )

        st.plotly_chart(
            fig_forecast,
            use_container_width=True
        )

        # -------------------------------------------
        # INVENTORY
        # -------------------------------------------

        st.write("## 📦 Inventory")

        st.dataframe(
            inventory_df,
            use_container_width=True
        )

        low_stock = inventory_df[
            inventory_df["Stock"] <= 20
        ]

        st.write("## ⚠️ Low Stock Alerts")

        if not low_stock.empty:

            for perfume in low_stock[
                "Perfume_Name"
            ]:

                st.warning(
                    f"{perfume} is running low."
                )

        # -------------------------------------------
        # FAVORITES
        # -------------------------------------------

        st.write("## ❤️ Customer Favorites")

        try:

            favorites_df = pd.read_csv(
                "favorites.csv"
            )

            st.dataframe(
                favorites_df,
                use_container_width=True
            )

        except:

            st.warning(
                "No favorites yet."
            )

        # -------------------------------------------
        # ORDERS
        # -------------------------------------------

        st.write("## 🧾 Customer Orders")

        try:

            orders_df = pd.read_csv(
                "orders.csv"
            )

            st.dataframe(
                orders_df,
                use_container_width=True
            )

        except:

            st.warning(
                "No orders yet."
            )

    else:

        st.warning(
            "Enter correct admin password."
        )

# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------

st.markdown("---")

st.caption(
    "PerfumeIQ AI © 2026"
)