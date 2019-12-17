# -*- coding: utf-8 -*-
"""
Created on Fri Mar  8 19:18:26 2019

@author: LAGNAOUI Outhmane
"""
import os
import numpy as np
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

global listes_blocs

listes_blocs = []
def homogene(matrice, i, j, pas, S, TB): # S: Seuil - TB: La taille des blocs
    global listes_blocs
    if np.std(matrice[i:i+pas, j:j+pas]) < S or pas <= TB:
        bloc_homogene = [i, j, pas, int(round(np.mean(matrice[i:i+pas, j:j+pas]) + 0.00001))] # Si 6.5 -> 7
        listes_blocs.append(bloc_homogene)
    else:        
        pas = int(pas/2)
        homogene(matrice, i, j, pas, S, TB) 
        homogene(matrice, i, j+pas, pas, S, TB) 
        homogene(matrice, i+pas, j , pas, S, TB)
        homogene(matrice, i+pas, j+pas, pas, S, TB)
     
def approximation(bloc):
    Approx = np.zeros((256, 256), dtype='uint8')
    for L in bloc:
        i = L[0] # Pour recupere 'i'    L[i, j, taille, moyenne]
        j = L[1] # Pour recupere 'j'
        p = L[2] # Pour recupere 'taille'
        Approx[i:i+p,j:j+p] = L[3] 
    return Approx

def ouvrir_img(label):
    global mat_img
    file_path = filedialog.askopenfilename()
    
    img = Image.open(file_path)
    img = img.resize((256, 256), Image.BICUBIC)
    mat_img = np.asarray(img, dtype='uint8')
    photo_img_ouv = ImageTk.PhotoImage(img)
    label.config(image=photo_img_ouv)
    label.image = photo_img_ouv
    label.grid(row=2, column=1)

def coder_img():
    global b_h_R, b_h_G, b_h_B, listes_blocs, mat_img 
    
    with open('matrice.txt', 'w', encoding='utf8') as file:
        for l in mat_img:
            for i in l:
                for j in i:
                    file.write(str(j) + ' ')
            file.write('\n')
       
    mat_img_R = mat_img[:,:,0]
    mat_img_G = mat_img[:,:,1]
    mat_img_B = mat_img[:,:,2]

    homogene(mat_img_R, 0, 0, len(mat_img_R), int(Seuil_val.get()), int(TBloc_val.get()))
    b_h_R = listes_blocs
    listes_blocs = []
    homogene(mat_img_G, 0, 0, len(mat_img_G), int(Seuil_val.get()), int(TBloc_val.get()))
    b_h_G = listes_blocs
    listes_blocs = []
    homogene(mat_img_B, 0, 0, len(mat_img_B), int(Seuil_val.get()), int(TBloc_val.get()))
    b_h_B = listes_blocs
    listes_blocs = []
    
    matrice_blocs_homogenes = []
    matrice_blocs_homogenes.append(b_h_R)
    matrice_blocs_homogenes.append(b_h_G)
    matrice_blocs_homogenes.append(b_h_B)
    
    with open('matrice_comp.txt', 'w', encoding='utf8') as file:
        for l in matrice_blocs_homogenes:
            for i in l:
                for j in i:
                    file.write(str(int(j)) + ' ')
            file.write('\n')           
    
def decoder_img(label):
    matrice_approximation = np.zeros((256,256,3),dtype='uint8')
    approx_R = approximation(b_h_R)
    approx_G = approximation(b_h_G)
    approx_B = approximation(b_h_B)
    
    matrice_approximation[:,:,0] = approx_R
    matrice_approximation[:,:,1] = approx_G
    matrice_approximation[:,:,2] = approx_B

    img_resultat = Image.fromarray(matrice_approximation)
 
    with open('matrice_dec.txt', 'w', encoding='utf8') as file:
        for l in matrice_approximation:
            for i in l:
                for j in i:
                    file.write(str(int(j)) + ' ')
            file.write('\n')    
    
    photo_resultat = ImageTk.PhotoImage(img_resultat)
    label.config(image=photo_resultat)
    label.image = photo_resultat
    label.grid(row=2, column=6)
    
    err_approx = abs(np.std(mat_img) - np.std(matrice_approximation))
    eapr_val.set(str(round(err_approx, 3))) 
    
    file_init_stat = os.stat('matrice.txt')
    file_init_taille = file_init_stat.st_size
    file_final_stat = os.stat('matrice_comp.txt')
    file_final_taille = file_final_stat.st_size
    gane_espace = file_init_taille-file_final_taille
    gane_espace /= 1000 # (Octet -> Ko (1 Ko = 1000 Octects))
    gs_val.set(str(round(gane_espace, 1)) + ' Ko ')  
    
window = Tk()
    
window.title('Projet 1')
window.geometry(newGeometry='885x400')
window.resizable(width=False, height=False)
labIntro = Label(master=window, text='Manipulation des Images', fg='red')
labIntro.grid(row=0, column=3, columnspan=3, padx=10, pady=5)

img_init1 = Image.new('1', (256, 256), 'white')
photo_init1 = ImageTk.PhotoImage(img_init1)
label_init1 = Label(window, image=photo_init1)
label_init1.image = photo_init1
label_init1.grid(row=2, column=1, padx=10, pady=5)

img_init2 = Image.new('1', (256, 256), 'white')    
photo_init2 = ImageTk.PhotoImage(img_init2)
label_init2 = Label(window, image=photo_init2)
label_init2.image = photo_init2
label_init2.grid(row=2, column=6, padx=10, pady=5)
  
btnOuvrir = Button(window, text='Ouvrir une image', command=lambda: ouvrir_img(label_init1))
btnOuvrir.grid(row=1, column=1, padx=10, pady=5)

labelSeuil = Label(window, text='Seuil')
labelSeuil.grid(row=1, column=2, padx=10, pady=5)
Seuil_val = StringVar(window)
entrySeuil = Entry(window, width=10, textvariable=Seuil_val)
entrySeuil.grid(row=1, column=3, padx=10, pady=5)

labelTBloc = Label(window, text='Taille des blocs')
labelTBloc.grid(row=1, column=4, padx=10, pady=5)
TBloc_val = StringVar(window)
entryTBloc = Entry(window, width=10, textvariable=TBloc_val)
entryTBloc.grid(row=1, column=5, padx=10, pady=5)

btnCoder = Button(window, text='Coder', command=lambda: coder_img())
btnCoder.grid(row=2, column=3, padx=10, pady=5)

btnDecoder = Button(window, text='Decoder', command=lambda: decoder_img(label_init2))
btnDecoder.grid(row=2, column=4, padx=10, pady=5)

labelERRApprox = Label(window, text='Erreur d\'approximation:')
labelERRApprox.grid(row=3, column=2, columnspan=3, padx=10, pady=5)
eapr_val = StringVar(window)
labelERRApproxRep = Label(window, text='Gain', textvariable=eapr_val)
labelERRApproxRep.grid(row=3, column=4, columnspan=2, padx=10, pady=5)

labelGEMemoire = Label(window, text='Gain en espace memoire:')
labelGEMemoire.grid(row=4, column=2, columnspan=3, padx=10, pady=5)
gs_val = StringVar(window)
labelGEMemoireRep = Label(window, text='Gain', textvariable=gs_val)
labelGEMemoireRep.grid(row=4, column=4, columnspan=2, padx=10, pady=5)


window.mainloop()











