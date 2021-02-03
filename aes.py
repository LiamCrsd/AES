import Modules.aes_dec as dec
import Modules.aes_enc as enc
from Modules.convert import *

def encrypt(text, key):

    mat_text = ascii_2_matrix(text)
    mat_key = key_2_matrix(key)
    res = enc.AES(mat_text, mat_key)
    return res

def decrypt(text, key):
    mat_key = key_2_matrix(key)
    if type(text) == str:
        mat_text = ascii_2_matrix(text)
    else:
        mat_text = text
    res = dec.InvAES(mat_text,mat_key)
    return matrix_2_ascii(res)
