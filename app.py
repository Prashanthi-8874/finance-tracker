import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")

st.set_page_config(layout="wide")
st.title("📊 Advanced Finance Dashboard")

# ----------------------------
# Store data in session
# ----------------------------
if "data" not in st.session_state:
    st.session_state.data = []

# ----------------------------
# Input Section
# ----------------------------
st.subheader("➕ Add Transaction")

col1, col2, col3 = st.columns(3)

with col1:
    t_type = st.selectbox("Type", ["Income", "Expense"])

with col2:
    category = st.text_input("Category")

with col3:
    amount = st.number_input("Amount", min_value=0)

if st.button("Add Transaction"):
    if category and amount > 0:
        st.session_state.data.append([t_type, category, amount])
        st.success("✅ Added successfully")
    else:
        st.error("Please enter valid data")

# ----------------------------
# Convert to DataFrame
# ----------------------------
df = pd.DataFrame(st.session_state.data, columns=["Type", "Category", "Amount"])

st.subheader("📋 Transactions")
st.dataframe(df)

# ----------------------------
# Dashboard
# ----------------------------
if not df.empty:

    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()
    balance = income - expense

    # KPI Cards
    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Income", income)
    col2.metric("💸 Expense", expense)
    col3.metric("📊 Balance", balance)

    # Charts
    colA, colB = st.columns(2)

    # Bar Chart
    with colA:
        st.subheader("📊 Expense by Category")

        exp_df = df[df["Type"] == "Expense"]

        if not exp_df.empty:
            cat_data = exp_df.groupby("Category")["Amount"].sum().reset_index()

            fig1, ax1 = plt.subplots()
            sns.barplot(data=cat_data, x="Category", y="Amount", ax=ax1)
            plt.xticks(rotation=45)

            st.pyplot(fig1)
        else:
            st.info("Add expense data to see bar chart")

    # Pie Chart
    with colB:
        st.subheader("🥧 Income vs Expense")

        if income > 0 or expense > 0:
            fig2, ax2 = plt.subplots()
            ax2.pie([income, expense],
                    labels=["Income", "Expense"],
                    autopct='%1.1f%%',
                    startangle=90)
            st.pyplot(fig2)

    # Trend Chart
    st.subheader("📈 Spending Trend")

    fig3, ax3 = plt.subplots()
    df_group = df.groupby("Category")["Amount"].sum().reset_index()
    sns.lineplot(data=df_group, x="Category", y="Amount", marker="o", ax=ax3)
    plt.xticks(rotation=45)

    st.pyplot(fig3)

else:
    st.info("👉 Add transactions to see analytics")
