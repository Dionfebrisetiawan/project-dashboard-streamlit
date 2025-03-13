import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
from unidecode import unidecode 

sns.set(style='dark')

st.header('Selamat Datang di Dashboard E-Commerce Public Dataset ✨')

order_payments = pd.read_csv("order_payments_dataset.csv")  
customer_dataset = pd.read_csv("customers_dataset.csv")  

if not order_payments.empty:
    st.subheader("Ringkasan Data")
    st.write(order_payments.describe(include="all"))

    # Membuat DataFrame untuk metode pembayaran
    sum_order_items_df = order_payments.groupby('payment_type')['order_id'].count().reset_index()
    sum_order_items_df.columns = ['payment_type', 'order_count']  
    sum_order_items_df = sum_order_items_df.sort_values(by="order_count", ascending=False)

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    sns.barplot(x="order_count", y="payment_type", data=sum_order_items_df.head(5), palette=colors, ax=ax)
    ax.set_title("Payment Types", fontsize=15)
    ax.set_xlabel("Order Count")
    ax.set_ylabel("Payment Type")
    
    st.pyplot(fig)  # Menampilkan visualisasi di Streamlit

if not customer_dataset.empty:
    customer_dataset["customer_city"] = customer_dataset["customer_city"].apply(
        lambda x: unidecode(x.lower()) if pd.notnull(x) else x
    )

    # Menghitung distribusi customer per kota
    customer_distribution = customer_dataset["customer_city"].value_counts().reset_index()
    customer_distribution.columns = ["customer_city", "count"]

    top_5_cities = customer_distribution.head(5)

    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
    
    sns.barplot(x="count", y="customer_city", data=top_5_cities, palette=colors, ax=ax)
    ax.set_title("Customers Distribution", fontsize=15)
    ax.set_xlabel("Customer Count")
    ax.set_ylabel("Customer City")
    
    st.pyplot(fig) 

if order_payments.empty:
    raise ValueError("Dataset order_payments kosong!")

# Menghitung jumlah transaksi per metode pembayaran
payment_count = order_payments["payment_type"].value_counts().reset_index()
payment_count.columns = ["payment_type", "count"]

# Menghitung rata-rata nilai transaksi per metode pembayaran
average_transaction = order_payments.groupby("payment_type")["payment_value"].mean().reset_index()

result = pd.merge(payment_count, average_transaction, on="payment_type")

print(result.head())

fig, ax1 = plt.subplots(figsize=(12, 6))

color1 = "#72BCD4"
sns.barplot(x="payment_type", y="count", data=result, ax=ax1, color=color1, label="Total Transactions")

ax2 = ax1.twinx()
color2 = "#D97706"
sns.lineplot(x="payment_type", y="payment_value", data=result, ax=ax2, color=color2, marker="o", linewidth=2, label="Avg Transaction Value")

ax1.set_xlabel("Payment Type")
ax1.set_ylabel("Total Transactions", color=color1)
ax2.set_ylabel("Avg Transaction Value", color=color2)
plt.title("Comparison of Payment Methods: Transactions vs. Avg Transaction Value")

ax1.legend(loc="upper left")
ax2.legend(loc="upper right")

st.pyplot(fig)

st.write("Do you satisfied with the dashboard?")

max_value = st.slider(
    label="Adjust satisfaction level",
    min_value=0, max_value=100, value=100
)
values = (0, max_value)

print("Matplotlib berhasil diimpor!")