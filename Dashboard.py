import json
import streamlit as st
import time
from cookie_utils import get_cookies

cookieManager = get_cookies()

if not "step" in st.session_state:
    st.session_state.step = 1
if not "clicked" in st.session_state:
    st.session_state.clicked = False
if not "loggedIn" in st.session_state:
    st.session_state.loggedIn = False

try:
    cookie = cookieManager.get("loggedIn")
    player = cookieManager.get("player")
except:
    cookie, player = None
if not cookie == None:
    if not player == None:
        st.session_state.clicked = True
        st.session_state._submittedPlayer = cookieManager.get("player")
        player = cookieManager.get("player")
        st.session_state.loggedIn = True
        st.session_state.step = 3

st.title("Viggo Coin 2")

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

with open("player.json", "r") as file:
    playerData = json.load(file)
with open("password.json", "r") as file:
    passwordsData = json.load(file)
with open("balance.json", "r") as file:
    balanceData = json.load(file)

def hide_button(input):
    st.session_state.clicked = True
    if input == "login":
        st.session_state._stage = "login"
    else:
        st.session_state._stage = "register"
    st.session_state.step = 2

if not st.session_state.clicked:
    st.button("Login", on_click=lambda: hide_button("login"))
    st.button("Register", on_click=lambda: hide_button("register"))
if st.session_state.step == 2:
    if st.session_state._stage == "register":
        st.text("Register")
    else:
        st.text("Login")
    with st.form("FORM2"):
        player = st.text_input("Enter player:")
        password = st.text_input("Enter hidden Password")
        submit = st.form_submit_button("Enter")
        if submit:
            st.session_state._submittedPlayer = player
            st.session_state._submittedPassword = password
            st.session_state._process = True
if st.session_state.get("_process"):
    if not password == "":
        if st.session_state._stage == "register":
            match = False
            for key in playerData:
                if key == st.session_state._submittedPlayer:
                    match = True
            if match:
                st.warning("Player already has that name!")
            else:
                st.text("Success!")
                playerData.append(st.session_state._submittedPlayer)
                passwordsData[st.session_state._submittedPlayer] = st.session_state._submittedPassword
                balanceData[st.session_state._submittedPlayer] = 0
                with open("player.json", "w") as file:
                    json.dump(playerData, file, indent=4)
                with open("password.json", "w") as file:
                    json.dump(passwordsData, file, indent=4)
                with open("balance.json", "w") as file:
                    json.dump(balanceData, file, indent=4)
                st.session_state.step = 2
                st.session_state._process = False
                st.session_state._state = "login"
                st.rerun()
        else:
            match = False
            for key in playerData:
                if key == st.session_state._submittedPlayer:
                    match = True
            if match:
                if passwordsData[st.session_state._submittedPlayer] == st.session_state._submittedPassword:
                    st.session_state.step = 3
                    st.session_state._process = False
                    st.session_state.loggedIn = True
                    cookieManager.set(
                        "loggedIn",
                        "true",
                        key="login_cookie"
                    )
                    cookieManager.set(
                        "player",
                        st.session_state._submittedPlayer,
                        key="player_cookie"
                    )
                    player = st.session_state._submittedPlayer
                    time.sleep(0.5)
                    st.rerun()
            else:
                st.warning("No user found! Register an account.")
    else:
        st.warning("No password entered!")

if st.session_state.step == 3:
    player = cookieManager.get("player")
    try:
      balance = balanceData[player]
    except:
        if player == None:
            st.session_state.step = 2
            st.rerun()
        print(player, "Not found")
    st.text(f"Welcome, {player}!")
    st.text(f"Balance: {balance}")