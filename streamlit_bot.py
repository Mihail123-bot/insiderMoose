import streamlit as st

# Wallet address for payments
WALLET_ADDRESS = "GJYnbja54NLVqob7329eieZ5u7kTzgK85s36HYbNiBLd"

# Main Function
def main():
    # Page Title
    st.title("Welcome to Insider Moose Bot 🌟")

     # Display Discord link at the beginning
    st.markdown("### Join our Discord Community!")
    st.markdown("[Click here to join](https://discord.gg/63Fe5qnXGb)")

    
    # Initialize session state
    if "step" not in st.session_state:
        st.session_state.step = "welcome"
    if "selected_plan" not in st.session_state:
        st.session_state.selected_plan = None
    if "wallet_address" not in st.session_state:
        st.session_state.wallet_address = ""

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
        st.session_state.step = "plans"  # Navigate to the plans page

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

    # Buttons to select a plan
    if col1.button("Select Basic (0.1 SOL)"):
        st.session_state.selected_plan = "Basic (0.1 SOL)"
        st.session_state.step = "wallet"

    if col2.button("Select Basic (0.25 SOL)"):
        st.session_state.selected_plan = "Basic (0.25 SOL)"
        st.session_state.step = "wallet"

    if col3.button("Select Pro (1 SOL)"):
        st.session_state.selected_plan = "Pro (1 SOL)"
        st.session_state.step = "wallet"

# Wallet Input Page
def ask_for_wallet():
    st.subheader(f"You selected the {st.session_state.selected_plan} plan.")
    wallet_address = st.text_input("Please enter your wallet address for payment:", value=st.session_state.wallet_address)

    if st.button("Submit Wallet Address"):
        if wallet_address.strip():
            st.session_state.wallet_address = wallet_address.strip()
            st.session_state.step = "payment"  # Proceed to payment page
        else:
            st.error("Please enter a valid wallet address.")

# Payment Instructions Page
def show_payment_instructions():
    st.subheader(f"Thank you! You selected the {st.session_state.selected_plan} plan.")
    st.write(f"""
    ### Payment Details:
    Send **{st.session_state.selected_plan.split(' ')[1]} SOL** to the following wallet address:

    **{WALLET_ADDRESS}**

    After completing the payment, the order will be processed.
    """)

    col1, col2 = st.columns(2)
    if col1.button("Check Status"):
        st.info("Verification takes up to 24 hours.")
    if col2.button("Cancel"):
        # Reset all session state variables
        st.session_state.step = "welcome"
        st.session_state.selected_plan = None
        st.session_state.wallet_address = ""

# Run the App
if __name__ == "__main__":
    main()
