#Import des modules codés pendant le TIPE
import Modules.aes_dec as dec 
import Modules.aes_enc as enc
from Modules.convert import *
#Import de modules python déjà existant
from PIL import Image
from math import *
import time
import codecs
from numpy.polynomial import Polynomial
import numpy as np

initialization_vector = [[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,16]] #Vecteur d'initialisation quelconque

def f_time(fun, *kwargs):
	"""Calcul du temps d'éxecution d'une fonction

	Cette fonction effectue une fonction donnée et renvoie le temps (en min) nécessaire à l'éxecution de la fonction

	Parameters
	----------
	fun : fonction à étudier

	*kwargs : ensemble des paramètres de la fonction

	Returns
	-------
	int 
		Le temps mis pour faire tourner la fonction
	"""
	t1 = time.time()
	r = fun(*kwargs)
	t2 = time.time()
	t = t2 - t1
	return t/60

def XOR(A,B):
	"""Opérateur XOR entre deux matrices

	Cette fonction applique l'opérateur XOR terme à terme entre deux matrices 4x4

	Parameters
	----------
	A : list or np.array
		Premiere matrice
	B : list or np.array
		Seconde matrice

	Returns
	-------
	List 
		Matrice résultante de l'opération XOR (addition dans le corps de Galois)
	"""
	C = [[1,7,2,9],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	for i in range(4):
		for j in range(4):
			C[i][j] = int(A[i][j]) ^ int(B[i][j])
	return C

def increase(compteur):
	"""Fonction augmantant de 1 un compteur sous forme de matrice 4x4

	Parameters
	----------
	compteur : list or np.array
		compteur que l'on souhait augmanter de 1

	Returns
	-------
	List 
		nouveau compteur augmanté de 1
	"""
	for i in range(4):
		for j in range(4):
			if compteur[i][j] != 255:
				compteur[i][j] += 1
				return compteur

def poly(p):
	"""Obtention du polynome représentant un entier entre 0 et 255
	Fonction renvoyant le polynome associé à la représentation en base 2 d'un entier.

	Parameters
	----------
	p : int 
		entier compris entre 0 et 255

	Returns
	-------
	Polynomial 
		polynome associé à la représentation de l'entier
	"""
	t = bin(p)[2:]
	mat_p = []
	for e in t:
		mat_p = [int(e)] + mat_p
	return Polynomial(mat_p)

def mult_single(p,q):
	"""Multiplication de deux entier dans le corps de Galois
	Effectue la multiplication de deux entiers dans le corps de Galois en passant par la réprensation polynomiale des entiers

	Parameters
	----------
	p : int
		Premier nombre entier
	q : int 
		Second nombre entier

	Returns
	-------
	int
		Le produit des deux nombres
	"""
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
	"""Multiplication terme à terme de deux matrices dans le corps de Galois

	Parameters
	----------
	M : list or np.array
		Premiere matrice
	N : list or np.array
		Seconde matrice

	Returns
	-------
	List 
		Produit des deux matrices
	"""
	res = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
	for i in range(4):
		for j in range(4):
			res[i][j] = mult_single(M[i][j],N[i][j])
	return res

def encrypt(text,key,mode = "ECB",auth_data1 = initialization_vector ):
	"""Fonction chiffrant un texte de longueur quelconque selon le mode choisit
	Fonction appliquant l'AES sur un texte dont la longueur peut dépasser les 16 caractères.
	La méthode appliquée pour chiffrer ce texte dépendant du mode d'opération choisit. 

	Parameters
	----------
	text : str 
		texte à chiffrer 
	key : str
		clé de chiffrement
	mode : str 
		Mode d'opération choisit (trois choix possible parmis :)

		- "ECM" : méthode de base sans opération suplémentaire

		- "CBC" : méthode évitant les répétitions

		- "GCM" : méthode plus rapide réduisant le risque d'erreur et permettant une vérification rapide
	auth_data1 : list 
		vecteur d'authentification uniquement pour le mode GCM
	
	Returns
	-------
	list
		Liste de matrice 4x4 contenant les élèments chiffrés
	list
		Matrice 4x4 d'authentification (uniquement en GCM) permettant de vérifier l'absence d'erreur 
	"""
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
		compteur = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
		hash_subkey = enc.AES([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]],key_2_matrix(key))
		auth_tag = mult(hash_subkey,auth_data1)
		temp = compteur.copy()
		truc = enc.AES(temp[:],key_2_matrix(key))
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
	"""Fonction déchiffrant un texte de longueur quelconque selon le mode choisit
	Fonction appliquant l'AES sur un texte dont la longueur peut dépasser les 16 caractères.
	La méthode appliquée pour déchiffrer ce texte dépendant du mode d'opération choisit. 

	Parameters
	----------
	text : str or list 
		texte à déchiffrer ou liste de matrice 4x4 contenant les éléments chiffrés
	key : str
		clé de chiffrement
	mode : str 
		Mode d'opération choisit (trois choix possible parmis :)

		- "ECM" : méthode de base sans opération suplémentaire

		- "CBC" : méthode évitant les répétitions

		- "GCM" : méthode plus rapide réduisant le risque d'erreur et permettant une vérification rapide

		(doit etre identique au mode utilisé pour chiffrer)

	auth_data1 : list 
		vecteur d'authentification uniquement pour le mode GCM
	
	Returns
	-------
	str
		Texte déchiffré 
	list
		Matrice 4x4 d'authentification (uniquement en GCM) permettant de vérifier l'absence d'erreur 
	"""
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
			compteur = np.array([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
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
				if i == 0:
					print(l_text[i])
				auth_tag = XOR(auth_tag.copy(),l_text[i])
				auth_tag = mult(auth_tag.copy(),hash_subkey)
			auth_tag = XOR(auth_tag,truc)
			return l_res, auth_tag
		else:
			pass

def create_image(text_enc,width,height,name = "img_enc.jpg"):
	"""Création d'une image
	Cette fonction crée et enregistre une image

	Parameters
	----------
	text_enc : str 
		donnée de l'image (liste des valeurs RGB des pixels)
	width : int
		largeur de l'image
	height : int
		hauteur de l'image
	name : str
		nom de l'image ainsi crée

	Returns
	-------
	None 
	"""
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
	"""Première version de l'application de l'AES à une image
	Cette fonction chiffre une image pixel par pixel en AES

	Parameters
	----------
	image : str
		nom de l'image
	key : str
		clé de chiffrement
	mode : str
		mode de chiffrement 

	Returns
	-------
	List 
		liste des matrices contenant les données de l'image chiffrée 
	"""
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
	"""Première version de l'application de l'AES à une image
	Cette fonction déchiffre une image pixel par pixel en AES

	Parameters
	----------
	mat : list
		liste de matrice 4x4 contenant les données de l'image 
	key : str
		clé de chiffrement
	mode : str
		mode de chiffrement 

	Returns
	-------
	None
		Enregiste l'image déchiffrée
	"""
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
	"""Seconde version de l'application de l'AES à une image
	Cette fonction chiffre une image pixel par pixel en AES et l'enregistre

	Parameters
	----------
	image : str
		nom de l'image
	key : str
		clé de chiffrement
	mode : str
		mode de chiffrement 
	name : str
		nom de de l'image chiffrée ainsi obtenue

	Returns
	-------
	List 
		liste des matrices contenant les données de l'image chiffrée 
	"""
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
	if mode == "GCM" or mode == "gcm":
		res,auth = encrypt(text,key,mode)
	else:
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
	"""Seconde version de l'application de l'AES à une image
	Cette fonction déchiffre une image pixel par pixel en AES

	Parameters
	----------
	mat : list
		liste de matrice 4x4 contenant les données de l'image 
	key : str
		clé de chiffrement
	width : int
		largeur de l'image
	height : int
		hauteur de l'image
	mode : str
		mode de chiffrement 

	Returns
	-------
	None
		Enregiste l'image déchiffrée
	"""
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
	"""Première version de l'application de l'AES à un fichier texte
	Cette fonction chiffre un fichier texte ligne par ligne en AES et enregistre le texte chiffré

	Parameters
	----------
	fic_txt : str
		nom du fichier
	key : str
		clé de chiffrement
	mode : str
		mode de chiffrement 
	name :
		nom du fichier sauvegardant le texte chiffré
	Returns
	-------
	None
	"""
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
	"""Première version de l'application de l'AES à un fichier texte
	Cette fonction déchiffre un fichier texte ligne par ligne en AES

	Parameters
	----------
	fic_txt : str
		nom du fichier à déchiffrer
	key : str
		clé de chiffrement
	mode : str
		mode de chiffrement 
	name : str
		nom du fichier sauvergardant le texte déchiffré 
	Returns
	-------
	None
	"""
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
	"""Seconde version de l'application de l'AES à un fichier texte
	Cette fonction chiffre un fichier texte en AES et enregistre le texte chiffré

	Parameters
	----------
	fic_txt : str
		nom du fichier
	key : str
		clé de chiffrement
	mode : str
		mode de chiffrement 
	name :
		nom du fichier sauvegardant le texte chiffré
	Returns
	-------
	None
	"""
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
	"""Seconde version de l'application de l'AES à un fichier texte
	Cette fonction déchiffre un fichier texte en AES

	Parameters
	----------
	fic_txt : str
		nom du fichier à déchiffrer
	key : str
		clé de chiffrement
	mode : str
		mode de chiffrement 
	name : str
		nom du fichier sauvergardant le texte déchiffré 
	Returns
	-------
	None
	"""
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
