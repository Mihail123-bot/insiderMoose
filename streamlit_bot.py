import streamlit as st

# Global Variables
WALLET_ADDRESS = "EdFcVXCxo2c5VBi1FY4UAhuW9VhyM2S9uu3BRY9Whcj4"

# Main Function
def main():
    # Page Title
    st.title("Welcome to Insider Moose Bot 🌟")

    # Session State Initialization
    if "step" not in st.session_state:
        st.session_state.step = "welcome"
    if "selected_plan" not in st.session_state:
        st.session_state.selected_plan = None
    if "wallet_address" not in st.session_state:
        st.session_state.wallet_address = None

    # Steps Logic
    if st.session_state.step == "welcome":
        show_welcome_page()
    elif st.session_state.step == "plans":
        show_plans_page()
    elif st.session_state.step == "wallet":
        ask_for_wallet()
    elif st.session_state.step == "payment":
        show_payment_instructions()

# Welcome Page
def show_welcome_page():
    st.subheader("Do not miss out on this crazy community and join now!")
    st.write("Just follow the instructions to complete the payment.")
    if st.button("Start Payment"):
        st.session_state.step = "plans"
        st.experimental_rerun()

# Plans Page
def show_plans_page():
    st.subheader("Please select a plan:")
    st.write("""
    ### ⚡️Basic: 0.1 SOL/month⚡️
    - High quality signals ✅
    - Late signals ✅
    - Access to private tools ❌
    - Access to private bots ❌
    - Early signals ❌

    ### ⚡️Basic: 0.25 SOL/month⚡️
    - High quality signals ✅
    - Late signals ✅
    - Access to private tools ✅
    - Access to private bots ❌
    - Early signals ❌

    ### ⚡️Pro: 1 SOL/month⚡️
    - High quality signals ✅
    - Late signals ✅
    - Access to private tools ✅
    - Access to private bots ✅
    - Early signals ✅
    - BONUS: Chatroom with whales and insiders ✅
    """)
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("Select Basic (0.1 SOL)"):
            st.session_state.selected_plan = "Basic (0.1 SOL)"
            st.session_state.step = "wallet"
            st.experimental_rerun()
    with col2:
        if st.button("Select Basic (0.25 SOL)"):
            st.session_state.selected_plan = "Basic (0.25 SOL)"
            st.session_state.step = "wallet"
            st.experimental_rerun()
    with col3:
        if st.button("Select Pro (1 SOL)"):
            st.session_state.selected_plan = "Pro (1 SOL)"
            st.session_state.step = "wallet"
            st.experimental_rerun()

# Wallet Input
def ask_for_wallet():
    st.subheader(f"You selected the {st.session_state.selected_plan} plan.")
    wallet_address = st.text_input("Please enter your wallet address for payment:")
    if wallet_address:
        st.session_state.wallet_address = wallet_address
        st.session_state.step = "payment"
        st.experimental_rerun()

# Payment Instructions
def show_payment_instructions():
    st.subheader(f"Thank you! You selected the {st.session_state.selected_plan} plan.")
    st.write(f"""
    ### Payment Details:
    Send **{st.session_state.selected_plan.split(' ')[1]} SOL** to the following wallet address:

    **{WALLET_ADDRESS}**

    After completing the payment, the order will be processed.
    """)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Check Status"):
            st.success("Payment verification is under construction.")
    with col2:
        if st.button("Cancel"):
            st.session_state.step = "welcome"
            st.session_state.selected_plan = None
            st.session_state.wallet_address = None
            st.experimental_rerun()

# Run App
if __name__ == "__main__":
    main()
