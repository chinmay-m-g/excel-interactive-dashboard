import pandas as pd
import plotly.express as px
import streamlit as st

#@st.cache
def excel_to_df(file_name):
    df= pd.read_excel(
        io=file_name,
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols='B:R',
        nrows=1000,
        )
    #Add 'hour' column to data frame
    df["hour"] = pd.to_datetime(df["Time"], format="%H:%M:%S").dt.hour
    return df

if __name__=="__main__":
    df = excel_to_df("supermarkt_sales.xlsx")
    #setting page config
    st.set_page_config(
        page_title = "Sales Dashboard",
        page_icon=":bar_chart:",
        layout="wide"
        )
    #sidebar
    st.sidebar.header("Please Filter Here:")
    city = st.sidebar.multiselect(
        "Select the City:",
        options=df["City"].unique(),
        default=df["City"].unique()
    )
    customer_type = st.sidebar.multiselect(
        "Select the Customer Type:",
        options=df["Customer_type"].unique(),
        default=df["Customer_type"].unique()
    )
    gender = st.sidebar.multiselect(
        "Select the Gender:",
        options=df["Gender"].unique(),
        default=df["Gender"].unique()
    )
    df_selection = df.query(
        "City == @city & Customer_type == @customer_type & Gender == @gender"
    )
    st.title(":bar_chart: sales Dashboard")
    st.markdown("##")

    #top api
    total_sales = int(df_selection["Total"].sum())
    average_rating = round(df_selection["Rating"].mean(),1)
    star_rating = ":star:" * int(round(average_rating,0))
    average_sales_per_transaction = round(df_selection["Total"].mean(),2)
    
    left_column, middle_column, right_column= st.columns(3)
    with left_column:
        st.subheader("Total Sales:")
        st.subheader(f"US $ {total_sales:,}") # {total_sales:,} for 1000 separator with comma
    with middle_column:
        st.subheader("Total Rating:")
        st.subheader(f"{average_rating} {star_rating}")
    with right_column:
        st.subheader("Average Sales Per Transaction:")
        st.subheader(f"US $ {average_sales_per_transaction}")
    # Sales by product [Bar chart]
    sales_by_product_line=(
    df.groupby(by=["Product line"]).sum()[["Total"]].sort_values(by="Total")
    )
    fig_product_sales = px.bar(
        sales_by_product_line, 
        x="Total", 
        y=sales_by_product_line.index,
        orientation="h",
        title="<b>Sales by Product Line</b>",
        color_discrete_sequence=["#0083B8"] *len(sales_by_product_line),
        template="plotly_white",
        )
    fig_product_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=(dict(showgrid=False))
        )

     # Sales by hour [Bar chart]
    sales_by_hour=df_selection.groupby(by=["hour"]).sum()[["Total"]]
    fig_hourly_sales = px.bar(
        sales_by_hour, 
        x=sales_by_hour.index, 
        y="Total",
        #orientation="h",
        title="<b>Sales by Hour</b>",
        color_discrete_sequence=["#0083B8"] *len(sales_by_hour),
        template="plotly_white",
        )
    fig_hourly_sales.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        yaxis=(dict(showgrid=False)),
        xaxis=dict(tickmode="linear"),
        )

    left_column, right_column = st.columns(2)
    right_column.plotly_chart(fig_product_sales)
    left_column.plotly_chart(fig_hourly_sales)
    
    hide_st_style="""
                        <style>
                        #MainMenu {visibility: hidden;}
                        footer {visibility: hidden;}
                        header {visibility: hidden;}
                        </style>

                  """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    #st.dataframe(df_selection)        
