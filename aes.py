import Modules.aes_dec as dec
import Modules.aes_enc as enc
from PIL import Image
from Modules.convert import *
from math import *
import time
import codecs
from numpy.polynomial import Polynomial


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
			C[i][j] = int(A[i][j]) ^ int(B[i][j])
	return C

def increase(compteur):
	c = -1,-1
	for i in range(4):
		for j in range(4):
			if compteur[i][j] != 255:
				compteur[i][j] += 1
				return compteur

def poly(p):
	t = bin(p)[2:]
	mat_p = []
	for e in t:
		mat_p = [int(e)] + mat_p
	return Polynomial(mat_p)

def mult_single(p,q):
	P,Q = poly(p),poly(q)
	res = P*Q
	for i in range(res.degree() + 1):
		if res.coef[i] == 2:
			res.coef[i] = 0
	while res.degree() >= 8:
		R = [0] * (res.degree() - 8) + [1,1,0,1,1,0,0,0,1]
		l = []
		for i in range(res.degree() + 1):
			l.append((res.coef[i] + R[i])%2)
		c = 1
		while l[-1 * c - 1] == 0:
			c += 1
		res = Polynomial(l[:(-1 * c)])
	val = 0
	for i in range(res.degree() + 1):
		val += res.coef[i] * (2 ** i)
	return val

def mult(M,N):
	res = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	for i in range(4):
		for j in range(4):
			res[i][j] = mult_single(M[i][j],N[i][j])
	return res

def encrypt(text,key,mode = "ECB",auth_data1 = initialization_vector ):
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
		t1 = time.time()
		L = len(text)
		l_text = []
		for i in range(ceil(L/16)):
			l_text.append(ascii_2_matrix(text[i*16:(i+1)*16]))
		compteur = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
		hash_subkey = enc.AES([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],key_2_matrix(key))
		auth_tag = mult(hash_subkey,auth_data1)
		print("1 :",auth_tag)
		truc = enc.AES(compteur,key_2_matrix(key))
		compteur = increase(compteur)
		l_compteur_chiffré = []
		t2 = time.time()
		for i in range(len(l_text)):
			l_compteur_chiffré.append(enc.AES(compteur,key_2_matrix(key)))
			compteur = increase(compteur)
		l_res = []
		t3 = time.time()
		for i in range(len(l_text)):
			l_res.append(XOR(l_text[i],l_compteur_chiffré[i]))
			#auth_tag = XOR(auth_tag.copy(),l_res[-1])
			#auth_tag = mult(auth_tag.copy(),hash_subkey)
		#auth_tag = XOR(auth_tag,truc)
		t4 = time.time()
		print("Temps total : ",t4 - t1)
		print("Précalcul : ",t3 - t2)
		print("Chiffrement ",t4 - t3)
		print("Début : ",t2 - t1)
		return l_res, auth_tag
	else:
		print("Error : wrong mode")

def decrypt(text,key,mode = "ECB",auth_data1 = initialization_vector):
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
	elif mode.upper() == "GCM":
		if type(text) == str:
			L = len(text)
			l_text = []
			for i in range(ceil(L/16)):
				l_text.append(ascii_2_matrix(text[i*16:(i+1)*16]))
			compteur = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
			hash_subkey = enc.AES([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],key_2_matrix(key))
			auth_tag = mult(hash_subkey,auth_data1)
			truc = enc.AES(compteur,key_2_matrix(key))
			compteur = increase(compteur)
			l_compteur_chiffré = []
			for i in range(len(l_text)):
				l_compteur_chiffré.append(enc.AES(compteur,key_2_matrix(key)))
				compteur = increase(compteur)
			l_res = []			
			for i in range(len(l_text)):
				l_res.append(XOR(l_text[i],l_compteur_chiffré[i]))
				auth_tag = XOR(auth_tag.copy(),l_text[i])
				auth_tag = mult(auth_tag.copy(),hash_subkey)
			auth_tag = XOR(auth_tag,truc)
			return l_res, auth_tag
		else:
			pass

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

