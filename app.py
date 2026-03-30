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
st.subheader("📈 Expense Chart")

if not df.empty:
    expense_data = df[df["Type"] == "Expense"]

    if not expense_data.empty:
        chart_data = expense_data.groupby("Category")["Amount"].sum()

        fig, ax = plt.subplots()
        chart_data.plot(kind="bar", ax=ax)
        ax.set_title("Expenses by Category")

        st.pyplot(fig)
    else:
        st.info("No expense data to show chart")
else:
    st.info("No data available")
