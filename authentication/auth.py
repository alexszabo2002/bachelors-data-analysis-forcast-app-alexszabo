import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st


def get_authenticator():

    with open('./authentication/config.yaml') as file:
        config = yaml.load(file, Loader=SafeLoader)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days']  
    )

    authenticator.login()

    if st.session_state["authentication_status"] is False:
        st.error('Incorrect username/password')
        st.stop()
    elif st.session_state["authentication_status"] is None:
        st.warning('Please enter your username and password')
        st.stop()

    return authenticator
