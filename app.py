import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")

st.set_page_config(layout="wide")

st.title("📊 Interactive Finance Dashboard")

# ----------------------------
# Session state (store data)
# ----------------------------
if "df" not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["Type", "Category", "Amount"])

# ----------------------------
# Input Section
# ----------------------------
st.subheader("➕ Add Transaction")

col1, col2, col3 = st.columns(3)

with col1:
    type_val = st.selectbox("Type", ["Income", "Expense"])

with col2:
    category_val = st.text_input("Category")

with col3:
    amount_val = st.number_input("Amount", min_value=0)

if st.button("Add Entry"):
    if category_val and amount_val > 0:
        new_row = pd.DataFrame([[type_val, category_val, amount_val]],
                               columns=["Type", "Category", "Amount"])
        st.session_state.df = pd.concat([st.session_state.df, new_row], ignore_index=True)
        st.success("✅ Added successfully!")
    else:
        st.error("Please enter valid data")

# ----------------------------
# Data
# ----------------------------
df = st.session_state.df

st.subheader("📋 Transactions Table")
st.dataframe(df)

# ----------------------------
# KPIs
# ----------------------------
if not df.empty:
    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = income - expense

    k1, k2, k3 = st.columns(3)
    k1.metric("💰 Income", income)
    k2.metric("💸 Expense", expense)
    k3.metric("📊 Balance", balance)

    # ----------------------------
    # Charts
    # ----------------------------
    colA, colB = st.columns(2)

    # 🔹 Bar Chart
    with colA:
        st.subheader("📊 Expense by Category")

        exp_df = df[df["Type"] == "Expense"]

        if not exp_df.empty:
            cat_data = exp_df.groupby("Category")["Amount"].sum().reset_index()

            fig1, ax1 = plt.subplots()
            sns.barplot(data=cat_data, x="Category", y="Amount", ax=ax1)
            plt.xticks(rotation=45)

            st.pyplot(fig1)

    # 🔹 Pie Chart
    with colB:
        st.subheader("🥧 Income vs Expense")

        fig2, ax2 = plt.subplots()
        ax2.pie([income, expense],
                labels=["Income", "Expense"],
                autopct='%1.1f%%',
                startangle=90)

        st.pyplot(fig2)

    # 🔹 Distribution Chart
    st.subheader("📈 Expense Distribution")

    exp_df = df[df["Type"] == "Expense"]

    if not exp_df.empty:
        fig3, ax3 = plt.subplots()
        sns.histplot(exp_df["Amount"], kde=True, ax=ax3)
        st.pyplot(fig3)

else:
    st.info("👉 Add transactions to see analytics")
