import streamlit as st
import json
from cookie_utils import get_cookies

cookieManager = get_cookies()
cookie = cookieManager.get("loggedIn")
player = cookieManager.get("player")


st.markdown("""
<style>
/* Hide main menu */
#MainMenu {visibility: hidden;}

/* Hide footer */
footer {visibility: hidden;}

/* Hide header (Deploy button, etc.) */
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

if not "loggedIn" in st.session_state:
    st.session_state.loggedIn = False
try:
    if cookie:
        st.session_state.loggedIn = True
except:
    print("")

with open("balance.json", "r") as file:
    balanceData = json.load(file)

def sendBal(amount, toUser):
    if not amount > balance:
        try:
            balanceData[player] -= amount
            balanceData[toUser] += amount
            with open("balance.json", "w") as file:
                json.dump(balanceData, file, indent=4)
        except:
            st.warning("The user doesn't exist")
    else:
        st.warning("The balance is less then send amount!")

if not st.session_state.loggedIn == False:
    balance = balanceData[player]
    st.title("Welcome to Bank transfer!")
    st.text(f"Balance: {balance}")
    st.divider()
    userToSendTo = st.text_input("User to send to:")
    amount = st.number_input("Amount to send:")
    if st.button("Send"):
        sendBal(amount, userToSendTo)
else:
    st.warning("You're not logged in, please log in first!")