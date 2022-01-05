import hashlib
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
import binascii
string = "pythonpool.com"
print(len(string))
encoded = string.encode()
result1 = hashlib.sha256(encoded)
a= result1.hexdigest()
print(type(a))
print(a) #hash
#print(len(a))

key_Private = RSA.generate(3072) #4096
key_Public = key_Private.publickey()
print(f"Public key:  (n={hex(key_Public.n)}, e={hex(key_Public.e)})")
#pubKeyPEM = pubKey.exportKey()
#print(pubKeyPEM.decode('ascii'))
print(f"Private key: (n={hex(key_Public.n)}, d={hex(key_Private.d)})")
#privKeyPEM = keyPair.exportKey()
#print(privKeyPEM.decode('ascii'))
b = bytes(a, 'utf-8')
encryptor = PKCS1_OAEP.new(key_Public)
encrypted = encryptor.encrypt(b)
print("Encrypted:", binascii.hexlify(encrypted))

decryptor = PKCS1_OAEP.new(key_Private)
decrypted = decryptor.decrypt(encrypted)
print('Decrypted:', decrypted.decode('utf-8'))

