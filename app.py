import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")

st.title("💰 Finance Tracker Dashboard")

# ----------------------------
# Session state to store data
# ----------------------------
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Type", "Category", "Amount"])

# ----------------------------
# Input Form
# ----------------------------
st.subheader("➕ Add Transaction")

with st.form("entry_form"):
    type_option = st.selectbox("Type", ["Income", "Expense"])
    category = st.text_input("Category")
    amount = st.number_input("Amount", min_value=0)

    submit = st.form_submit_button("Add")

    if submit:
        if category and amount > 0:
            new_data = pd.DataFrame([[type_option, category, amount]],
                                    columns=["Type", "Category", "Amount"])
            st.session_state.data = pd.concat([st.session_state.data, new_data], ignore_index=True)
            st.success("Transaction added!")
        else:
            st.error("Please enter valid category and amount")

# ----------------------------
# Show Data
# ----------------------------
df = st.session_state.data

st.subheader("📋 Transactions")
st.dataframe(df)

# ----------------------------
# Dashboard
# ----------------------------
st.subheader("📊 Advanced Financial Dashboard")

if not df.empty:

    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()

    expense_data = df[df["Type"] == "Expense"]

    col1, col2 = st.columns(2)

    # 🔹 Bar Chart
    with col1:
        st.write("### Expense by Category")

        if not expense_data.empty:
            cat_data = expense_data.groupby("Category")["Amount"].sum().reset_index()

            fig1, ax1 = plt.subplots(figsize=(8, 5))
            sns.barplot(data=cat_data, x="Category", y="Amount", ax=ax1)
            ax1.set_title("Expenses by Category")

            st.pyplot(fig1)

    # 🔹 Pie Chart
    with col2:
        st.write("### Income vs Expense")

        fig2, ax2 = plt.subplots(figsize=(6, 6))
        ax2.pie(
            [income, expense],
            labels=["Income", "Expense"],
            autopct='%1.1f%%',
            startangle=90
        )
        ax2.set_title("Income vs Expense")

        st.pyplot(fig2)

    # 🔹 Distribution Chart
    st.write("### Expense Distribution")

    if not expense_data.empty:
        fig3, ax3 = plt.subplots(figsize=(10, 5))
        sns.histplot(expense_data["Amount"], kde=True, ax=ax3)
        ax3.set_title("Expense Distribution Curve")
        st.pyplot(fig3)

else:
    st.info("Add transactions to see charts")