def enc_img2(image,key,mode = "ECB", name = "enc_img.png"):
	t1 = time.time()
	img = Image.open(image)
	data = img.load()
	text = ""
	for i in range(img.width):
		for j in range(img.height):
			a,b,c,_ = data[i,j]
			text += int_2_utf8(a)
			text += int_2_utf8(b)
			text += int_2_utf8(c)
	t2 = time.time()
	t_lecture = t2 - t1
	res = encrypt(text,key,mode)
	t3 = time.time()
	t_enc = t3 - t2
	create_image(matrix_2_data(res),img.width,img.height,name)
	t4 = time.time()
	t_save_img = t4 - t3
	t_tot = t4 -t1
	print("Temps total : ",t_tot)
	print("Temps lecture image : ",t_lecture)
	print("Temps chiffrement : ",t_enc)
	print("Temps creation image : ",t_save_img)
	return res

def dec_img2(image,key,width,height,mode = "ECB", name = "dec_img.png"):
	if type(image) != str:
		res = decrypt(image,key,mode)
		create_image(res,width,height,name)
	else:
		img = Image.open(image)
		data = img.load()
		text = ""
		for i in range(img.width):
			for j in range(img.height):
				a,b,c,_ = data[i,j]
				text += int_2_utf8(a)
				text += int_2_utf8(b)
				text += int_2_utf8(c)
		res = decrypt(text,key,mode)
		create_image(res,img.width,img.height,name)

def enc_fic_txt(fic_txt,key,mode = "ECB", name = "enc.txt"):
	fichier = codecs.open(fic_txt,mode="r",encoding="utf-8")
	fichier2 = codecs.open(name,mode="x",encoding="utf-8")
	lignes = fichier.readlines()
	for e in lignes:
		e2 = e.strip("\n")
		res = encrypt(e2,key,mode)
		res2 = matrix_2_data(res)
		res2 = res2.replace("\n",bytes([196,255-64]).decode())
		res2 = res2.replace("\r",bytes([196,254-64]).decode())
		fichier2.write(res2 + "\n")
	print(len(lignes))
	fichier2.close()
	fichier.close()

def dec_fic_txt(fic_txt,key,mode = "ECB", name = "dec.txt"):
	fichier = codecs.open(fic_txt,mode="r",encoding="utf-8")
	fichier2 = codecs.open(name,mode="x",encoding="utf-8")
	lignes = fichier.readlines()
	for e in lignes:
		print("1 : ",e)
		e2 = e.strip("\n")
		print("2 : ",e2)
		res = decrypt(e2,key,mode)
		print("3 : ",res)
		res2 = matrix_2_data(res)
		res2.replace(bytes([196,255-64]).decode(),"\n")
		res2.replace(bytes([196,254-64]).decode(),"\r")
		print("\n")
		fichier2.writeline(res2)
	fichier2.close()
	fichier.close()

def enc_fic_txt2(fic_txt,key,mode = "ECB", name = "enc.txt"):
	fichier = codecs.open(fic_txt,mode="r",encoding="utf-8")
	try:
		fichier2 = codecs.open(name,mode="x",encoding="utf-8")
	except:
		fichier2 = codecs.open(name[:-4] + str(time.time()) + ".txt",mode="x",encoding="utf-8")
	lignes = fichier.readlines()
	txt = ""
	for e in lignes:
		txt += e
	if mode == "GCM" or mode == "gcm":
		res, auth = encrypt(txt,key,mode)
		res = matrix_2_data(res)
		print("auth :",auth)
	else:
		res = matrix_2_data(encrypt(txt,key,mode))
	fichier2.write(res)
	fichier2.close()
	fichier.close()

def dec_fic_txt2(fic_txt,key,mode = "ECB", name = "dec.txt"):
	fichier = codecs.open(fic_txt,mode="r",encoding="utf-8")
	try:
		fichier2 = codecs.open(name,mode="x",encoding="utf-8")
	except:
		fichier2 = codecs.open(name[:-4] + str(time.time()) + ".txt",mode="x",encoding="utf-8")
	lignes = fichier.readlines()
	txt = ""
	for e in lignes:
		txt += e
	if mode == "GCM" or mode == "gcm":
		res, auth = decrypt(txt,key,mode)
		res = matrix_2_data(res)
		print("auth :",auth)
	else:
		res = decrypt(txt,key,mode)
	fichier2.write(res)
	fichier2.close()
	fichier.close()
