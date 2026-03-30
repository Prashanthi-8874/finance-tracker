import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_style("darkgrid")

st.title("📊 Live Finance Dashboard")

# ----------------------------
# Store data
# ----------------------------
if "data" not in st.session_state:
    st.session_state.data = []

# ----------------------------
# Input
# ----------------------------
st.subheader("➕ Enter Data")

col1, col2, col3 = st.columns(3)

with col1:
    t_type = st.selectbox("Type", ["Income", "Expense"])

with col2:
    category = st.text_input("Category")

with col3:
    amount = st.number_input("Amount", min_value=0)

if st.button("Add"):
    if category and amount > 0:
        st.session_state.data.append({
            "Type": t_type,
            "Category": category,
            "Amount": amount
        })
        st.success("Added!")

# ----------------------------
# Convert to DataFrame
# ----------------------------
df = pd.DataFrame(st.session_state.data)

st.subheader("📋 Data")
st.dataframe(df)

# ----------------------------
# Charts (LIVE)
# ----------------------------
if not df.empty:

    income = df[df["Type"] == "Income"]["Amount"].sum()
    expense = df[df["Type"] == "Expense"]["Amount"].sum()

    col1, col2 = st.columns(2)

    # 🔹 Bar Chart
    with col1:
        st.write("📊 Expense by Category")

        exp_df = df[df["Type"] == "Expense"]

        if not exp_df.empty:
            cat_data = exp_df.groupby("Category")["Amount"].sum().reset_index()

            fig1, ax1 = plt.subplots()
            sns.barplot(data=cat_data, x="Category", y="Amount", ax=ax1)
            plt.xticks(rotation=45)

            st.pyplot(fig1)

    # 🔹 Pie Chart
    with col2:
        st.write("🥧 Income vs Expense")

        fig2, ax2 = plt.subplots()
        ax2.pie([income, expense],
                labels=["Income", "Expense"],
                autopct='%1.1f%%')

        st.pyplot(fig2)

    # 🔹 Distribution
    st.write("📈 Expense Distribution")

    exp_df = df[df["Type"] == "Expense"]

    if not exp_df.empty:
        fig3, ax3 = plt.subplots()
        sns.histplot(exp_df["Amount"], kde=True, ax=ax3)
        st.pyplot(fig3)

else:
    st.info("👉 Please add some data to see graphs")
