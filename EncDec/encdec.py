from modules.Affine import Affine
from modules.util import is_coprime

def menu() -> dict:
    print("AFFINE CIPHER || ENCRYPT / DECRYPT")
    settings: dict = {}
    mode: str = ''
    while mode != "e" and mode != "d":
        mode = input("Encryption or Decryption (e, d): ").lower()

    while True:  # While loop to continually ask until valid information has been given
        try:
            key_a: int = int(input("Enter key a: "))
            if is_coprime(key_a, 26) and key_a < 26:
                break
            else:
                print("Enter an integer that is a coprime of 26")
        except ValueError:
            print("Enter an integer that is a coprime of 26")
    while True:
        try:
            key_b: int = int(input("Enter key b: "))
            break
        except ValueError:
            print("Enter a integer")

    prompt = "Enter plaintext: " if mode == 'e' else "Enter ciphertext: "
    text = input(prompt)
    settings["mode"] = mode
    settings["keya"] = key_a
    settings["keyb"] = key_b
    settings["text"] = text
    # Settings stores the information to encrypt or decrypt the affine
    return settings



def main():
    settings: dict = menu()
    algo: Affine = Affine(settings["text"], settings["keya"], settings["keyb"])
    if settings["mode"] == 'e':
        algo.encrypt()
    else:
        algo.decrypt()

    print(f"Ciphertext: {algo.encrypted}" if settings["mode"] == 'e' else f"Decrypted: {algo.decrypted}")
