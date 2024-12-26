

from model.model_pg import get_serie_by_name, insert_serie
from controleurs.includes import add_activity
import random
import toml
import psycopg
from psycopg.sql import SQL, Identifier
import flask
from flask import Flask, request, redirect, url_for, session
app = Flask(__name__)
import datetime

global grille
grille=False
    
global tab

def get_color(item_id):
       for i in range (len(alea)):
         if alea[i][0]==item_id:
            return alea[i][4]
       return "#FFFFFF"

if POST and 'bouton_validergrille':
    grille=True
    if 'largeur_grille' in POST and 'longeur_grille' in POST:
     largeur = int(POST['largeur_grille'][0])
     longeur = int(POST['longeur_grille'][0])
     SESSION['largeur']=largeur
     SESSION['longeur']=longeur
     tab = [[0 for _ in range(largeur)] for _ in range(longeur)]
     if largeur*longeur>=5:
         nta10=largeur*longeur*0.1
         nta20=largeur*longeur*0.2
         if nta10.is_integer()==False:
             n=round(nta10)
             if n<nta10:
                 nta10=n+1
             else:
                 nta10=n
         if nta20.is_integer()==False:
             n=round(nta20)
             if n<nta20:
                 nta20=n
             else:
                 nta20=n-1
         nta10=int(nta10)
         nta20=int(nta20)
         nta=random.randint(nta10,nta20)
         ic=random.randint(0,longeur-1)
         jc=random.randint(0,largeur-1)
         tab[ic][jc]=1
         print("nbre cases",nta)
         nta=nta-1
         while nta>0:
             d=random.randint(0,3)
             if d==0:
                 if ic+1<longeur and tab[ic+1][jc]==0:
                     tab[ic+1][jc]=1
                     ic=ic+1
                     nta=nta-1
             elif d==1:
                 if ic-1>=0 and tab[ic-1][jc]==0:
                     tab[ic-1][jc]=1
                     ic=ic-1
                     nta=nta-1
             elif d==2:
                 if jc+1<largeur and tab[ic][jc+1]==0:
                     tab[ic][jc+1]=1
                     jc=jc+1
                     nta=nta-1
             else:
                 if jc-1>=0 and tab[ic][jc-1]==0:
                     tab[ic][jc-1]=1
                     jc=jc-1
                     nta=nta-1
         SESSION['message_tab']="Il y a entre 10% et 20% des cases cibles."
     else:
         SESSION['message_tab']="Il faut plus des cases pour générer des cases cibles."
     SESSION['tab']=tab
     SESSION['tabcouleur'] = [['#FFFFFF' for _ in range(largeur)] for _ in range(longeur)]
     for i in range (len(SESSION['tabcouleur'])):
         for j in range (len(SESSION['tabcouleur'][0])):
             SESSION['tabcouleur'][i][j]="#FFFFFF"

if POST and 'bouton_validertours':
    if 'nbre_tours' in POST:
     tours=int(POST['nbre_tours'][0])
     SESSION['tours_rest']=tours
     SESSION['tours_max']=tours
    else:
     print("erreur")
     
global mode
if POST and 'bouton_validermode':
    if 'mode' in POST:
     mode=POST['mode'][0]
     SESSION['mode']=mode
    else:
     print("erreur")
else:
    mode="none"
     
       
add_activity(SESSION['HISTORIQUE'], "consultation de la page de jeu")

config = toml.load('config-bd.toml')
def get_connexion(host, username, password, db, schema):
    try:
        connexion = psycopg.connect(host=host, user=username,password=password, dbname=db, autocommit=True)
        cursor = psycopg.ClientCursor(connexion)
        cursor.execute("SET search_path TO %s", [schema])
    except Exception as e:
        print(e)
        return None
    return connexion
    
 
conn=get_connexion(config['POSTGRESQL_SERVER'],config['POSTGRESQL_USER'],config['POSTGRESQL_PASSWORD'],config['POSTGRESQL_DATABASE'],config['POSTGRESQL_SCHEMA'])

