
def get_key():
    with open("key.txt", "r") as keyFile:
        return keyFile.read()