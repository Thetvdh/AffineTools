from EncDec import encdec
from Cracker import cracker


def print_menu() -> int:
    while True:
        try:
            choice: int = int(input("Cracker or Encryption/Decryption (1,2)"))
            if choice == 1 or choice == 2:
                break
        except ValueError:
            print("Enter a value of 1 or 2")
    return choice


if __name__ == '__main__':

    match print_menu():
        case 1:
            cracker.main()
        case 2:
            encdec.main()