if POST and 'bouton_validerprenom' in POST:
    prenom = POST['prenom'][0]
    if prenom:
        SESSION['prenom'] = prenom
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM legos.Joueur WHERE prenom = %s LIMIT 1;", (prenom,))
            result = cursor.fetchone()
            if result:
                print(f"Le prénom '{prenom}' existe déjà.")
            else:
                cursor.execute("INSERT INTO legos.Joueur(prenom) VALUES (%s);", (prenom,))
                cursor.execute("INSERT INTO legos.gagnant (joueur_gagnant) VALUES (%s);", (SESSION['prenom'],))
        except psycopg.Error as e:
            print(f"Error: {e}")
        cursor.close()
def get_aleaf(conn,SQL,Identifier):
   try:
        cursor = conn.cursor()
        query = SQL("SELECT * FROM {schema}.{table} WHERE longeur <=2 OR largeur <=2 ORDER BY RANDOM() LIMIT 4").format(schema=Identifier('legos'),table=Identifier('piece'))
    
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
   except psycopg.Error as e:
        print(f"Error : {e}")
   return None
   
def get_alead(conn,SQL,Identifier):
   try:
        cursor = conn.cursor()
        query = SQL("SELECT * FROM {schema}.{table} ORDER BY RANDOM() LIMIT 4").format(schema=Identifier('legos'),table=Identifier('piece'))
    
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
   except psycopg.Error as e:
        print(f"Error : {e}")
   return None
   

global alea


    
SESSION['start_tir'] = True

if POST and 'start' in POST:
    if 'start_tir' in SESSION:
        SESSION['debut']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
              cursor = conn.cursor()
              cursor.execute("SELECT MAX(id_partie) FROM legos.partie;")
              max_id = cursor.fetchone()[0]
              if max_id is not None:
                    next_id = max_id + 1
              else:
                    next_id =  1

              SESSION['partie'] = next_id
              cursor.execute("INSERT INTO legos.partie (id_partie,date_debut,id_configuration) VALUES (%s, %s,%s);",(SESSION['partie'],SESSION['debut'],'NULL'))
              
        except psycopg.Error as e:
              print(f"Error: {e}")
        cursor.close()
        SESSION['score']=0
        SESSION['tours']=0
        print("Score initialise",SESSION['score'])
        if SESSION['start_tir'] == True:
            if mode == "facile" or mode == "difficile":
              
                alea = None
                if mode == "facile":
                    alea = get_aleaf(conn, SQL, Identifier)
                elif mode == "difficile":
                    alea = get_alead(conn, SQL, Identifier)
                SESSION['message_mode'] = ""
                
              
                for a in alea:
                    print(a)
                SESSION['ALEA'] = alea
                
                
                SESSION['start_tir'] = False
            else:
                
                SESSION['message_mode'] = "Il est nécessaire de sélectionner un mode de jeu!"
        else:
            SESSION['message_mode'] = "Le tirage des briques a déjà été effectué. Impossible de tirer à nouveau."
    else:
        SESSION['message_mode'] = "Une erreur est survenue avec le tirage des briques."




        

            

global largeur_brique
global longeur_brique
global item_id
   
if POST and 'bouton_pressed' in POST:
    item_id = int(POST['idi'][0]) #brique choisi par l'utilisateur
    for i in range (len(alea)):
        if alea[i][0]==item_id:
            SESSION['CHOISI']=alea[i]
            SESSION['BRIQUE']=alea[i]
            longeur_brique=alea[i][1]
            largeur_brique=alea[i][2]
    '''for i in range(4):
       if alea[i][0]==item_id:
          if mode=="facile":
              alea[i]=get_aleaf(conn,SQL,Identifier)[0]
          else:
              alea[i]=get_alead(conn,SQL,Identifier)[0]'''
  
global placer_i #a
global placer_j #a
  

  
def placer_tab(tab, l1, l2):
    def can_place(tab, l1, l2):
        global placer_i #a
        global placer_j #a
        for i in range(len(tab) - l1 + 1):
            for j in range(len(tab[0]) - l2 + 1):
                place_block = True
                for a in range(l1):
                    for b in range(l2):
                        if tab[i + a][j + b] != 1:
                            place_block = False
                            break
                    if not place_block:
                        break
                if place_block:
                    placer_i=i #a
                    placer_j=j #a
                    return True
        return False
    return can_place(tab, l1, l2) or can_place(tab, l2, l1)
