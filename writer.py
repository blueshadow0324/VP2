import json

data = [
    "PLAYER1",
    "PLAYER2",
]

passwords = {
    "PLAYER1": "PASSWORD"
}

balances = {
    "PLAYER1": 100
}

#with open("player.json", "w") as file:
    #json.dump(data, file, indent=4)
#with open("password.json", "w") as file:
    #json.dump(passwords, file, indent=4)
with open("balance.json", "w") as file:
    json.dump(balances, file, indent=4)