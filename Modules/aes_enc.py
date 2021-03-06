from binascii import hexlify as hex
import numpy

# AES_enc Version du 03 / 02

#----------------------------------------------------Données de base------------------------------------------------------------------------------

len_key = 128 #taille de la clé, 128, 192 ou 256 bits
t_key = len_key/8 #taille de la clé en octets
N_key = int(t_key/4) #Nombre de colones du tableau contenant la clé
tab_conv = {4:10,6:12,8:14} #Dictionnaire affectant à la valeur N_key le nombre de tours nécessaires
nr = tab_conv[N_key] #Nombre de tours définie en fonction de la taille de la clé

#------------------------------------------------------Données nécessaire---------------------------------------------------------------

Sbox = ( #Table de substitution
    0x63, 0x7C, 0x77, 0x7B, 0xF2, 0x6B, 0x6F, 0xC5, 0x30, 0x01, 0x67, 0x2B, 0xFE, 0xD7, 0xAB, 0x76,
    0xCA, 0x82, 0xC9, 0x7D, 0xFA, 0x59, 0x47, 0xF0, 0xAD, 0xD4, 0xA2, 0xAF, 0x9C, 0xA4, 0x72, 0xC0,
    0xB7, 0xFD, 0x93, 0x26, 0x36, 0x3F, 0xF7, 0xCC, 0x34, 0xA5, 0xE5, 0xF1, 0x71, 0xD8, 0x31, 0x15,
    0x04, 0xC7, 0x23, 0xC3, 0x18, 0x96, 0x05, 0x9A, 0x07, 0x12, 0x80, 0xE2, 0xEB, 0x27, 0xB2, 0x75,
    0x09, 0x83, 0x2C, 0x1A, 0x1B, 0x6E, 0x5A, 0xA0, 0x52, 0x3B, 0xD6, 0xB3, 0x29, 0xE3, 0x2F, 0x84,
    0x53, 0xD1, 0x00, 0xED, 0x20, 0xFC, 0xB1, 0x5B, 0x6A, 0xCB, 0xBE, 0x39, 0x4A, 0x4C, 0x58, 0xCF,
    0xD0, 0xEF, 0xAA, 0xFB, 0x43, 0x4D, 0x33, 0x85, 0x45, 0xF9, 0x02, 0x7F, 0x50, 0x3C, 0x9F, 0xA8,
    0x51, 0xA3, 0x40, 0x8F, 0x92, 0x9D, 0x38, 0xF5, 0xBC, 0xB6, 0xDA, 0x21, 0x10, 0xFF, 0xF3, 0xD2,
    0xCD, 0x0C, 0x13, 0xEC, 0x5F, 0x97, 0x44, 0x17, 0xC4, 0xA7, 0x7E, 0x3D, 0x64, 0x5D, 0x19, 0x73,
    0x60, 0x81, 0x4F, 0xDC, 0x22, 0x2A, 0x90, 0x88, 0x46, 0xEE, 0xB8, 0x14, 0xDE, 0x5E, 0x0B, 0xDB,
    0xE0, 0x32, 0x3A, 0x0A, 0x49, 0x06, 0x24, 0x5C, 0xC2, 0xD3, 0xAC, 0x62, 0x91, 0x95, 0xE4, 0x79,
    0xE7, 0xC8, 0x37, 0x6D, 0x8D, 0xD5, 0x4E, 0xA9, 0x6C, 0x56, 0xF4, 0xEA, 0x65, 0x7A, 0xAE, 0x08,
    0xBA, 0x78, 0x25, 0x2E, 0x1C, 0xA6, 0xB4, 0xC6, 0xE8, 0xDD, 0x74, 0x1F, 0x4B, 0xBD, 0x8B, 0x8A,
    0x70, 0x3E, 0xB5, 0x66, 0x48, 0x03, 0xF6, 0x0E, 0x61, 0x35, 0x57, 0xB9, 0x86, 0xC1, 0x1D, 0x9E,
    0xE1, 0xF8, 0x98, 0x11, 0x69, 0xD9, 0x8E, 0x94, 0x9B, 0x1E, 0x87, 0xE9, 0xCE, 0x55, 0x28, 0xDF,
    0x8C, 0xA1, 0x89, 0x0D, 0xBF, 0xE6, 0x42, 0x68, 0x41, 0x99, 0x2D, 0x0F, 0xB0, 0x54, 0xBB, 0x16,
)
Rcon = ( #Ensemble des valeurs prises par Rcon
    0x00, 0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40,
    0x80, 0x1B, 0x36, 0x6C, 0xD8, 0xAB, 0x4D, 0x9A,
    0x2F, 0x5E, 0xBC, 0x63, 0xC6, 0x97, 0x35, 0x6A,
    0xD4, 0xB3, 0x7D, 0xFA, 0xEF, 0xC5, 0x91, 0x39,
)


#----------------------------------------------------Fonctions dans l'AES---------------------------------------------------------------

#----------------------------------------------------Fonctions dans Round---------------------------------------------------------------

def x_mult(t):
    nt = t << 1         # Multiplie par x
    if nt & 256:         # CAS OU x^8 est atteint
        nt = nt ^ 27    # Division modulo x^8 + x^4 + x^3 + x + 1
        nt = nt & 255   # On garde les 8 premiers bits
    return nt


