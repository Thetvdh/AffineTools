from modules.util import mmi

class Affine:

    def __init__(self, plain: str, a: int, b: int) -> None:
        self.plain: str = plain.upper()
        self.a: int = a
        self.b: int = b
        self.decrypted: str = ""
        self.encrypted: str = ""

    def encrypt(self) -> None:
        for letter in self.plain:
            # Ignores all punctuation but keeps whitespace
            if letter.isalpha():
                alpha_pos = ord(letter) - ord('A')
                # Runs the encryption algorithm c=am+b
                self.encrypted += chr(((self.a * alpha_pos + self.b) % 26) + ord('A'))  # appends encrypted char to ciphertext
            elif letter.isspace():
                self.encrypted += letter
            else:
                continue

    def decrypt(self) -> None:
        self.decrypted = ""
        for letter in self.plain:
            # I chose to not add the punctuation stripper on decryption as punctuation could add useful context.
            if letter.isalpha():
                alpha_pos = ord(letter) - ord('A')
                # finds the modular multiplicative inverse. Then applies the decryption algorithm
                # m = inv(a)(c-b)
                self.decrypted += chr(mmi(self.a, 26) * (alpha_pos - self.b) % 26 + ord('A'))
            else:
                self.decrypted += letter

    def update_keys(self, a: int, b: int):
        self.a = a
        self.b = b

