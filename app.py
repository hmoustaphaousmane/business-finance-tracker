import streamlit as st
import pandas as pd

from datetime import datetime


DATA_FILE = 'db/transactions.csv'

# Load transactions from CSV file
def load_data():
    """Load transactions data from CSV file"""
    try:
        # Read and load data from file (if exists)
        return pd.read_csv(DATA_FILE, parse_dates=['date'])
    except FileNotFoundError:
        # If a FileNotFoundError is raised, create and return a new pandas
        # dataframe with the specified columns
        return pd.DataFrame(
            columns=[
                'date', 'time', 'category', 'description', 'amount', 'type'
            ]
        )

def save_data(df):
    """Save transactions data to CSV file"""
    df.to_csv(DATA_FILE, index=False)

def main():
    """Entry point of the program"""
    # Title of the app
    st.title('Gestion des transactions')

    # Sidebar for navigation
    role = st.sidebar.selectbox('Select your role', ['Gérant', 'Admin'])

    # If the user is a manager,
    if role == 'Gérant':
        # Dipslay the manager space
        manager_space()
    # Otherwise, is the user is an Admin
    elif role == 'Admin':
        # Require password
        password = st.sidebar.text_input(
            'Enter admin password',
            type='password',
            # place_holder='Enter an admin password here'
        )
        # Verify the password
        if password == 'adminpassword':  # Replace with a secure method
            # If the password is correct, display the admin space
            admin_space()
        else:
            st.error('Mot de passe incorrect!')

def manager_space():
    """Define the Manager space"""
    st.header('Espace Gérant')
    st.subheader('Ajouter des Nouvelles Transactions')
    
    # New Transaction registration form
    col1, col2, col3 = st.columns(3)
    with col1:
        # Category field, this could be any service that the business provides
        category = st.selectbox(
            'Categorie',
            [
                'airtel money',
                # 'moov money',
                'abonnement canal +',
                # 'transfert credit (aiftel, moov)'
            ]
        )
    with col2:
        # The transaction amount
        amount = st.number_input('Montant', min_value=0.0, step=1.00)
    with col3:
        # Thr transaction type, income or outgo (expense)
        type_ = st.selectbox('Type', ['income', 'expense'])
    
    # Description of the transaction
    description = st.text_input('Description')
    
    # Transaction add button, if the button is pressed
    if st.button('Ajouter Transaction'):
        # Automatically set transaction date and time to the current datetime
        date = datetime.now().date()
        time = datetime.now().time().strftime('%H:%M:%S')

        # Create a new transaction dataframe with the provided infomations
        new_transaction = pd.DataFrame(
            [
                [date, time, category, description, amount, type_]
            ],
            columns=[
                'date', 'time', 'category', 'description', 'amount', 'type'
            ]
        )
        # Load transaction data
        data = load_data()

        # Append the new transaction to the existing data
        data = pd.concat([data, new_transaction], ignore_index=True)

        # Save
        save_data(data)

        st.success('Transaction ajouter avec success!')

    # Transaction history section
    st.subheader('Historique des Transactions')
    data = load_data()
    st.dataframe(data)

def admin_space():
    """Define an Admin's space"""
    st.header('Admin Space')
    
    # Statistics section
    st.subheader('Statistics')
    # Load the data
    data = load_data()

    # If there is no data yet
    if data.empty:
        # Display a wornig message
        st.warning('No transactions to show.')
        return

    # Compute income, expense and profit
    total_income = data[data['type'] == 'income']['amount'].sum()
    total_expense = data[data['type'] == 'expense']['amount'].sum()
    profit = total_income - total_expense

    # Display the computed values
    st.metric('RevenuTotal', f"${total_income:.2f}")
    st.metric('Dépense Totale', f"${total_expense:.2f}")
    st.metric('Profit', f"${profit:.2f}")

    # Transaction history section
    st.subheader('Historique des Transactions')
    st.dataframe(data)

if __name__ == '__main__':
    main()