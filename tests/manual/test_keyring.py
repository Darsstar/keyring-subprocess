import keyring

password = keyring.get_password(
    "keyring-subprocess",
    "'eyJtZXRob2QiOiAiZ2V0X3Bhc3N3b3JkIiwgInNlcnZpY2UiOiAiaHR0cHM6Ly9wa2dzLmRldi5henVyZS5jb20vTktJLUFWTC9fcGFja2FnaW5nL1JUL3B5cGkvc2ltcGxlLyIsICJ1c2VybmFtZSI6ICJWc3NTZXNzaW9uVG9rZW4ifQ=='",
)

print(password)
