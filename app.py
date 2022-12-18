from enum import unique
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide"
)

# -------------- READ EXCEL FILE ---------------
df = pd.read_excel(
    io='supermarkt_sales.xlsx',
    engine='openpyxl',
    sheet_name='Sales',
    skiprows=3,
    usecols='B:R',
    nrows=1000,
)


# -------------- SIDEBAR ---------------

## multiselect for city 
st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select City:",
    options=df["City"].unique(),
    default=df["City"].unique()
)

## multiselect for gender
gender = st.sidebar.multiselect(
    "Select Gender:",
    options=df["Gender"].unique(),
    default=df["Gender"].unique()
)

## multiselect for customer type
customer_type = st.sidebar.multiselect(
    "Select Customer Type:",
    options=df["Customer_type"].unique(),
    default=df["Customer_type"].unique()
)

## multiselect for branch 
branch = st.sidebar.multiselect(
    "Select Branch:",
    options=df["Branch"].unique(),
    default=df["Branch"].unique()
)

payment = st.sidebar.multiselect(
    "Select Payment:",
    options=df["Payment"].unique(),
    default=df["Payment"].unique()
)

#"name_column" == @value
df_selection = df.query(
    "City == @city & Gender == @gender & Customer_type == @customer_type & Branch == @branch & Payment == @payment" 
) 

# st.title("🛸 Data")
# st.dataframe(df_selection)


# -------------- MAIN HEADER ---------------

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

total = round(df_selection["Total"].sum(), 2)
avg_rating_test = df_selection["Rating"].mean()
avg_rating = round(df_selection["Rating"].mean(), 1)
star_rating = ":star:" * int(round(avg_rating, 0))
avg_total = round(df_selection["Total"].mean(), 2)

left_column, center_column, right_column = st.columns(3)

with left_column:
    st.subheader("Total:")
    st.subheader(f"RM {total:,}")

with center_column:
    st.subheader("Average Rating:")
    # st.subheader(f"{avg_rating_test}")
    st.subheader(f"{avg_rating} {star_rating}")

with right_column:
    st.subheader("Average Sales Per Transaction:")
    st.subheader(f"RM {avg_total}")

st.markdown("---")


# SALES BY PRODUCT LINE [BAR CHART]

sales_by_product_line = (df_selection.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total"))

fig_product_sales = px.bar(
    sales_by_product_line,
    x = "Total",
    y = sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white"
)

st.plotly_chart(fig_product_sales)