import streamlit as st
import extra_streamlit_components as stx

def get_cookie_manager():
    return stx.CookieManager()

def get_cookies():
    manager = get_cookie_manager()
    cookies = manager.get_all()

    if cookies is None:
        st.stop()

    return manager
