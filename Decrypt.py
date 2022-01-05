from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from base64 import b64encode, b64decode
import hashlib
ciphertextt = b'8cugxNNa7vQf021sqFZMVw=='
ciphertext = b64decode(ciphertextt)
def decrypt(ciphertext):
    with open("cipher_file","rb") as c_file:
        iv = c_file.read(16)
        key = c_file.read()

    cipher = AES.new(key, AES.MODE_CBC,iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

#a = decrypt(ciphertext)
#print(a)

def a(string):
#    print(len(string))
    encoded = string.encode()
    result1 = hashlib.sha256(encoded)
    a = result1.hexdigest()
    print(type(a))
    print(a) #hash
a("abc")
