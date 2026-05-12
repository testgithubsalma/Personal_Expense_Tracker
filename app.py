import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# =========================
# PAGE CONFIGURATION
# =========================

st.set_page_config(
    page_title="Personal Expense Tracker",
    page_icon="💰",
    layout="wide"
)

# =========================
# FILE SETUP
# =========================

FILE_NAME = "expenses.csv"

# Create CSV file if not exists
if not os.path.exists(FILE_NAME):

    empty_df = pd.DataFrame(columns=[
        "Type",
        "Category",
        "Amount",
        "Date",
        "Description"
    ])

    empty_df.to_csv(FILE_NAME, index=False)

# Load existing data
df = pd.read_csv(FILE_NAME)

# =========================
# SIDEBAR
# =========================

st.sidebar.title("💰 Navigation")

page = st.sidebar.radio(
    "Go To",
    [
        "Home",
        "Add Transaction",
        "View Transactions",
        "Summary"
    ]
)

# =========================
# HOME PAGE
# =========================

if page == "Home":

    st.title("💸 Personal Expense Tracker")

    st.write(
        "This application helps users track income and expenses easily."
    )

    st.markdown("## Features")

    st.markdown("""
- Add Income
- Add Expenses
- View Transactions
- Download Transactions
- Financial Summary
- Expense Charts
""")

# =========================
# ADD TRANSACTION
# =========================

elif page == "Add Transaction":

    st.title("➕ Add Transaction")

    transaction_type = st.selectbox(
        "Transaction Type",
        ["Income", "Expense"]
    )

    # Category
    if transaction_type == "Income":

        category = st.text_input(
            "Income Source"
        )

    else:

        category = st.selectbox(
            "Expense Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Education",
                "Medical",
                "Others"
            ]
        )

    # Amount
    amount = st.number_input(
        "Enter Amount",
        min_value=0.0,
        step=1.0
    )

    # Date
    transaction_date = st.date_input(
        "Select Date"
    )

    # Description
    description = st.text_area(
        "Description"
    )

    # Save Button
    if st.button("Save Transaction"):

        new_data = pd.DataFrame([{
            "Type": transaction_type,
            "Category": category,
            "Amount": amount,
            "Date": transaction_date,
            "Description": description
        }])

        # Append data
        df = pd.concat(
            [df, new_data],
            ignore_index=True
        )

        # Save CSV
        df.to_csv(FILE_NAME, index=False)

        st.success("✅ Transaction Added Successfully!")

# =========================
# VIEW TRANSACTIONS
# =========================

elif page == "View Transactions":

    st.title("📋 Transaction History")

    if df.empty:

        st.warning("No transactions found.")

    else:

        st.dataframe(
            df,
            use_container_width=True
        )

        # Download button
        csv = df.to_csv(index=False)

        st.download_button(
            label="⬇ Download CSV",
            data=csv,
            file_name="transactions.csv",
            mime="text/csv"
        )

# =========================
# SUMMARY PAGE
# =========================

elif page == "Summary":

    st.title("📊 Financial Summary")

    if df.empty:

        st.warning("No data available.")

    else:

        # Income and Expense Data
        income_df = df[df["Type"] == "Income"]

        expense_df = df[df["Type"] == "Expense"]

        # Calculations
        total_income = income_df["Amount"].sum()

        total_expense = expense_df["Amount"].sum()

        balance = total_income - total_expense

        # Metrics
        col1, col2, col3 = st.columns(3)

        col1.metric(
            "💰 Total Income",
            f"₹ {total_income}"
        )

        col2.metric(
            "💸 Total Expense",
            f"₹ {total_expense}"
        )

        col3.metric(
            "🏦 Balance",
            f"₹ {balance}"
        )

        # Category Summary
        if expense_df.empty:

            st.info("No expense data available.")

        else:

            st.subheader("📂 Category-wise Expense Summary")

            category_summary = (
                expense_df.groupby("Category")["Amount"]
                .sum()
                .reset_index()
            )

            st.dataframe(
                category_summary,
                use_container_width=True
            )

            # Bar Chart
            st.subheader("📊 Expense Bar Chart")

            st.bar_chart(
                category_summary.set_index("Category")
            )

            # Pie Chart
            st.subheader("🥧 Expense Distribution")

            fig, ax = plt.subplots()

            ax.pie(
                category_summary["Amount"],
                labels=category_summary["Category"],
                autopct="%1.1f%%"
            )

            ax.axis("equal")

            st.pyplot(fig)