def placer_brique(tab,l1,l2,a,b): #a
    #ajouter
    for i in range (len(tab)):
        for j in range (len(tab[0])):
            if i==a and j==b:
                a=i
                b=j
    for i in range (l1):
        for j in range (l2):
            tab[a+i][b+j]=item_id
            for l in range (len(alea)):
                if alea[l][0]==item_id:
                    SESSION['tabcouleur'][a+i][b+j]=alea[l][4]
    
    
          
                    
    
            
 
def verifier_gagner(tab):
    gagner=True
    for i in range (len(tab)):
        for j in range (len(tab[0])):
            if tab[i][j]==1:
                gagner=False
    return gagner
 

global taille_brique
if grille==True and POST and 'bouton_actionbr' in POST:
    post_data = POST.copy()
    SESSION['place']=""
    actionbrique=POST['actionbrique'][0]
    
    if actionbrique=="placer":
        taille_brique=longeur_brique*largeur_brique
        place=placer_tab(tab,longeur_brique,largeur_brique)
        if place==True:
          SESSION['place']="On peut placer brique sur la grille."
          SESSION['taille_brique']=taille_brique
         
                  
          #placer_brique(tab,longeur_brique,largeur_brique,placer_i,placer_j)#a
          print("Couleurs:",SESSION['tabcouleur'])
          print("Grid:", tab)
          print("Brick Dimensions:", longeur_brique, largeur_brique)
          SESSION['tab']=tab #a
        else:
          SESSION['place']="Il n'y a pas assez d'espace sur grille."
          SESSION['score']=SESSION['score']+1
          if 'tours_rest' in SESSION:
            SESSION['tours_rest']=SESSION['tours_rest']-1
            if SESSION['tours_rest']==0:
              SESSION['score']=999
              SESSION['resultat']="Vous avez perdu!"
    elif actionbrique=="defausser":
      SESSION['score']=SESSION['score']+1
      SESSION['tours']=SESSION['tours']+1
      try:
              cursor = conn.cursor()
              cursor.execute("INSERT INTO legos.tour (id_partie, numero) VALUES (%s,%s);", (SESSION['partie'],SESSION['tours']))
              cursor.execute("INSERT INTO legos.action (id_partie, numero, id_b, description) VALUES (%s,%s,%s,%s);", (SESSION['partie'],SESSION['tours'],item_id,'defaussee'))
      except psycopg.Error as e:
              print(f"Error: {e}")
      cursor.close()

      if 'tours_rest' in SESSION:
          SESSION['tours_rest']=SESSION['tours_rest']-1
          if SESSION['tours_rest']==0:
              SESSION['score']=999
              SESSION['resultat']="Vous avez perdu!"
              try:
                cursor = conn.cursor()
                if 'prenom' not in SESSION:
                  SESSION['prenom']="NULL"
                cursor.execute("INSERT INTO legos.derouler (prenom, id_partie, joueur_gagnant, score) VALUES (%s,%s,%s,%s);", (SESSION['prenom'],SESSION['partie'],'NULL',SESSION['score']))
                print("insere")
              except psycopg.Error as e:
                print(f"Error: {e}")
                cursor.close()
      for i in range(4):
          if alea[i][0]==item_id:
            if mode=="facile":
                alea[i]=get_aleaf(conn,SQL,Identifier)[0]
            else:
                alea[i]=get_alead(conn,SQL,Identifier)[0]
    
      #aj
    del post_data['bouton_actionbr']
    SESSION.pop('CHOISI', None)



