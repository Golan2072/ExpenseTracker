import streamlit as st
import pandas as pd
from datetime import date
import database
import os
import matplotlib.pyplot as plt

def pie_chart(data, title):
    fig, ax = plt.subplots()
    ax.pie(data, labels=data.index, autopct="%1.1f%%", startangle=90)
    ax.set_ylabel("")
    ax.set_title(title)
    st.pyplot(fig)

if __name__ == "__main__":
    if os.path.exists("expense_base.db"):
        pass
    else:
        database.create_database()

    st.set_page_config(page_title="Expense Tracker",
                       page_icon=":chart_with_upwards_trend:", layout="wide")
    st.title("Expense Tracker")
    st.write("To best manage one's expenses.")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        ["Input Expense", "Input Income", "Balances", "Category Analysis", "Anual Analysis"])

    with tab1:
        st.header("Input Expense")
        with st.form("Input Expense", clear_on_submit=True):
            st.write("Please input your expense.")
            expense_description = st.text_input("Expense Description")
            expense_sum = st.number_input(
                "Amount (₪)", min_value=0.00, format="%.2f")
            expense_category = st.selectbox("Expense Type", [
                                            "Business", "Taxes and Pension", "Commissions and Loan", "House Maintenance", "Travel", "Grocery", "Health", "Telecom", "Subscriptions", "Clothing", "Eating Outside", "Misc", "Previous Undertakings"])
            payment_method = st.selectbox(
                "Payment Method", ["Bank Account", "Cash", "Credit Card", "PayPal"])
            expense_date = st.date_input(
                "Date", value=date.today(), max_value=date.today())
            submitted = st.form_submit_button("Input Expense")
            if submitted:
                database.insert_expense(
                    expense_description, expense_sum, expense_category, payment_method, expense_date)
            else:
                pass

    with tab2:
        st.header("Input Income")
        with st.form("Input Income", clear_on_submit=True):
            st.write("Please input your income.")
            income_description = st.text_input("Income Description")
            income_sum = st.number_input(
                "Amount (₪)", min_value=0.00, format="%.2f")
            income_category = st.selectbox("Income Type", [
                                           "Business", "Benefits", "Tax Rebate", "Miscellaneous"])
            income_date = st.date_input(
                "Date", value=date.today(), max_value=date.today())
            submitted = st.form_submit_button("Input Expense")
            if submitted:
                database.insert_income(
                    income_description, income_sum, income_category, income_date)
            else:
                pass

    with tab3:
        st.header("Balances")
        expense_dataframe = database.expenses_dataframe()
        income_dataframe = database.incomes_dataframe()
        balance = income_dataframe["sum"].sum() - expense_dataframe["sum"].sum()
        business_balance = (income_dataframe.loc[income_dataframe["type"] == "Business", "sum"].sum() - expense_dataframe.loc[expense_dataframe["type"] == "Business", "sum"].sum())
        st.write(f"Total Monthly Expenses: {expense_dataframe["sum"].sum()}₪")
        st.write(f"Total Monthly Incomes: {income_dataframe["sum"].sum()}₪") 
        if balance < 0:
            st.markdown(f"Monthly Balance: :red[{balance}₪]")
        else:
            st.write(f"Monthly Balance: {balance}₪")
        if business_balance < 0:
            st.markdown(f"Monthly Business Balance: :red[{business_balance}₪]")
        else:
            st.markdown(f"Monthly Business Balance: {business_balance}₪")
        st.divider()
    
    with tab4:
        expense_dataframe = database.expenses_dataframe()
        income_dataframe = database.incomes_dataframe()
        st.header("Category Analysis")
        st.write("Last Month Expenses by Category:")
        expenses_by_category = expense_dataframe.groupby("type")["sum"].sum().sort_values(ascending=False)
        for type, total in expenses_by_category.items():
            st.write(f"{type}: ₪{total:,.2f}")
        pie_chart(expenses_by_category, "Expenses by Category")
        st.divider()
        st.write("Last Month Incomes by Category")
        incomes_by_category = income_dataframe.groupby("type")["sum"].sum().sort_values(ascending=False)
        for type, total in incomes_by_category.items():
            st.write(f"{type}: ₪{total:,.2f}")
        pie_chart(incomes_by_category, "Incomes by Category")

    with tab5:
        expenses_dataframe_annual = database.expenses_dataframe_annual()
        incomes_dataframe_annual = database.incomes_dataframe_annual()
        st.header("Anual Analysis")
        st.write("Last Year Expenses by Category:")
        expenses_by_category = expenses_dataframe_annual.groupby("type")["sum"].sum().sort_values(ascending=False)
        for type, total in expenses_by_category.items():
            st.write(f"{type}: ₪{total:,.2f}")
        pie_chart(expenses_by_category, "Annual Expenses by Category")
        st.divider()
        st.write("Last Year Incomes by Category")
        incomes_by_category = incomes_dataframe_annual.groupby("type")["sum"].sum().sort_values(ascending=False)
        for type, total in incomes_by_category.items():
            st.write(f"{type}: ₪{total:,.2f}")
        pie_chart(incomes_by_category, "Annual Incomes by Category")
