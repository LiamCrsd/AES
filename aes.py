import Modules.aes_dec as dec
import Modules.aes_enc as enc
from PIL import Image
from Modules.convert import *
from math import *
import time

initialization_vector = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]]

def f_time(fun, *kwargs):
	t1 = time.time()
	r = fun(*kwargs)
	t2 = time.time()
	t = t2 - t1
	return t/60


def XOR(A,B):
	C = [[1,7,2,9],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	for i in range(4):
		for j in range(4):
			C[i][j] = A[i][j] ^ B[i][j]
	return C

def encrypt(text,key,mode = "ECB"):
	if mode.upper() == "CBC":
		res = [initialization_vector]
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
			text_list.append(ascii_2_matrix(text[i*16:(i+1)*16]))
		for e in text_list:
			mat_key = key_2_matrix(key)
			mat_res.append(enc.AES(e, mat_key))
		return mat_res
	elif mode.upper() == "GCM":
		print("Under development")
	else:
		print("Error : wrong mode")

def decrypt(text,key,mode = "ECB"):
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
			mat_text = [initialization_vector]
			for i in range(len(text)//16 + 1):
				mat_text.append(ascii_2_matrix(text[i*16:(i+1)*16]))
			for i in range(len(mat_text) - 1,0,-1):
				mat_key = key_2_matrix(key)
				res = dec.InvAES(mat_text[i],mat_key)
				res2 = XOR(res,mat_text[i-1])
				text_dec = matrix_2_ascii(res2) + text_dec
		else:
			text = [initialization_vector] + text
			for i in range(len(text) - 1,0,-1):
				print(i)
				mat_key = key_2_matrix(key)
				res = dec.InvAES(text[i],mat_key)
				res2 = XOR(res,text[i-1])
				text_dec = matrix_2_ascii(res2) + text_dec
		return text_dec.strip("\x00")


def create_image(text_enc,width,height,name = "img_enc.jpg"):
	size = width,height
	img = Image.new("RGB",size)
	data = img.load()
	nb_pixel = width * height
	print("nombre de pixel : ",nb_pixel)
	for i in range(width):
		for j in range(height):
			compteur = i * height + j
			a,b,c = ord((text_enc[3*compteur:3*(compteur + 1)])[0]),ord((text_enc[3*compteur:3*(compteur + 1)])[1]),ord((text_enc[3*compteur:3*(compteur + 1)])[2])
			data[i,j] = a,b,c
	img.save(name)


def matrix_2_data(mat):
	t = ""
	for e in mat:
		t += matrix_2_ascii(e)
	print(len(t))
	return t


def enc_img(image,key,mode = "ECB"):
	img = Image.open(image)
	data = img.load()
	res = []
	print(img.width,img.height)
	compteur = img.width * img.height
	for i in range(img.width):
		for j in range(img.height):
			print(compteur)
			compteur -= 1
			a,b,c = data[i,j]
			a,b,c = str(a),str(b),str(c)
			while len(a) < 4:
				a = "0" + a
			while len(b) < 4:
				b = "0" + b
			while len(c) < 4:
				c = "0" + c
			t = a + b + c
			res.append(encrypt(t,key,mode))
	res.append((img.width,img.height))
	return res

def dec_img(mat,key,mode):
	size = mat.pop()
	img = Image.new("RGB",size)
	img.save("output.png")
	data = img.load()
	compteur = img.width * img.height
	for i in range(img.width):
		for j in range(img.height):
			print(compteur)
			compteur -= 1
			text = mat[i * img.height + j]
			res = decrypt(text,key,mode)
			data[i,j] = (int(res[0:4]),int(res[4:8]),int(res[8:12]))
	img.save("output2.png")

def enc_img2(image,key,mode = "ECB", name = "enc_im.png"):
	img = Image.open(image)
	data = img.load()
	text = ""
	for i in range(img.width):
		for j in range(img.height):
			a,b,c = data[i,j]
			text += int_2_utf8(a)
			text += int_2_utf8(b)
			text += int_2_utf8(c)
	print(len(text))
	return text,encrypt(text,key,mode)
