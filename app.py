import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")

st.set_page_config(layout="wide")
st.title("📊 Advanced Finance Analytics Dashboard")

# ----------------------------
# Internal Dataset
# ----------------------------
data = {
    "Date": pd.date_range(start="2025-01-01", periods=12, freq="D"),
    "Type": ["Income","Expense","Expense","Income","Expense","Expense","Income","Expense","Income","Expense","Expense","Income"],
    "Category": ["Salary","Food","Transport","Freelance","Bills","Shopping","Bonus","Travel","Salary","Entertainment","Food","Bonus"],
    "Amount": [50000,4000,2000,12000,3000,4500,8000,2500,55000,3000,3500,9000]
}

df = pd.DataFrame(data)

# ----------------------------
# KPIs
# ----------------------------
income = df[df["Type"] == "Income"]["Amount"].sum()
expense = df[df["Type"] == "Expense"]["Amount"].sum()
balance = income - expense

col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Income", f"₹ {income}")
col2.metric("💸 Total Expense", f"₹ {expense}")
col3.metric("📊 Balance", f"₹ {balance}")

# ----------------------------
# Charts Section
# ----------------------------
colA, colB = st.columns(2)

# 🔹 Bar Chart
with colA:
    st.subheader("📊 Expense by Category")

    exp_df = df[df["Type"] == "Expense"]

    cat_data = exp_df.groupby("Category")["Amount"].sum().reset_index()

    fig1, ax1 = plt.subplots(figsize=(6,4))
    sns.barplot(data=cat_data, x="Category", y="Amount", ax=ax1)
    plt.xticks(rotation=45)

    st.pyplot(fig1)

# 🔹 Pie Chart
with colB:
    st.subheader("🥧 Income vs Expense")

    fig2, ax2 = plt.subplots(figsize=(5,5))
    ax2.pie(
        [income, expense],
        labels=["Income", "Expense"],
        autopct='%1.1f%%',
        startangle=90
    )

    st.pyplot(fig2)

# ----------------------------
# Trend Chart
# ----------------------------
st.subheader("📈 Spending Trend Over Time")

trend = df.groupby("Date")["Amount"].sum().reset_index()

fig3, ax3 = plt.subplots(figsize=(10,4))
ax3.plot(trend["Date"], trend["Amount"], marker="o")

plt.xticks(rotation=45)
st.pyplot(fig3)

# ----------------------------
# Distribution Chart
# ----------------------------
st.subheader("📊 Expense Distribution")

fig4, ax4 = plt.subplots(figsize=(10,4))
sns.histplot(df[df["Type"] == "Expense"]["Amount"], kde=True, ax=ax4)

st.pyplot(fig4)

# ----------------------------
# Data Table
# ----------------------------
st.subheader("📋 Dataset")
st.dataframe(df)
