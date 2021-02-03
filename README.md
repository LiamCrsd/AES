# AES
AES-128bits encryption program code with a classic block cipher mode of operation. 


The program allows encryption/decryption of a text (converted using the ascii table) given using a 128-bit key. 

Planned :
- Encryption/decryption for a key of 192/256bits.
- Choice between ascii and utf-8
- Different block cipher mode of operation

# Overview 

``` python
from AES import *

text = "This is a message to encrypt"
key = "The 128-bits key"

enc_mat = encrypt(text, key)

enc_text = text2matrix(enc_mat) #It is better to leave the encrypted message in matrix form 
                                #because by converting it into text some characters will not be recognized.

dec_text = decrypt(enc_mat, key) #It's the same key
``` 

