from Crypto.Random import get_random_bytes
from base64 import b64encode, b64decode
import pyaes

#key_r = get_random_bytes(22)
#key = b64encode(key_r) # len(key)=32 bytes
#print(key)
key = b'cdhtdvdfracdcdhtdvdfracddfrthvfe'
#print(len(key))
plaintext1 = 'helloobhfjkkggnnnvvvxfxfxdxdxdxfxf'
plaintext2= 'helloobhfjkvvxfxfxdxdxdx'
plaintext3 = 'helloobhfjkkggnnnvvaaaxfxdxdxdx'
#print(len(plaintext))
def encrypt(plaintext):
    ciphertext = pyaes.AESModeOfOperationCTR(key).encrypt(plaintext)
    print(ciphertext)
    return ciphertext

def decrypt(ciphertext):
    plaintext = pyaes.AESModeOfOperationCTR(key).decrypt(ciphertext)
    print(plaintext)
    print(plaintext.decode())
    return plaintext.decode()
ciphertext1 = encrypt(plaintext1)
ciphertext2 = encrypt(plaintext2)
ciphertext3 = encrypt(plaintext3)
ciphertext0 = b'\x90\xf3\xc6\xe5\x0f\xa4\xaa\xc1e"\xb2\xf8s\x94b\xc1V\xce \xe8['
decrypt(ciphertext0)
decrypt(ciphertext2)
decrypt(ciphertext3)
