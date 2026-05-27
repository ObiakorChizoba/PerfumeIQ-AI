import streamlit as st
import pandas as pd
import plotly.express as px
import os

# ===================================================
# PAGE CONFIG
# ===================================================

st.set_page_config(
    page_title="PerfumeIQ AI",
    page_icon="🌸",
    layout="wide"
)

# ===================================================
# MODERN LUXURY UI
# ===================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #f5f5f5;
        color: #1c1c1c;
    }

    h1, h2, h3, h4 {
        color: #8b5e3c;
        font-weight: bold;
    }

    p, label, div {
        color: #1c1c1c;
    }

    .stButton>button {
        background-color: #8b5e3c;
        color: white;
        border-radius: 10px;
        border: none;
        font-weight: bold;
        padding: 10px 20px;
    }

    .stButton>button:hover {
        background-color: #c49b66;
        color: white;
    }

    .stMetric {
        background-color: white;
        padding: 15px;
        border-radius: 12px;
        border: 1px solid #dddddd;
    }

    section[data-testid="stSidebar"] {
        background-color: #ede7df;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ===================================================
# LOAD DATA
# ===================================================

df = pd.read_csv("perfume_sales.csv")

pricing_df = pd.read_excel(
    "perfume_pricing_analysis_updated.xlsx"
)
# ===================================================
# PERFUME CATEGORIES
# ===================================================

sweet_perfumes = [

    "PINK SUGAR",
    "VANILLA",
    "CHOCOLATE MUSK",
    "STRAWBERRY",
    "SUGAR BABY",
    "COCONUT PASSION",
    "LOVE SPELL",
    "SWEET TEMPTATION",
    "ESCADA CHERRY",
    "PINK CHIFFON"

]

oud_perfumes = [

    "BLACK OUD",
    "OUD COLLECTION",
    "GUCCI OUD INTENSE",
    "WOOD OUD",
    "TUSCAN LEATHER",
    "OUD TOUCH",
    "AMOUAGE OUD",
    "OUD GOLD",
    "ROSE OUD",
    "PRINCESS OUD",
    "TOM OUD",
    "OUD MAN"

]

fresh_perfumes = [

    "COOL WATER",
    "BLUE LADY",
    "CHANNEL BLUE",
    "POLO SPORT",
    "PLAY BLUE",
    "212 AQUA",
    "CREED SILVER WATER",
    "BLUE WATER",
    "DAVID BACKUM"

]

luxury_perfumes = [

    "BACCARAT",
    "TOMFORD",
    "SAVAGE DIOR",
    "CREED AVENTUS",
    "BLACK ORCHID",
    "GOOD GIRL",
    "JADORE",
    "COCO MADEMOISELLE",
    "MON PARIS"

]

inventory_df = pd.read_csv(
    "inventory.csv"
)

# ===================================================
# CALCULATIONS
# ===================================================

df["Revenue"] = (
    df["Selling_Price (N)"] *
    df["Qty_Sold (Pcs)"]
)

df["Profit"] = (
    df["Revenue"] -
    (
        df["Cost_Price (N)"] *
        df["Qty_Sold (Pcs)"]
    )
)

total_revenue = df["Revenue"].sum()

total_profit = df["Profit"].sum()

best_perfume = (
    df.groupby("Perfume_Name")
    ["Qty_Sold (Pcs)"]
    .sum()
    .idxmax()
)

# ===================================================
# SIDEBAR
# ===================================================

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

# ===================================================
# CUSTOMER DASHBOARD
# ===================================================

if page == "Customer Dashboard":

    # =============================================
    # CREATE RETAIL CART SESSION
    # =============================================

    if "retail_cart" not in st.session_state:

        st.session_state.retail_cart = []

    st.markdown(
        """
        <div style="
            background: linear-gradient(
                to right,
                #d8c3a5,
                #ede7df
            );
            padding: 40px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 30px;
        ">

        <h1 style="
            color:#8b5e3c;
            font-size:50px;
        ">
            🌸 PerfumeIQ AI
        </h1>

        <h3 style="
            color:#1c1c1c;
        ">
            AI-Powered Luxury Fragrance Platform
        </h3>

        </div>
        """,
        unsafe_allow_html=True
    )

    # ===================================================
    # TOP 3 BEST SELLERS
    # ===================================================

    st.write("## 🏆 Top 3 Best Sellers")

    top_perfumes = (
        df.groupby("Perfume_Name")
        ["Qty_Sold (Pcs)"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .reset_index()
    )

    col1, col2, col3 = st.columns(3)

    positions = [
        "🥇 1st Place",
        "🥈 2nd Place",
        "🥉 3rd Place"
    ]

    columns = [col1, col2, col3]

    for idx, row in top_perfumes.iterrows():

        perfume = row["Perfume_Name"]

        qty = row["Qty_Sold (Pcs)"]

        with columns[idx]:

            st.markdown(
                f"""
                <div style="
                    background-color:white;
                    padding:20px;
                    border-radius:15px;
                    text-align:center;
                    border:2px solid #d8c3a5;
                    margin-bottom:10px;
                ">

                <h3 style="color:#8b5e3c;">
                    {positions[idx]}
                </h3>

                <h2 style="color:#1c1c1c;">
                    {perfume}
                </h2>

                <p style="
                    color:#555555;
                    font-size:18px;
                ">
                    {qty} units sold
                </p>

                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown("---")

    # ===================================================
    # SMART SEARCH
    # ===================================================

    st.write("## 🔎 Smart Perfume Search")

    search_term = st.text_input(
        "Search Perfume Name"
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

    perfumes = (
        search_df["Perfume_Name"]
        .drop_duplicates()
        .tolist()
    )

    cols = st.columns(3)

    for idx, perfume in enumerate(perfumes[:12]):

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
                    background-color:white;
                    padding:15px;
                    border-radius:15px;
                    text-align:center;
                    border:1px solid #d8c3a5;
                ">

                <h3 style="color:#8b5e3c;">
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

    st.markdown("---")

# ===================================================
# ORDER PERFUME
# ===================================================

st.write("## 🛒 Order Perfume")

    retail_perfume = st.selectbox(

        "Select Perfume",

        pricing_df[
            "Fragrance_Name"
        ].unique(),

        key="retail_perfume"

    )

    retail_size = st.selectbox(

        "Select Bottle Size",

        pricing_df[
            "Bottle_Size"
        ].unique(),

        key="retail_size"

    )

    retail_quantity = st.number_input(

        "Enter Quantity",

        min_value=1,
        step=1,

        key="retail_quantity"

    )

    # ===================================================
    # GET PRICE
    # ===================================================

    retail_match = pricing_df[

        (

            pricing_df[
                "Fragrance_Name"
            ]

            == retail_perfume

        )

        &

        (

            pricing_df[
                "Bottle_Size"
        ]

            == retail_size

        )

    ]

    if not retail_match.empty:

        retail_price = (

            retail_match[
                "Retail_Selling_Price_N"
            ]

            .values[0]

        )

    else:

        retail_price = 0

    retail_total_price = (

        retail_price *
        retail_quantity

    )

    st.success(
        f"""
        Total Price:
        ₦{retail_total_price:,.0f}
        """
    )

    # ===================================================
    # ADD TO CART
    # ===================================================

    if st.button(
        "Add To Retail Cart"
    ):

        st.session_state.retail_cart.append({

            "Perfume":
            retail_perfume,

            "Bottle_Size":
            retail_size,

            "Quantity":
            retail_quantity,

            "Total_Price":
            retail_total_price

        })

        st.success(
            "Added to retail cart."
        )



    # ===================================================
    # RETAIL CART
    # ===================================================

    if st.session_state.retail_cart:

        st.write("## 🧾 Retail Cart")

        retail_cart_df = pd.DataFrame(
            st.session_state.retail_cart
        )

        st.dataframe(
            retail_cart_df,
            use_container_width=True
        )

        # =============================================
        # CART TOTAL
        # =============================================

        retail_total = (
            retail_cart_df["Total_Price"]
            .sum()
        )

        # =============================================
        # CUSTOMER DETAILS
        # =============================================

        customer_name = st.text_input(
            "Customer Name"
        )

        payment_method = st.selectbox(

            "Payment Method",

            [
                "Transfer",
                "Cash on Delivery"
            ]

        )

        # =============================================
        # DELIVERY OPTION
        # =============================================

        delivery_option = st.radio(

            "Delivery Option",

            [
                "Pickup",
                "Delivery"
             ]

        )

        delivery_fee = 0

        delivery_address = ""

        if delivery_option == "Delivery":

            delivery_location = st.selectbox(

                "Select Delivery Area",

                [

                    "Peter Odili Road",
                    "Rumuola",
                    "Dline",
                    "Ozuoba",
                    "Choba"

                ]

            )

            delivery_fees = {

                "Peter Odili Road": 600,
                "Rumuola": 2000,
                "Dline": 1500,
                "Ozuoba": 4000,
                "Choba": 5000

            }

            delivery_fee = delivery_fees[
                delivery_location
            ]

            delivery_address = st.text_area(
                "Enter Delivery Address"
            )

            st.warning(
                f"""
                Delivery Fee:
                ₦{delivery_fee:,.0f}
                """
            )

        # =============================================
        # FINAL TOTAL
        # =============================================

        final_total = (
            retail_total +
            delivery_fee
        )

        st.success(
            f"""
            Final Total:
            ₦{final_total:,.0f}
            """
        )

        # =============================================
        # CHECKOUT BUTTON
        # =============================================

        if st.button("Checkout Retail Cart"):

            retail_cart_df[
                "Customer_Name"
            ] = customer_name

            retail_cart_df[
                "Payment_Method"
            ] = payment_method

            retail_cart_df[
                "Sales_Type"
            ] = "Retail"

            retail_cart_df[
                "Delivery_Option"
            ] = delivery_option

            retail_cart_df[
                "Delivery_Address"
            ] = delivery_address

            retail_cart_df[
                "Delivery_Fee"
            ] = delivery_fee

            # =========================================
            # REORDER COLUMNS
            # =========================================

            retail_cart_df = retail_cart_df[
                [
                    "Customer_Name",
                    "Perfume",
                    "Bottle_Size",
                    "Quantity",
                    "Total_Price",
                    "Payment_Method",
                    "Sales_Type",
                    "Delivery_Option",
                    "Delivery_Address",
                    "Delivery_Fee"
                ]
            ]

            retail_cart_df.columns = [

                "Customer_Name",
                "Perfume",
                "Bottle_Size",
                "Quantity",
                "Total_Price",
                "Payment_Method",
                "Sales_Type",
                "Delivery_Option",
                "Delivery_Address",
                "Delivery_Fee"

            ]

            # =========================================
            # SAVE ORDER
            # =========================================

            retail_cart_df.to_csv(
                "orders.csv",
                mode="a",
                header=False,
                index=False
            )

            # =========================================
            # UPDATE INVENTORY
            # =========================================

            for item in st.session_state.retail_cart:

                bottle_ml = int(
                    item["Bottle_Size"]
                    .replace("ml", "")
                )

                used_ml = (
                    bottle_ml *
                    item["Quantity"]
                )

                inventory_df.loc[
                    inventory_df["Perfume_Name"] ==
                    item["Perfume"],
                    "Stock"
                ] -= used_ml

            inventory_df.to_csv(
                "inventory.csv",
                index=False
            )

            # =========================================
            # SUCCESS MESSAGE
            # =========================================

            st.success(
                "✅ Retail order placed."
            )

            st.info(
                f"""
                Bank Name:
                {st.secrets["BANK_NAME"]}

                Account Number:
                {st.secrets["ACCOUNT_NUMBER"]}

                Account Name:
                {st.secrets["ACCOUNT_NAME"]}
                """
            )

            st.link_button(
                "📱 Send Proof on WhatsApp",
                f"https://wa.me/{st.secrets['WHATSAPP_NUMBER']}"
            )

            # =========================================
            # CLEAR CART
            # =========================================

            st.session_state.retail_cart = []

    st.markdown("---")


# ===================================================
# WHOLESALE PRICING
# ===================================================

if page == "Wholesale Pricing":

    st.title("📦 Wholesale Marketplace")

    # -------------------------------------------------
    # CREATE CART SESSION
    # -------------------------------------------------

    if "wholesale_cart" not in st.session_state:

        st.session_state.wholesale_cart = []

    # -------------------------------------------------
    # PRODUCT SELECTION
    # -------------------------------------------------

    wholesale_perfume = st.selectbox(
        "Select Perfume",
        pricing_df["Fragrance_Name"].unique(),
        key="wholesale_perfume"
    )

    wholesale_size = st.selectbox(
        "Select Bottle Size",
        pricing_df["Bottle_Size"].unique(),
        key="wholesale_size"
    )

    wholesale_quantity = st.number_input(
        "Enter Quantity",
        min_value=1,
        step=1,
        key="wholesale_quantity"
    )

    # -------------------------------------------------
    # MOQ RULES
    # -------------------------------------------------

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

    # -------------------------------------------------
    # GET PRICE
    # -------------------------------------------------

    wholesale_price_df = pricing_df[
        (pricing_df["Fragrance_Name"] ==
         wholesale_perfume) &

        (pricing_df["Bottle_Size"] ==
         wholesale_size)
    ]

    if not wholesale_price_df.empty:

        wholesale_row = (
            wholesale_price_df.iloc[0]
        )

        retail_price = (
            wholesale_row[
                "Retail_Selling_Price_N"
            ]
        )

        required_moq = moq.get(
            wholesale_size,
            5
        )

        # -------------------------------------------------
        # MOQ VALIDATION
        # -------------------------------------------------

        if wholesale_quantity >= required_moq:

            wholesale_price = (
                retail_price * 0.8
            )

            wholesale_total = (
                wholesale_price *
                wholesale_quantity
            )

            savings = (
                (retail_price *
                 wholesale_quantity)
                - wholesale_total
            )

            st.success(
                f"""
                MOQ Reached ✅

                Wholesale Total:
                ₦{wholesale_total:,.0f}

                Savings:
                ₦{savings:,.0f}
                """
            )

            # -------------------------------------------------
            # ADD TO CART
            # -------------------------------------------------

            if st.button(
                "Add To Wholesale Cart"
            ):

                st.session_state.wholesale_cart.append({

                    "Perfume":
                    wholesale_perfume,

                    "Bottle_Size":
                    wholesale_size,

                    "Quantity":
                    wholesale_quantity,

                    "Total_Price":
                    wholesale_total

                })

                st.success(
                    "✅ Added to wholesale cart."
                )

        else:

            remaining = (
                required_moq -
                wholesale_quantity
            )

            st.warning(
                f"""
                Add {remaining}
                more bottles
                to activate wholesale pricing.
                """
            )

            st.write("## 🧾 Wholesale Cart")

        wholesale_cart_df = pd.DataFrame(
            st.session_state.wholesale_cart
        )

        st.dataframe(
            wholesale_cart_df,
            use_container_width=True
        )

        wholesale_total = (
            wholesale_cart_df[
                "Total_Price"
            ].sum()
        )

        # =============================================
        # CUSTOMER INFO
        # =============================================

        wholesale_customer = st.text_input(
            "Business Name"
        )

        wholesale_payment = st.selectbox(

            "Payment Method",

            [
                "Transfer",
                "Corporate Payment",
                "Bank Deposit"
            ]

        )

        # =============================================
        # DELIVERY OPTION
        # =============================================

        wholesale_delivery_option = st.radio(

            "Delivery Option",

            [
                "Pickup",
                "Delivery"
            ],

            key="wholesale_delivery"

        )

        wholesale_delivery_fee = 0

        wholesale_delivery_address = ""

        if wholesale_delivery_option == "Delivery":

            wholesale_delivery_location = st.selectbox(

                "Select Delivery Area",

                [

                    "Peter Odili Road",
                    "Rumuola",
                    "Dline",
                    "Ozuoba",
                    "Choba"

                ],

                key="wholesale_location"

            )

            wholesale_delivery_fees = {

                "Peter Odili Road": 600,
                "Rumuola": 2000,
                "Dline": 1500,
                "Ozuoba": 4000,
                "Choba": 5000

            }

            wholesale_delivery_fee = (
                wholesale_delivery_fees[
                    wholesale_delivery_location
                ]
            )

            wholesale_delivery_address = st.text_area(
                "Enter Delivery Address",
                key="wholesale_address"
            )

            st.warning(
                f"""
                Delivery Fee:
                ₦{wholesale_delivery_fee:,.0f}
                """
            )

        # =============================================
        # FINAL TOTAL
        # =============================================

        wholesale_final_total = (

            wholesale_total +
            wholesale_delivery_fee

        )

        st.success(
            f"""
            Final Total:
            ₦{wholesale_final_total:,.0f}
            """
        )

        # =============================================
        # CHECKOUT
        # =============================================

        if st.button(
            "Checkout Wholesale Cart"
        ):

            wholesale_cart_df[
                "Customer_Name"
            ] = wholesale_customer

            wholesale_cart_df[
                "Payment_Method"
            ] = wholesale_payment

            wholesale_cart_df[
                "Sales_Type"
            ] = "Wholesale"

            wholesale_cart_df[
                "Delivery_Option"
            ] = wholesale_delivery_option

            wholesale_cart_df[
                "Delivery_Address"
            ] = wholesale_delivery_address

            wholesale_cart_df[
                "Delivery_Fee"
            ] = wholesale_delivery_fee

            # =========================================
            # COLUMN ORDER
            # =========================================

            wholesale_cart_df = wholesale_cart_df[
                [
                    "Customer_Name",
                    "Perfume",
                    "Bottle_Size",
                    "Quantity",
                    "Total_Price",
                    "Payment_Method",
                    "Sales_Type",
                    "Delivery_Option",
                    "Delivery_Address",
                    "Delivery_Fee"
                ]
            ]

            wholesale_cart_df.to_csv(
                "orders.csv",
                mode="a",
                header=False,
                index=False
            )

            # =========================================
            # INVENTORY UPDATE
            # =========================================

            for item in (
                st.session_state
                .wholesale_cart
            ):

                bottle_ml = int(
                    item["Bottle_Size"]
                    .replace("ml", "")
                )

                used_ml = (
                    bottle_ml *
                    item["Quantity"]
                )

                inventory_df.loc[
                    inventory_df["Perfume_Name"] ==
                    item["Perfume"],
                    "Stock"
                ] -= used_ml

            inventory_df.to_csv(
                "inventory.csv",
                index=False
            )

            st.success(
                "✅ Wholesale order placed."
            )

            st.info(
                f"""
                Bank Name:
                {st.secrets["BANK_NAME"]}

                Account Number:
                {st.secrets["ACCOUNT_NUMBER"]}

                Account Name:
                {st.secrets["ACCOUNT_NAME"]}
                """
            )

            st.link_button(
                "📱 Contact Wholesale Manager",
                f"https://wa.me/{st.secrets['WHATSAPP_NUMBER']}"
            )

            st.session_state.wholesale_cart = []

            # ---------------------------------------------
            # CLEAR CART
            # ---------------------------------------------

            st.session_state.wholesale_cart = []


# ===================================================
# AI ASSISTANT
# ===================================================

if page == "AI Assistant":

    st.title("🤖 AI Fragrance Assistant")

    preference = st.selectbox(

        "What fragrance profile do you prefer?",

        [

            "Sweet",
            "Oud",
            "Fresh",
            "Luxury",
            "Best Sellers"

        ]

    )

    # -------------------------------------------------
    # BEST SELLERS
    # -------------------------------------------------

    bestseller_perfumes = [

        "SUGAR BABY",
        "BACCARAT",
        "CREED AVENTUS",
        "GOOD GIRL",
        "BLACK OUD"

    ]

    # -------------------------------------------------
    # RECOMMENDATION LOGIC
    # -------------------------------------------------

    if preference == "Sweet":

        recommendations = sweet_perfumes

    elif preference == "Oud":

        recommendations = oud_perfumes

    elif preference == "Fresh":

        recommendations = fresh_perfumes

    elif preference == "Luxury":

        recommendations = luxury_perfumes

    else:

        recommendations = bestseller_perfumes

    # -------------------------------------------------
    # DISPLAY RECOMMENDATIONS
    # -------------------------------------------------

    st.write("## 🌸 AI Recommendations")

    cols = st.columns(5)

    for idx, perfume in enumerate(
        recommendations[:5]
    ):

        with cols[idx]:

            st.markdown(
                f"""
                <div style="
                    border:1px solid #d4a373;
                    border-radius:10px;
                    padding:10px;
                    text-align:center;
                    background-color:#fffaf3;
                ">

                <h4 style="
                    color:#9c6644;
                ">
                🌸 {perfume}
                </h4>

                </div>
                """,
                unsafe_allow_html=True
            )

            st.progress(85)

            st.success(
                "⭐ AI Match Score: 85%"
            )

            favorite_customer = st.text_input(
                f"Enter Name for {perfume}",
                key=f"fav_{perfume}_{idx}"
            )

            if st.button(
                f"❤️ Save {perfume}",
                key=f"btn_{perfume}_{idx}"
            ):

                favorite_data = pd.DataFrame([{

                    "Customer_Name":
                    favorite_customer,

                    "Favorite_Perfume":
                    perfume

                }])

                favorite_data.to_csv(
                    "favorites.csv",
                    mode="a",
                    header=False,
                    index=False
                )

                st.success(
                    "Saved Successfully!"
                )

# ===================================================
# ADMIN DASHBOARD
# ===================================================

if page == "Admin Dashboard":

    st.title("🔐 Admin Dashboard")

    admin_password = st.text_input(
        "Enter Admin Password",
        type="password"
    )

    if admin_password == "admin123":

        st.success("Admin Access Granted")
        # ===================================================
        # LIVE PRICE MANAGEMENT
        # ===================================================

        st.write("## 💰 Live Price Management")

        admin_perfume = st.selectbox(
            "Select Perfume",
            pricing_df["Fragrance_Name"].unique(),
            key="admin_perfume"
        )

        admin_size = st.selectbox(
            "Select Bottle Size",
            pricing_df["Bottle_Size"].unique(),
            key="admin_size"
        )

        admin_price_row = pricing_df[
            (pricing_df["Fragrance_Name"] ==
             admin_perfume) &

            (pricing_df["Bottle_Size"] ==
             admin_size)
        ]

        if not admin_price_row.empty:

            current_price = (
                admin_price_row.iloc[0]
                ["Retail_Selling_Price_N"]
            )

            st.info(
                f"""
                Current Price:
                ₦{current_price:,.0f}
                """
            )

            new_price = st.number_input(
                "Enter New Retail Price",
                min_value=0,
                value=int(current_price),
                key="new_price"
            )

            if st.button(
                "Update Retail Price"
            ):

                pricing_df.loc[
                    (pricing_df["Fragrance_Name"] ==
                     admin_perfume) &

                    (pricing_df["Bottle_Size"] ==
                     admin_size),

                    "Retail_Selling_Price_N"

                ] = new_price

                pricing_df.to_excel(
                    "perfume_pricing_analysis_updated.xlsx",
                    index=False
                )

                st.success(
                    f"""
                    ✅ Price updated to
                    ₦{new_price:,.0f}
                    """
                )

        # ===================================================
        # SALES TYPE ANALYSIS
        # ===================================================

        st.write(
            "## 📊 Retail vs Wholesale Analysis"
        )

        try:

            orders_df = pd.read_csv(
                "orders.csv"
            )

            sales_summary = (
                orders_df.groupby(
                    "Sales_Type"
                )["Total_Price"]
                .sum()
                .reset_index()
            )

            fig_sales = px.pie(
                sales_summary,
                names="Sales_Type",
                values="Total_Price",
                title="Retail vs Wholesale Revenue"
            )

            st.plotly_chart(
                fig_sales,
                use_container_width=True
            )

        except:

            st.warning(
                "No sales data yet."
            )


        # ===================================================
        # ADMIN METRICS
        # ===================================================

        col1, col2 = st.columns(2)

        col1.metric(
            "💰 Total Revenue",
            f"₦{total_revenue:,.0f}"
        )

        col2.metric(
            "📈 Total Profit",
            f"₦{total_profit:,.0f}"
        )
        # ===================================================
        # FORECASTING
        # ===================================================

        st.write("## 📈 Sales Forecasting")

        monthly_forecast = (
            df.groupby("Date")["Revenue"]
            .sum()
            .reset_index()
        )

        monthly_forecast[
            "Predicted_Revenue"
        ] = (
            monthly_forecast["Revenue"]
            .rolling(window=2)
            .mean()
        )

        fig_forecast = px.line(
            monthly_forecast,
            x="Date",
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

        # ===================================================
        # INVENTORY
        # ===================================================

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

        # ===================================================
        # ORDERS
        # ===================================================

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

# ===================================================
# FOOTER
# ===================================================

st.markdown("---")

st.caption(
    "PerfumeIQ AI © 2026"
)