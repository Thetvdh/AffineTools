import re  # Module for regular expressions, used in checking plaintexts against a wordlist
import sys

from tqdm import tqdm  # Used for the progress bar in the wordlist checker

from modules.Affine import Affine  # Custom Class import
from modules.util import is_coprime  # Custom function import


def get_ciphertext() -> str:
    return input("Enter the ciphertext to be cracked: ").upper()  # Simply returns the value inputted by the user



def brute_force_all_keys(ctext: str) -> dict:
    allowed_keys = [i for i in range(1, 26) if is_coprime(i, 26)]  # Generates a list of valid allowed keys for A
    decrypter = Affine(ctext, 1, 0)  # Creates the instance of the class Affine to allow for decryption
    output_plaintexts = {}
    """
    Brute force attack of the Affine Cipher
    x and y are the keys in the cipher
    
    m = inv(a) * (c - b) % 26
    
    This is then outputted into a dictionary with the key: value pair being structured the key is the decrypted
    plaintext and the value is a tuple containing the two keys used to get that output.
    """
    for x in allowed_keys:  # Loop through every possible value for Key A
        for y in range(1, 26):  # Loop through every possible value for Key B
            decrypter.update_keys(x, y)
            decrypter.decrypt()
            output_plaintexts[decrypter.decrypted] = (x, y)

    return output_plaintexts



def quadgram_analysis(texts: list) -> list:
    quadgram_dict = {}
    with open("quadgrams.txt", "r") as quadgrams:
        for line in quadgrams:
            data = line.split(" ")
            quadgram_dict[data[0].replace("\n", "")] = int(data[1])
    score_dict = {}

    # set all scores to 0
    for text in texts:
        score_dict[text] = 0

    # compares each set of 4 letters in the text to the quadgrams
    for text in texts:
        for i in range(len(text) - 4 + 1):
            if text[i: i + 4] in quadgram_dict.keys():
                score_dict[text] += quadgram_dict[text[i: i + 4]]

    sorted_list = sorted(score_dict.items(), key=lambda i: i[1],
                         reverse=True)  # Sorts list so the highest values are at the top

    return sorted_list[0:5]  # returns top 5 outputs




def check_dictionary(likely_plaintexts: list) -> list:
    plaintexts = [word[0] for word in likely_plaintexts]
    ret_list = []
    with open("words", "r") as word_file:
        words = word_file.read().split("\n")
        words = [word.upper() for word in words]
        num_words = len(words)

        # Loop through every word in the words file
        for word in tqdm(words, total=num_words, unit="word"):
            for plain in plaintexts:
                match = re.search(fr"{word}", plain)  # check if the word is in the string
                if match:
                    ret_list.append(plain)  # add the plaintext if a word exists in it

        return list(dict.fromkeys(ret_list))


# Mixed Contribution
def main() -> None:
    ciphertext = get_ciphertext()
    plaintexts = brute_force_all_keys(ciphertext)  # gets a list of plaintexts
    likely_plaintexts = quadgram_analysis(list(plaintexts.keys()))  # converts to a list for simplicity sake
    if likely_plaintexts:
        print("These are the most likely plaintexts")
        for text in likely_plaintexts:
            print(f"Decrypted: {text[0]} | Keys: {plaintexts[text[0]]}")
        choice = input(
            "Would you like to attempt to reduce this further by comparing against a dictionary? Y/N: ").upper()
        if choice == 'Y':
            ret_list = check_dictionary(likely_plaintexts)
            print("These decoded cipher texts contain words in the dictionary:")
            for item in ret_list:
                print(f"{item} | Keys: {plaintexts[item]}")

        print("Exiting the cracker...")
        sys.exit(0)
