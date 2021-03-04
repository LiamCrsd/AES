import Modules.aes_dec as dec
import Modules.aes_enc as enc
from Modules.convert import *
from math import *

VI = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]


def XOR(A,B):
	C = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	for i in range(4):
		for j in range(4):
			C[i][j] = A[i][j] ^ B[i][j]
	return C

def encrypt(text,key,mode):
	if mode.upper() == "CBC":
		res = [VI]
		L = len(text)
		l_text = []
		for i in range(ceil(L/16)):
			l_text.append(ascii_2_matrix(text[i*16:(i+1)*16]))
		for elem in l_text:
			mat_key = key_2_matrix(key)
			mat_text = XOR(elem,res[-1])
			res.append(enc.AES(mat_text, mat_key))
		return res[1:]
	elif mode.upper() == "ECB":
		mat_res = []
		text_list = []
		for i in range(ceil(len(text)/16)):
			print(i)
			text_list.append(ascii_2_matrix(text[i*16:(i+1)*16]))
		for e in text_list:
			mat_key = key_2_matrix(key)
			mat_res.append(enc.AES(e, mat_key))
		return mat_res
	elif mode.upper() == "GCM":
		print("Under development")
	else:
		print("Error : wrong mode")

def decrypt(text,key,mode):
	if mode.upper() == "ECB":
		text_dec = ""
		if type(text) == str:
			for i in range(ceil(len(text)/16)):
				mat_key = key_2_matrix(key)
				mat_text = ascii_2_matrix(text[i*16:(i+1)*16])
				res = dec.InvAES(mat_text,mat_key)
				text_dec += matrix_2_ascii(res)
		else:
			for e in text:
				mat_key = key_2_matrix(key)
				mat_text = e
				res = dec.InvAES(mat_text,mat_key)
				text_dec += matrix_2_ascii(res)
		return text_dec.strip("\x00")
	elif mode.upper() == "CBC":
		text_dec = ""
		if type(text) == str:
			mat_text = [VI]
			for i in range(len(text)//16 + 1):
				mat_text.append(ascii_2_matrix(text[i*16:(i+1)*16]))
			for i in range(len(mat_text) - 1,0,-1):
				mat_key = key_2_matrix(key)
				res = dec.InvAES(mat_text[i],mat_key)
				res2 = XOR(res,mat_text[i-1])
				text_dec = matrix_2_ascii(res2) + text_dec
		else:
			text = [VI] + text
			for i in range(len(text) - 1,0,-1):
				mat_key = key_2_matrix(key)
				res = dec.InvAES(text[i],mat_key)
				res2 = XOR(res,text[i-1])
				text_dec = matrix_2_ascii(res2) + text_dec
		return text_dec.strip("\x00")









