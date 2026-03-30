import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Finance Tracker", layout="wide")

st.title("💰 Personal Finance Tracker")

# Session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Type", "Category", "Amount"])

# ===== SIDEBAR FORM (FIXED) =====
st.sidebar.header("Add Transaction")

with st.sidebar.form("form", clear_on_submit=True):
    type_ = st.selectbox("Type", ["Income", "Expense"])
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0)

    submit = st.form_submit_button("Add Transaction")

# Add data
if submit:
    if category != "" and amount > 0:
        new_data = pd.DataFrame([[type_, category, amount]],
                                columns=["Type", "Category", "Amount"])
        st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
        st.success("Transaction Added!")
    else:
        st.warning("Enter valid details")

df = st.session_state.data

# ===== SHOW DATA =====
st.subheader("📋 Transactions")
st.dataframe(df)

# ===== SUMMARY =====
income = df[df["Type"] == "Income"]["Amount"].sum()
expense = df[df["Type"] == "Expense"]["Amount"].sum()
balance = income - expense

st.subheader("📊 Summary")
col1, col2, col3 = st.columns(3)
col1.metric("Income", f"₹{income}")
col2.metric("Expense", f"₹{expense}")
col3.metric("Balance", f"₹{balance}")

# ===== ADVANCED GRAPHS =====
st.subheader("📈 Financial Insights")

if not df.empty:

    col1, col2 = st.columns(2)

    # Bar Chart
    with col1:
        st.write("### Expense by Category")
        expense_data = df[df["Type"] == "Expense"]

        if not expense_data.empty:
            cat_data = expense_data.groupby("Category")["Amount"].sum()
            fig1, ax1 = plt.subplots()
            cat_data.plot(kind="bar", ax=ax1)
            st.pyplot(fig1)
        else:
            st.info("No expense data")

    # Pie Chart
    with col2:
        st.write("### Income vs Expense")
        fig2, ax2 = plt.subplots()
        ax2.pie([income, expense], labels=["Income", "Expense"], autopct='%1.1f%%')
        st.pyplot(fig2)

    # Horizontal Chart
    st.write("### Category Distribution")
    if not expense_data.empty:
        fig3, ax3 = plt.subplots()
        cat_data.sort_values().plot(kind="barh", ax=ax3)
        st.pyplot(fig3)

else:
    st.info("Add some data to see graphs")