def SubBytes(tab):
    """Fonction subsituant chaque valeur d'une matrice selon la table préalablement définie

    Parameters
    ----------
    tab : list or np.array
        Matrice 4x4

    Returns
    -------
    list or np.array
        Matrice dont les éléments ont été substitués
    """
    for i in range(4):
        for j in range(4):
            tab[i][j] = Sbox[tab[i][j]]
    return tab

def ShiftRows(tab):
    """Procédure qui opère une rotation à gauche sur chaque ligne du tableau

    Parameters
    ----------
    tab : list or np.array
        Matrice 4x4 sur laquelle appliquer la rotation

    Returns
    -------
    list or np.array
        Matrice ayant subit la rotatation
    """
    ntab = [tab[0]]
    for i in range(1,4):
        ntab.append([tab[i][i%4],tab[i][(1+i)%4],tab[i][(2+i)%4],tab[i][(3+i)%4]])
    return ntab

def mix_single_column(t):
    """Produit matriciel d'une colonne par une matrice 4x4 de convention

    Parameters
    ----------
    t : list
        Colonne de 4 entiers

    Returns
    -------
    list
        Nouvelle colonne de 4 entiers
    """
    a, b, c, d = t[0], t[1], t[2], t[3]
    na = x_mult(a ^ b) ^ b ^ c ^ d
    nb = a ^ x_mult(b ^ c) ^ c ^ d
    nc = a ^ b ^ x_mult(c ^ d) ^ d
    nd = x_mult(a ^ d) ^ a ^ b ^ c
    return [na, nb, nc, nd]

def MixColumns(tab):
    """Procédure appliquant la transformation à chaque colonne

    Parameters
    ----------
    tab : list
        Matrice 4x4 d'entiers

    Returns
    -------
    list
        Nouvelle matrice 4x4
    """
    transp = numpy.array(tab)
    for i in range(4):
        transp[:,i] = mix_single_column(transp[:, i])
    return transp


def AddRoundKey(tab,T_key):
    """Fonction appliquant la clé sur le bloc à chiffrer à l'aide de l'opération XOR terme à terme

    Parameters
    ----------
    tab : list or np.array
        Matric 4x4 à chiffrer
    T_key : list or np.array
        Matrice 4x4 contenant la clé à appliquer

    Returns
    -------
    list or np.array
        Matrice 4x4 après l'application de la clé
    """
    for i in range(4):
        for j in range(4):
            tab[i][j] ^= T_key[j][i]
    return tab

#------------------------------------------------------Fonction Round--------------------------------------------------------------------

def Round(tab,T_key):
    """Fonction effectuant les 4 opérations à effectuer à chaque tour

    Parameters
    ----------
    tab : list
        Matrice 4x4 à chiffrer
    T_key : list
        Matrice 4x4 contenant la clé à utiliser

    Returns
    -------
    list
        Matrice 4x4 ayant subit un tour de chiffrement
    """
    tab = SubBytes(tab)
    tab = ShiftRows(tab)
    tab = MixColumns(tab)
    tab = AddRoundKey(tab,T_key)
    return tab

#----------------------------------------------------Fonction FinalRound--------------------------------------------------------------------

def FinalRound(tab,T_key):
    """Fonction effectuant les 3 opérations à effectuer lors du dernier tour

    Parameters
    ----------
    tab : list
        Matrice 4x4 à chiffrer
    T_key : list
        Matrice 4x4 contenant la clé à utiliser

    Returns
    -------
    list
        Matrice 4x4 ayant subit le tour de chiffrement
    """
    tab = SubBytes(tab)
    tab = ShiftRows(tab)
    tab = AddRoundKey(tab,T_key)
    return tab

#---------------------------------------------------Fonction KeyExpansion--------------------------------------------------------------------

def KeyExpansion(tab):
    """Fonction étandant la clé principale en une liste de clé (sous forme de matrice 4x4)

    Parameters
    ----------
    tab : list
        Matrice 4x4 contenant la clé de départ

    Returns
    -------
    list
        Liste de clé
    """
    blocks = tab
    for i in range(4, 4 * (nr + 1)):
        blocks.append([])
        if i % 4 == 0:
            b = blocks[i-4][0] ^ Sbox[blocks[i - 1][1]] ^ Rcon[i // 4]
            blocks[i].append(b)
            for j in range(1, 4):
                b = blocks[i - 4][j] ^ Sbox[blocks[i-1][(j + 1) % 4]]
                blocks[i].append(b)
        else:
            for j in range(4):
                b = blocks[i - 4][j] ^ blocks[i - 1][j]
                blocks[i].append(b)
    return blocks


#------------------------------------------------------Fonction AES--------------------------------------------------------------------

def AES(tab, key):
    """Fonction chiffrant un bloc de caractères

    Parameters
    ----------
    tab : list
        Matrice 4x4 contenant les caractères à chiffrer sous forme d'entiers compris entre 0 et 255
    key : list
        Matrice 4x4 contenant la clé de chiffrement

    Returns
    -------
    list
        Matrice 4x4 contenant les caractères chiffrés (sous forme d'entiers)
    """
    Tk = KeyExpansion(key)
    tab = AddRoundKey(tab,Tk[:4])
    for i in range(1,nr):
        tab = Round(tab,Tk[4 * i:4*(i+1)])
    tab = FinalRound(tab,Tk[-4:])
    return tab

#-------------------------------------------------------------------------------------------------------------
