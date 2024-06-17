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
                'date',
                'time',
                'category',
                'type',
                'amount',
                'transaction_type',
                'description'
            ]
        )


def save_data(df):
    """Save transactions data to CSV file"""
    df.to_csv(DATA_FILE, index=False)


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
                'Selectionner Une Catégorie',
                'Airtel Money',
                'Moov Money',
                'Canal +',
                'Recette Journalière'
            ]
        )
    with col2:
        # The transaction amount
        amount = st.number_input('Montant', min_value=0.0, step=1.00)
    with col3:
        if category == 'Airtel Money' or category == 'Moov Money':
            type_ = st.selectbox('Type', ['Dépôt', 'Retrait'])
            if type_ == 'Dépôt':
                transaction_type = '⬇️'
            else:
                transaction_type = '⬆️'
        elif category == 'Canal +':
            type_ = st.selectbox('Type', ['Abonnement', 'Achat de Kits'])
            transaction_type = '⬇️'
        elif category == 'Recette Journalière':
            type_ = st.selectbox(
                'Type',
                ['Secretariat', 'Transfert Airtel', 'Transfert Moov']
            )
            transaction_type = '⬇️'
        else:
            # The transaction type, income or outgo (expense)
            # type_ = st.selectbox('Type', ['income', 'expense'])
            type_ = st.selectbox('Type', [''])

    # Description of the transaction
    description = st.text_input('Description')

    # If a category/type is not yet select or the amount is 0
    if (
        category == 'Selectionner Une Catégorie' or
        amount == 0.0 or type_ == ''
    ):
        # Disable the add transaction button
        st.button(
            'Ajouter Transaction',
            disabled=st.session_state.get("disabled", True)
        )
    else:
        # If the add transaction add button is pressed
        if st.button('Ajouter Transaction'):
            # Set transaction date and time to the current datetime
            date = datetime.now().date()
            time = datetime.now().time().strftime('%H:%M')

            # Create a new transaction dataframe with the provided infomations
            new_transaction = pd.DataFrame(
                [
                    [
                        date,
                        time,
                        category,   
                        type_,
                        amount,
                        transaction_type,
                        description
                    ]
                ],
                columns=[
                    'date',
                    'time',
                    'category',
                    'type',
                    'amount',
                    'transaction_type',
                    'description'
                ]
            )
            # Load existing transaction data
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
    total_income = data[data['transaction_type'] == '⬇️']['amount'].sum()
    total_expense = data[data['transaction_type'] == '⬆️']['amount'].sum()
    profit = total_income - total_expense

    # Display the computed values
    col1, col2, col3 = st.columns(3)
    col1.metric('RevenuTotal', f"{total_income:.2f} FCFA")
    col2.metric('Dépense Totale', f"{total_expense:.2f} FCFA")
    col3.metric('Profit', f"{profit:.2f} FCFA", f"{profit} FCFA")

    # Transaction history section
    st.subheader('Historique des Transactions')
    st.dataframe(data)


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
        elif password == '':
            st.warning('Veillez entrer votre mot de passe.', icon="⚠️")
        else:
            st.error('Mot de passe incorrect!', icon='❌')


# Make sure that the file is running as a script
if __name__ == '__main__':
    main()
