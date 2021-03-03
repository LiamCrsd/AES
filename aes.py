import Modules.aes_dec as dec
import Modules.aes_enc as enc
from Modules.convert import *

def encrypt(text, key, mode):
    mat_res = []
    mat_key = key_2_matrix(key)
    if mode.upper() ==  "ECB":
        text_list = cipher_block_0(text)
        for e in text_list:
            tmp_key = mat_key.copy()
            mat_e = ascii_2_matrix(e)
            mat_res_e = enc.AES(mat_e, tmp_key)
            mat_res.append(mat_res_e)
    return mat_res

def decrypt(text, key):
    mat_key = key_2_matrix(key)
    if type(text) == str:
        mat_text = ascii_2_matrix(text)
    else:
        mat_text = text
    res = dec.InvAES(mat_text,mat_key)
    return matrix_2_ascii(res)


#First cipher function
def cipher_block_0(text):
    text_list = [] 
    for i in range(len(text) // 16 + 1):
        s = text[16*i:16*(i+1)]
        if len(s) != 16:
            for i in range(16 - len(s)):
                s += "0"
        text_list.append(s)
    return text_list

