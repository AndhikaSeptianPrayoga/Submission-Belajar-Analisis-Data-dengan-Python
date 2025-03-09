import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import urllib.request
import matplotlib.image as mpimg

# Set page configuration
st.set_page_config(page_title="Analisis Data Penjualan pada Dataset E-Commerce Publik", layout="wide")

# Title and description
st.title("📊 Analisis Data Penjualan pada Dataset E-Commerce Publik")

# Profile section
st.sidebar.markdown("""
    ### 👤 **Nama** : **Andhika Septian Prayoga**  
    ### 📧 **Email** : [andhika.elite007@gmail.com](mailto:andhika.elite007@gmail.com) | [mc299d5y1775@student.devacademy.id](mailto:mc299d5y1775@student.devacademy.id)  
    ### 🆔 **ID** : **MC299D5Y1775**
""")

# Load data
@st.cache_data
def load_data():
    data = pd.read_csv('main-data.csv')
    return data

data = load_data()

# Calculate product sales
product_sales = data.groupby('product_category_name_english').size().reset_index(name='sales_count')
product_sales_sorted = product_sales.sort_values(by='sales_count', ascending=False)

# Get top 10 and bottom 10 products
top_10_products = product_sales_sorted.head(10)
bottom_10_products = product_sales_sorted.tail(10)

# Display data overview
st.header("Data Overview")
st.dataframe(data.head())

# Visualize key metrics
st.header("Key Metrics Visualization")

# Plot Top 10 Produk Terlaris
st.subheader("Top 10 Produk Terlaris")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='sales_count', y='product_category_name_english', data=top_10_products, palette='viridis', ax=ax)
ax.set_title('Top 10 Produk Terlaris')
ax.set_xlabel('Jumlah Penjualan')
ax.set_ylabel('Kategori Produk')
st.pyplot(fig)

# Plot Bottom 10 Produk yang Kurang Diminati
st.subheader("Bottom 10 Produk yang Kurang Diminati")
fig, ax = plt.subplots(figsize=(10, 5))
sns.barplot(x='sales_count', y='product_category_name_english', data=bottom_10_products, palette='magma', ax=ax)
ax.set_title('Bottom 10 Produk yang Kurang Diminati')
ax.set_xlabel('Jumlah Penjualan')
ax.set_ylabel('Kategori Produk')
st.pyplot(fig)

# Additional visualization for customer spending over time
st.subheader("Total Pengeluaran Pelanggan per Bulan")
data['order_purchase_timestamp'] = pd.to_datetime(data['order_purchase_timestamp'])
start_date = '2017-01-01'
end_date = '2018-12-31'
filtered_orders = data[(data['order_purchase_timestamp'] >= start_date) & (data['order_purchase_timestamp'] <= end_date)]

filtered_orders['order_purchase_timestamp'] = pd.to_datetime(filtered_orders['order_purchase_timestamp'])
monthly_spending = filtered_orders.groupby(filtered_orders['order_purchase_timestamp'].dt.to_period('M'))['payment_value'].sum().reset_index()
monthly_spending['order_purchase_timestamp'] = monthly_spending['order_purchase_timestamp'].dt.to_timestamp()

fig, ax = plt.subplots(figsize=(12, 6))
sns.lineplot(x='order_purchase_timestamp', y='payment_value', data=monthly_spending, marker='o', ax=ax)
ax.set_title('Total Pengeluaran Pelanggan per Bulan')
ax.set_xlabel('Bulan')
ax.set_ylabel('Total Pengeluaran (Rupiah)')
plt.xticks(rotation=45)
ax.grid(True)
st.pyplot(fig)

# Additional visualization for customer geographic locations
st.subheader("Top 10 Geographic Locations of Customers")

# Process geolocation data
customer_locations = data.groupby(['customer_city', 'customer_state']).size().reset_index(name='customer_count')
customer_locations_sorted = customer_locations.sort_values(by='customer_count', ascending=False)
top_10_customer_locations = customer_locations_sorted.head(10)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x='customer_count', y='customer_city', data=top_10_customer_locations, palette='viridis', ax=ax)
ax.set_title('Top 10 Geographic Locations of Customers')
ax.set_xlabel('Number of Customers')
ax.set_ylabel('City')
st.pyplot(fig)

# Placeholder for insights
st.header("Insights")
st.markdown("""
    - **Top Selling Products:** The top 10 best-selling products are highlighted, showing which product categories are the most popular among customers.
    - **Least Popular Products:** The bottom 10 products with the lowest sales are identified, indicating which product categories are less favored.
    - **Customer Spending Over Time:** The total monthly spending of customers is visualized, revealing trends and patterns in customer expenditure over the specified period.
    - **Geographic Distribution of Customers:** The top 10 cities with the highest number of customers are displayed, providing insights into the geographic concentration of the customer base.
""")

# Footer
st.markdown("""
    <style>
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: white;
        color: black;
        text-align: center;
        padding: 10px;
    }
    </style>
    <div class="footer">
        © Andhika Septian Prayoga
    </div>
""", unsafe_allow_html=True)