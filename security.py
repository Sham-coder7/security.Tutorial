import streamlit as st
import string
import random
#<style>
page_bg ="""
<style>
.stApp {
    background-color: #CCB693 ;
    color: #000000;
    
    }
div.stButton > button {
    background-color :#5E3D20 ;
    color:white ;
    padding: 0.6rem 1.2rem;
    border-radius: 10px;
    font-size: 16px;
}
div.stTextInput > label, div.stTextArea > label, div.stSelectbox > label {
    color: #381D03 ;
}
</style> """

st.markdown(page_bg, unsafe_allow_html=True)

st.title("🔐 Encryption & Decryption Tool")
st.write("Choose a cipher method and mode.")

def caesar_encrypt(message, key):
    alphabet = string.ascii_lowercase
    result = ""
    for char in message.lower():
        if char in alphabet:
            result += alphabet[(alphabet.index(char) + key) % 26]
        else:
            result += char
    return result


def caesar_decrypt(message, key):
    return caesar_encrypt(message, -key)
                          
def otp_encrypt(message):
    key = "".join(chr(random.randint(0, 255)) for _ in message)
    encrypted = "".join(chr((ord(message[i]) + ord(key[i])) % 256) for i in range(len(message)))
    return encrypted, key


def otp_decrypt(cipher, key):
    decrypted = "".join(chr((ord(cipher[i]) - ord(key[i])) % 256) for i in range(len(cipher)))
    return decrypted

def playfair_prepare_text(text):
    text = text.lower().replace("j", "i")
    prepared = ""
    i = 0
    while i < len(text):
        a = text[i]
        b = text[i+1] if i+1 < len(text) else "x"

        if a == b:
            prepared += a + "x"
            i += 1
        else:
            prepared += a + b
            i += 2
    if len(prepared) % 2 != 0:
        prepared += "x"
    return prepared


def playfair_generate_key_matrix(key):
    key = key.lower().replace("j", "i")
    seen = set()
    matrix = []

    for char in key:
        if char not in seen and char.isalpha():
            seen.add(char)
            matrix.append(char)

    for char in string.ascii_lowercase.replace("j", ""):
        if char not in seen:
            seen.add(char)
            matrix.append(char)

    return [matrix[i:i+5] for i in range(0, 25, 5)]


def playfair_find(matrix, char):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row, col
    return None, None


def playfair_encrypt(message, key):
    matrix = playfair_generate_key_matrix(key)
    message = playfair_prepare_text(message)
    result = ""

    for i in range(0, len(message), 2):
        a, b = message[i], message[i+1]
        r1, c1 = playfair_find(matrix, a)
        r2, c2 = playfair_find(matrix, b)

        if r1 == r2:
            result += matrix[r1][(c1 + 1) % 5]
            result += matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:
            result += matrix[(r1 + 1) % 5][c1]
            result += matrix[(r2 + 1) % 5][c2]
        else:
            result += matrix[r1][c2]
            result += matrix[r2][c1]

    return result


def playfair_decrypt(message, key):
    matrix = playfair_generate_key_matrix(key)
    result = ""

    for i in range(0, len(message), 2):
        a, b = message[i], message[i+1]
        r1, c1 = playfair_find(matrix, a)
        r2, c2 = playfair_find(matrix, b)

        if r1 == r2:
            result += matrix[r1][(c1 - 1) % 5]
            result += matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:
            result += matrix[(r1 - 1) % 5][c1]
            result += matrix[(r2 - 1) % 5][c2]
        else:
            result += matrix[r1][c2]
            result += matrix[r2][c1]

    return result

message = st.text_area("Enter your message:")

cipher_choice = st.selectbox(
    "Choose Cipher Method:",
    ["Caesar Cipher", "One-Time Pad", "Playfair Cipher"]
)

mode_choice = st.selectbox(
    "Choose Mode:",
    ["Encrypt", "Decrypt"]
)

if cipher_choice == "Caesar Cipher":
    key = st.number_input("Enter key (1–25):", min_value=1, max_value=25, step=1)

elif cipher_choice == "Playfair Cipher":
    playfair_key = st.text_input("Enter Playfair key (letters only):")


if st.button("Run"):

    # ----------------- Caesar -----------------
    if cipher_choice == "Caesar Cipher":
        if mode_choice == "Encrypt":
            result = caesar_encrypt(message, key)
        else:
            result = caesar_decrypt(message, key)

        st.subheader("Result:")
        st.code(result)

    # ----------------- OTP -----------------
    elif cipher_choice == "One-Time Pad":

        if mode_choice == "Encrypt":
            encrypted, otp_key = otp_encrypt(message)
            st.subheader("Encrypted Message:")
            st.code(encrypted)

            st.subheader("OTP Key:")
            st.code(otp_key)

        else:
            otp_key = st.text_input("Enter OTP Key:")
            if otp_key:
                decrypted = otp_decrypt(message, otp_key)
                st.subheader("Decrypted Message:")
                st.code(decrypted)
            else:
                st.error("Please enter the OTP key.")

    # ----------------- Playfair -----------------
    elif cipher_choice == "Playfair Cipher":
        if not playfair_key:
            st.error("Please enter a Playfair key.")
        else:
            if mode_choice == "Encrypt":
                result = playfair_encrypt(message, playfair_key)
            else:
                result = playfair_decrypt(message, playfair_key)

            st.subheader("Result:")
            st.code(result)
