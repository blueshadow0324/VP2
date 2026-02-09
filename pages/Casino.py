import streamlit as st
import json
import random
from cookie_utils import get_cookies

cookieManager = get_cookies()
cookie = cookieManager.get("loggedIn")
player = cookieManager.get("player")

try:
    if cookie:
        st.session_state.loggedIn = True
except:
    print("")

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
if not "casinoClick" in st.session_state:
    st.session_state.casinoClick = False
if not "casinoState" in st.session_state:
    st.session_state.casinoState = ""

with open("balance.json", "r") as file:
    balanceData = json.load(file)

def hideButton(input):
    st.session_state.casinoState = input
def roll(amount, player, tryNumber):
    rightNumber = random.randint(1, 6)
    if rightNumber == tryNumber:
        balanceData[player] += amount*5
        st.warning(f"You guessed the right number is was {tryNumber}")
    else:
        balanceData[player] -= amount
        st.warning(f"You guessed wrong the right number was {rightNumber} and you geussed {tryNumber}")
    with open("balance.json", "w") as file:
        json.dump(balanceData, file, indent=4)

if not st.session_state.loggedIn == False:
    balance = balanceData[player]
    st.title("Welcome to the casino!")
    st.text(f"Balance:{balance}")
    st.divider()
    if st.session_state.casinoState == "dice":
        st.text("Pick a number between 1-6! If you guess right you will get 6x the amount.")
        guess = st.slider("Input the guessing number:", 1, 6)
        amount = st.number_input("Enter amount to gamble:")
        st.button("Gamble!", on_click=lambda: roll(player=player, amount=amount, tryNumber=guess))
    elif st.session_state.casinoState == "jackpot":
        st.text("Jackpot")
    else:
        st.button("Dice", on_click=lambda: hideButton("dice"))
        st.button("Jackpot", on_click=lambda: hideButton("jackpot"))
else:
    st.warning("You're not logged in, please log in first!")