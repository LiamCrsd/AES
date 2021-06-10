# AES python script
AES-128bits encryption program code with a classic block cipher mode of operation. 


The program allows encryption/decryption of a text (converted using the ascii table) given using a 128-bit key. 

Added :
- Choice between ECB and CBC cipher mode of operation.
- Begin of utf-8 (first 256 character).
- Encryption and decryption of an image. 
- Now supports utf-8.
- Addition of the GCM cipher mode of operation.
- Ability to encrypt images and text files directly

Planned :
- Encryption/decryption for a key of 192/256bits.

# Overview 

``` python
from AES import *

text = "This is a message to encrypt"
key = "The 128-bits key"

res = encrypt(text, key, "ECB")

dec_text = decrypt(res, key, "ECB") #It's the same key

res2 = enc_im("your_image.png",key,"ECB")

dec_im("res2,key,"ECB","name_decrypt_image.png")
``` 

# Copyright 

The program is completely free of rights whatever the use, private or public.
