from controleurs.includes import add_activity
import toml
import psycopg
from psycopg.sql import SQL, Identifier
import flask
from flask import Flask, request, redirect, url_for, session
app = Flask(__name__)
from model.model_pg import get_nb, get_couleurs, get_nbinstances, get_score, get_partie, get_moyenne, top_parties

add_activity(SESSION['HISTORIQUE'], "consultation de page d'acceuil")

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



if POST:
    if 'bouton_validertab' in POST:
        
        if all(_ in POST for _ in ['tab1', 'tab2', 'tab3']):
            SESSION['tab1'] = POST['tab1']
            SESSION['tab2'] = POST['tab2']
            SESSION['tab3'] = POST['tab3']
            SESSION['tabinstances'] = get_nbinstances(
                conn, SQL, Identifier, POST['tab1'][0], POST['tab2'][0], POST['tab3'][0]
            )
        else:
            print("Erreur")

    elif 'bouton_validercouleur' in POST:
        SESSION['5couleurs'] = get_couleurs(conn, SQL, Identifier)
    elif 'bouton_validerscore' in POST:
        result = get_score(conn, SQL, Identifier)
        if result is not None:
            SESSION['score_maxmin'] = result
    elif 'bouton_validergp' in POST:
         result = get_partie(conn, SQL, Identifier)
         if result is not None:
            SESSION['partie_stats'] = result
    elif 'bouton_validertours' in POST:
        result = get_moyenne(conn, SQL, Identifier)
        if result is not None:
            SESSION['moyenne_tours'] = result

    elif 'bouton_validerparties' in POST:
        result = top_parties(conn, SQL, Identifier)
        if result is not None:
            SESSION['top_parties'] = result
    
        
        


global alea
if POST and 'start' in POST:
   
   alea=get_alea(conn,SQL,Identifier)
   for a in alea:
      print(a)
   SESSION['ALEA'] = alea


   

if POST and 'bouton_pressed' in POST:
    item_id = int(POST['id'][0])
    print(f"button_pressed:{item_id}")
    SESSION['CHOISI']=item_id
    for i in range(4):
       if alea[i][0]==item_id:
          alea[i]=get_alea(conn,SQL,Identifier)[0]
       


if conn:
    conn.close()


    

