import seaborn as sns
sns.set_style("darkgrid")

st.subheader("📊 Advanced Financial Dashboard")

if not df.empty:

    expense_data = df[df["Type"] == "Expense"]

    col1, col2 = st.columns(2)

    # 🔹 BIG BAR CHART
    with col1:
        st.write("### Expense by Category")
        if not expense_data.empty:
            cat_data = expense_data.groupby("Category")["Amount"].sum().reset_index()

            fig1, ax1 = plt.subplots(figsize=(8,5))
            sns.barplot(data=cat_data, x="Category", y="Amount", ax=ax1)
            ax1.set_title("Expenses by Category", fontsize=14)

            st.pyplot(fig1)
        else:
            st.info("No expense data")

    # 🔹 BIG PIE CHART
    with col2:
        st.write("### Income vs Expense")

        fig2, ax2 = plt.subplots(figsize=(6,6))
        ax2.pie([income, expense],
                labels=["Income", "Expense"],
                autopct='%1.1f%%',
                startangle=90)
        ax2.set_title("Income vs Expense")

        st.pyplot(fig2)

    # 🔹 DISTRIBUTION GRAPH (LIKE YOUR IMAGE STYLE)
    st.write("### Expense Distribution")

    if not expense_data.empty:
        fig3, ax3 = plt.subplots(figsize=(10,5))

        sns.histplot(expense_data["Amount"], kde=True, ax=ax3)

        ax3.set_title("Expense Distribution Curve")

        st.pyplot(fig3)

else:
    st.info("Add data to see advanced charts")
