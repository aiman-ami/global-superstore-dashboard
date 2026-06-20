import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title='Global Superstore Dashboard', layout='wide')

st.markdown('<h1 style="text-align: center; color: #1f77b4;">Global Superstore Dashboard</h1>', unsafe_allow_html=True)
st.markdown('<h3 style="text-align: center; color: #555;">Sales, Profit and Segment Performance Analysis</h3>', unsafe_allow_html=True)

@st.cache_data
def load_data():
    orders = pd.read_excel('Global Superstore.xls', sheet_name='Orders', engine='xlrd')
    returns = pd.read_excel('Global Superstore.xls', sheet_name='Returns', engine='xlrd')
    people = pd.read_excel('Global Superstore.xls', sheet_name='People', engine='xlrd')

    orders['Returned'] = orders['Order ID'].isin(returns['Order ID']).map({True: 'Yes', False: 'No'})
    df = orders.merge(people, on='Region', how='left')

    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Order Year'] = df['Order Date'].dt.year
    df['Profit Margin'] = (df['Profit'] / df['Sales'] * 100).round(2)
    return df

df = load_data()

st.sidebar.header('Filters')

regions = ['All'] + sorted(df['Region'].unique().tolist())
selected_region = st.sidebar.selectbox('Select Region', regions)

categories = ['All'] + sorted(df['Category'].unique().tolist())
selected_category = st.sidebar.selectbox('Select Category', categories)

sub_categories = ['All'] + sorted(df['Sub-Category'].unique().tolist())
selected_sub_category = st.sidebar.selectbox('Select Sub-Category', sub_categories)

years = ['All'] + sorted(df['Order Year'].unique().tolist())
selected_year = st.sidebar.selectbox('Select Year', years)

managers = ['All'] + sorted(df['Person'].dropna().unique().tolist())
selected_manager = st.sidebar.selectbox('Select Regional Manager', managers)

filtered_df = df.copy()
if selected_region != 'All':
    filtered_df = filtered_df[filtered_df['Region'] == selected_region]
if selected_category != 'All':
    filtered_df = filtered_df[filtered_df['Category'] == selected_category]
if selected_sub_category != 'All':
    filtered_df = filtered_df[filtered_df['Sub-Category'] == selected_sub_category]
if selected_year != 'All':
    filtered_df = filtered_df[filtered_df['Order Year'] == selected_year]
if selected_manager != 'All':
    filtered_df = filtered_df[filtered_df['Person'] == selected_manager]

st.sidebar.markdown('---')
st.sidebar.markdown(f"**Filtered Records:** {len(filtered_df):,}")

if len(filtered_df) > 0:
    return_rate = (filtered_df['Returned'] == 'Yes').sum() / len(filtered_df) * 100
else:
    return_rate = 0
st.sidebar.markdown(f"**Return Rate:** {return_rate:.1f}%")

st.markdown('---')
st.subheader('Key Performance Indicators')

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric('Total Sales', f"${filtered_df['Sales'].sum():,.0f}")
with col2:
    st.metric('Total Profit', f"${filtered_df['Profit'].sum():,.0f}")
with col3:
    st.metric('Avg Order Value', f"${filtered_df['Sales'].mean():.2f}")
with col4:
    st.metric('Total Orders', f"{filtered_df['Order ID'].nunique():,}")
with col5:
    total_returns = (filtered_df['Returned'] == 'Yes').sum()
    st.metric('Returns', f"{total_returns:,}")

st.markdown('---')
st.subheader('Visual Analytics')

chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown('##### Sales Trend Over Time')
    monthly = filtered_df.groupby(filtered_df['Order Date'].dt.to_period('M')).agg({'Sales': 'sum', 'Profit': 'sum'}).reset_index()
    monthly['Order Date'] = monthly['Order Date'].astype(str)
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(monthly['Order Date'], monthly['Sales'], marker='o', color='#1f77b4')
    ax.set_xlabel('Month')
    ax.set_ylabel('Sales ($)')
    ax.tick_params(axis='x', rotation=45)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close()

with chart_col2:
    st.markdown('##### Profit Trend Over Time')
    fig, ax = plt.subplots(figsize=(10, 5))
    colors = ['green' if p >= 0 else 'red' for p in monthly['Profit']]
    ax.bar(monthly['Order Date'], monthly['Profit'], color=colors, alpha=0.7)
    ax.set_xlabel('Month')
    ax.set_ylabel('Profit ($)')
    ax.tick_params(axis='x', rotation=45)
    ax.axhline(y=0, color='black', linewidth=0.5)
    ax.grid(True, alpha=0.3)
    st.pyplot(fig)
    plt.close()

chart_col3, chart_col4 = st.columns(2)

with chart_col3:
    st.markdown('##### Sales by Category')
    cat_sales = filtered_df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(cat_sales.index, cat_sales.values, color=['#1f77b4', '#ff7f0e', '#2ca02c'], edgecolor='black')
    ax.set_ylabel('Sales ($)')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
    plt.close()

with chart_col4:
    st.markdown('##### Sales by Regional Manager')
    mgr_sales = filtered_df.groupby('Person')['Sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.bar(mgr_sales.index, mgr_sales.values, color=['#d62728', '#9467bd', '#8c564b', '#e377c2'], edgecolor='black')
    ax.set_ylabel('Sales ($)')
    ax.tick_params(axis='x', rotation=45)
    st.pyplot(fig)
    plt.close()

chart_col5, chart_col6 = st.columns(2)

with chart_col5:
    st.markdown('##### Top 10 Sub-Categories by Sales')
    subcat = filtered_df.groupby('Sub-Category')['Sales'].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(subcat.index[::-1], subcat.values[::-1], color='#17becf', edgecolor='black')
    ax.set_xlabel('Sales ($)')
    st.pyplot(fig)
    plt.close()

with chart_col6:
    st.markdown('##### Sales by Segment')
    seg_sales = filtered_df.groupby('Segment')['Sales'].sum().sort_values(ascending=False)
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.pie(seg_sales.values, labels=seg_sales.index, autopct='%1.1f%%', colors=['#bcbd22', '#7f7f7f', '#ffbb78'], startangle=90)
    st.pyplot(fig)
    plt.close()

st.markdown('---')
st.subheader('Top 5 Customers by Sales')
top_cust = filtered_df.groupby('Customer Name').agg(
    Total_Sales=('Sales', 'sum'),
    Total_Profit=('Profit', 'sum'),
    Orders=('Order ID', 'nunique'),
    Returns=('Returned', lambda x: (x == 'Yes').sum())
).sort_values('Total_Sales', ascending=False).head(5).reset_index()
top_cust.columns = ['Customer Name', 'Total Sales', 'Total Profit', 'Orders', 'Returns']
st.dataframe(top_cust, use_container_width=True, hide_index=True)

st.markdown('---')
st.subheader('Detailed Data View')
display_cols = ['Order ID', 'Order Date', 'Customer Name', 'Segment', 'Region', 'Person', 'Category', 'Sub-Category', 'Sales', 'Profit', 'Profit Margin', 'Returned']
st.dataframe(filtered_df[display_cols], use_container_width=True, hide_index=True)

st.markdown('---')
st.markdown('<p style="text-align: center; color: #666;">Global Superstore Dashboard | Built with Streamlit</p>', unsafe_allow_html=True)