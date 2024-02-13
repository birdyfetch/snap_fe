import streamlit as st
from utils import (is_voucher_valid, register_user, is_email_valid, mark_voucher_as_used)
from dotenv import load_dotenv
load_dotenv()
def main():
    st.title("Welcome, AppSumo Users! Get Started with SnapVisite360")
    st.subheader("Elevate Your Virtual Tour Experience")


    # Initialize the session state keys if they don't exist
    if 'registration_success' not in st.session_state:
        st.session_state['registration_success'] = False
    for key in ['username', 'email', 'password', 'repeat_password', 'voucher_code']:
        if key not in st.session_state:
            st.session_state[key] = ''

    # Check if the user has already registered successfully
    if st.session_state['registration_success']:
        st.success("Your registration was successful, Congratulations!! Please check your email to validate your password and activate your account")
        st.balloons()  # Show balloons when registration is successful
        return  # Exit the function to prevent the form from being displayed again

    with st.form("registration_form"):
        username = st.text_input("Username", value=st.session_state['username'], placeholder="Enter your username")
        email = st.text_input("Email Address", value=st.session_state['email'], placeholder="Enter your email address")
        password = st.text_input("Password", value=st.session_state['password'], type="password", placeholder="Enter your password")
        repeat_password = st.text_input("Repeat Password", value=st.session_state['repeat_password'], type="password", placeholder="Repeat your password")
        voucher_code = st.text_input("Voucher Code", value=st.session_state['voucher_code'], placeholder="Enter your voucher code")

        submitted = st.form_submit_button("Register")

        if submitted:
            if not all([username, email, password, repeat_password, voucher_code]):
                st.error("All fields are required.", icon="🚫")
            elif not is_email_valid(email):
                st.error("Please enter a valid email address.", icon="⚠️")
            elif password != repeat_password:
                st.error("Passwords do not match.", icon="🚫")
            elif not is_voucher_valid(voucher_code):
                st.error("This voucher code is invalid or has already been used.", icon="🚫")
            else:
                response = register_user(username, email, password)
                
                if response['status'] == 'success':
                    mark_voucher_as_used(voucher_code)
                    # Set the session state to indicate successful registration
                    st.session_state['registration_success'] = True
                    # Clear the form fields
                    for key in ['username', 'email', 'password', 'repeat_password', 'voucher_code']:
                        st.session_state[key] = ''
                    # Rerun the app to reflect changes in the session state and clear the form
                    st.rerun()
                    st.success("Your registration was successful, Congratulations!! Please check your email to validate your password and activate your account")
                    st.balloons()  # Celebrate the successful registration
                else:
                    # Show a generic error message to the user
                    st.error(response['message'])

if __name__ == "__main__":
    main()
