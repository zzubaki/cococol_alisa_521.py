
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Хатыпова Алиса full задание",
                   page_icon=":bar_chart:",
                   layout="wide"
)

@st.cache_data
def get_data_from_excel():
    df = pd.read_excel(
        io="supermarkt_sales.xlsx",
        engine="openpyxl",
        sheet_name="Sales",
        skiprows=3,
        usecols="B:R",
        nrows=305,
    )

    df["час"] = pd.to_datetime(df["Время"], format="%H:%M:%S").dt.hour
    return df

df = get_data_from_excel()


st.sidebar.header("Please Filter Here:")
city = st.sidebar.multiselect(
    "Select the City:",
    options=df["Город"].unique(),
    default=df["Город"].unique()
)

customer_type = st.sidebar.multiselect(
    "Select the Customer Type:",
    options=df["Тип_клиента"].unique(),
    default=df["Тип_клиента"].unique(),
)

gender = st.sidebar.multiselect(
    "Select the Gender:",
    options=df["Пол"].unique(),
    default=df["Пол"].unique()
)

df_selection = df.query(
    "Город == @city & Тип_клиента ==@customer_type & Пол == @gender"
)

if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()


st.title(":bar_chart: Sales Dashboard")
st.markdown("##")


total_sales = int(df_selection["Итого"].sum())
average_rating = round(df_selection["Рейтинг"].mean(), 1)
star_rating = ":star:" * int(round(average_rating, 0))
average_sale_by_transaction = round(df_selection["Итого"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Всего продаж:")
    st.subheader(f"US $ {total_sales:,}")
with middle_column:
    st.subheader("Средний рейтинг:")
    st.subheader(f"{average_rating} {star_rating}")
with right_column:
    st.subheader("Средний рейнинг за транзакцию:")
    st.subheader(f"US $ {average_sale_by_transaction}")

st.markdown("""---""")


sales_by_product_line = df_selection.groupby(by=["Product line"])[["Total"]].sum().sort_values(by="Total")
fig_product_sales = px.bar(
    sales_by_product_line,
    x="Total",
    y=sales_by_product_line.index,
    orientation="h",
    title="<b>Sales by Product Line</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_product_line),
    template="plotly_white",
)
fig_product_sales.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    xaxis=(dict(showgrid=False))
)


sales_by_hour = df_selection.groupby(by=["hour"])[["Total"]].sum()
fig_hourly_sales = px.bar(
    sales_by_hour,
    x=sales_by_hour.index,
    y="Total",
    title="<b>Sales by hour</b>",
    color_discrete_sequence=["#0083B8"] * len(sales_by_hour),
    template="plotly_white",
)
fig_hourly_sales.update_layout(
    xaxis=dict(tickmode="linear"),
    plot_bgcolor="rgba(0,0,0,0)",
    yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
