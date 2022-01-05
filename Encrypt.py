import hashlib

from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
key_r = get_random_bytes(22)
key = b64encode(key_r) # len(key)=32 bytes
print(key)
plaintext = 'Hello'

def encrypt(plaintext):
    cipher = AES.new(key, AES.MODE_CBC)
    ciphertext = cipher.encrypt(pad(plaintext, AES.block_size))
    with open("cipher_file","wb") as c_file:
        c_file.write(cipher.iv)
        c_file.write(key)
    print(cipher.iv)
    return (b64encode(ciphertext))
#a =encrypt(plaintext.encode())

#print(a)
def a(string):
#    print(len(string))
    encoded = string.encode()
    result1 = hashlib.sha256(encoded)
    a = result1.hexdigest()
    print(type(a))
    print(a) #hash
a("abc")