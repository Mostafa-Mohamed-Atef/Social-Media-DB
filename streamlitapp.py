import streamlit as st
import backend




# Streamlit application

st.sidebar.title("Instagram")
page = st.sidebar.radio("Navigation", ("register", "login"))

if  page == 'register':
    st.title("Instagram Sign Up")
    fname = st.text_input("First Name")
    lname = st.text_input("Last Name")
    profile_name = st.text_input("Profile Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    bio = st.text_area("Bio")
    account_type = st.radio("Account Type", ("regular", "business"))

    if st.button("Sign Up"):
        if fname and lname and profile_name and email and password and bio and account_type:
            backend.create_user(fname, lname, profile_name, email, password, bio, account_type)
            st.success("User signed up successfully!")
        else:
            st.error("Please fill all the fields.")


elif page == 'login':
    st.title("Instagram Login")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if email and password:
            user = backend.authenticate_user(email, password)
            if user:
                st.success("User authenticated successfully!")
            else:
                st.error("Invalid email or password.")
        else:
            st.error("Please fill all the fields.")