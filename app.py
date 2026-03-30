import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Finance Tracker", layout="wide")

st.title("💰 Personal Finance Tracker")

# Initialize session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Type", "Category", "Amount"])

# Sidebar input
st.sidebar.header("Add Transaction")

type_ = st.sidebar.selectbox("Type", ["Income", "Expense"])
category = st.sidebar.text_input("Category")
amount = st.sidebar.number_input("Amount", min_value=0)

if st.sidebar.button("Add"):
    new_data = pd.DataFrame([[type_, category, amount]],
                            columns=["Type", "Category", "Amount"])
    st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
    st.success("Added Successfully!")

df = st.session_state.data

# Show data
st.subheader("📋 Transactions")
st.dataframe(df)

# Total calculations
income = df[df["Type"] == "Income"]["Amount"].sum()
expense = df[df["Type"] == "Expense"]["Amount"].sum()
balance = income - expense

st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)

col1.metric("Income", f"₹{income}")
col2.metric("Expense", f"₹{expense}")
col3.metric("Balance", f"₹{balance}")

# Chart
st.subheader("📊 Advanced Financial Insights")

if not df.empty:

    col1, col2 = st.columns(2)

    # 1️⃣ Expense by Category (Bar Chart)
    with col1:
        st.write("### Expense by Category")
        expense_data = df[df["Type"] == "Expense"]
        if not expense_data.empty:
            cat_data = expense_data.groupby("Category")["Amount"].sum()
            fig1, ax1 = plt.subplots()
            cat_data.plot(kind="bar", ax=ax1)
            ax1.set_xlabel("Category")
            ax1.set_ylabel("Amount")
            st.pyplot(fig1)
        else:
            st.info("No expense data")

    # 2️⃣ Income vs Expense (Pie Chart)
    with col2:
        st.write("### Income vs Expense")
        labels = ["Income", "Expense"]
        values = [income, expense]

        fig2, ax2 = plt.subplots()
        ax2.pie(values, labels=labels, autopct='%1.1f%%')
        st.pyplot(fig2)

    # 3️⃣ Category Distribution (Horizontal Bar)
    st.write("### Category Distribution")
    if not expense_data.empty:
        fig3, ax3 = plt.subplots()
        cat_data.sort_values().plot(kind="barh", ax=ax3)
        st.pyplot(fig3)

else:
    st.info("Add some data to see insights")