if POST and 'bouton_actionplacer' in POST:
    post_data = POST.copy()
    SESSION['score']=SESSION['score']+1
    SESSION['tours']=SESSION['tours']+1
    if 'tours_rest' in SESSION:
        SESSION['tours_rest']=SESSION['tours_rest']-1
        if SESSION['tours_rest']==0:
            SESSION['score']=999
            SESSION['resultat']="Vous avez perdu!"
            SESSION['fin']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            try:
              cursor = conn.cursor()
              if 'prenom' not in SESSION:
                 SESSION['prenom']="NULL"
              cursor.execute("INSERT INTO legos.derouler (prenom, id_partie, joueur_gagnant, score) VALUES (%s,%s,%s,%s);", (SESSION['prenom'],SESSION['partie'],'NULL',SESSION['score']))
              print("insere")
            except psycopg.Error as e:
              print(f"Error: {e}")
              cursor.close()
    print("actionOK")
    placer=True
    coordonnees = set()
    for i in range(SESSION['longeur']):
     for j in range(SESSION['largeur']):
        if f'checkbox_{i}_{j}' in POST and 'on' in POST[f'checkbox_{i}_{j}']:
          print("verification")
          coordonnees.add((i, j))
          if tab[i][j]!=1:
              placer=False
              break
    print("placer:",placer)
    if placer:
       for (i, j) in coordonnees:
          voisin_trouve = False
          for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
              voisin_i = i + di
              voisin_j = j + dj
              print("Vérification voisin pour:", i, j)
            
    
              if 0 <= voisin_i < len(tab) and 0 <= voisin_j < len(tab[0]):
                
                  if (voisin_i, voisin_j) in coordonnees:
                      voisin_trouve = True
                      print(f"Case ({i}, {j}) a un voisin valide: ({voisin_i}, {voisin_j})")
                      break

          if not voisin_trouve and taille_brique!=1:
              placer = False
              print(f"Erreur : la case ({i}, {j}) n'a pas de voisin adjacent.")
              break
        
    if placer==True and len(coordonnees)!=taille_brique:
        placer=False
          
    print("placer2:",placer)
    if (placer==False and taille_brique==1):
       placer==True
    
   
    if placer==True:
      
     print("placer:",placer)
     try:
              cursor = conn.cursor()
              cursor.execute("INSERT INTO legos.tour (id_partie, numero) VALUES (%s,%s);", (SESSION['partie'],SESSION['tours']))
              cursor.execute("INSERT INTO legos.action (id_partie, numero, id_b, description) VALUES (%s,%s,%s,%s);", (SESSION['partie'],SESSION['tours'],item_id,'piochee'))
     except psycopg.Error as e:
              print(f"Error: {e}")
     for i in range(SESSION['longeur']):
      for j in range(SESSION['largeur']):
        if f'checkbox_{i}_{j}' in POST and 'on' in POST[f'checkbox_{i}_{j}']:
          tab[i][j]=item_id
          for m in range (len(alea)):
            if alea[m][0]==item_id:
              SESSION['tabcouleur'][i][j]=alea[m][4]
    else:
        SESSION['place']="Les coordonnées ne sont pas correctes."
    SESSION['tab']=tab
    del post_data['bouton_actionplacer']
    SESSION.pop('taille_brique', None)
    SESSION.pop('BRIQUE', None)
    
    
if POST and 'bouton_abandonner' in POST:
    SESSION['score']=999
     
if grille==True:
    if verifier_gagner(tab)==True:
        SESSION['resultat']="Vous avez gagné!"
        try:
              cursor = conn.cursor()
              if 'prenom' not in SESSION:
                SESSION['prenom']="NULL"
              cursor.execute("INSERT INTO legos.derouler (prenom, id_partie, joueur_gagnant, score) VALUES (%s,%s,%s,%s);", (SESSION['prenom'],SESSION['partie'],SESSION['prenom'],SESSION['score']))
              
        except psycopg.Error as e:
              print(f"Error: {e}")
        cursor.close()

if POST and 'bouton_recommencer' in POST:
    post_data = POST.copy()
  
    SESSION.pop('largeur', None)
    SESSION.pop('longeur', None)
    SESSION.pop('message_tab', None)
    SESSION.pop('tab', None)
    SESSION.pop('tabcouleur', None)
    if 'nbre_tours' in POST:
        del post_data['nbre_tours']
    SESSION.pop('tours_rest', None)
    SESSION.pop('tours_max', None)
    if 'mode' in POST:
        del post_data['mode']
    SESSION.pop('mode', None)
    if 'prenom' in POST:
        del post_data['prenom']
    SESSION.pop('prenom', None)
    if 'start' in POST:
        del post_data['start']
    SESSION.pop('start_tir', None)
    SESSION.pop('debut', None)
    SESSION.pop('score', None)
    SESSION.pop('tours', None)
    SESSION.pop('message_mode', None)
    SESSION.pop('ALEA', None)
    if 'bouton_pressed' in POST:
        del post_data['bouton_pressed']
    SESSION.pop('CHOISI', None)
    
    SESSION.pop('place', None)
    SESSION.pop('taille_brique', None)
    SESSION.pop('resultat', None)
    SESSION.pop('fin', None)
    
    
if conn:
    conn.close()
