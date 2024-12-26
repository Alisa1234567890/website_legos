import psycopg
from psycopg.sql import SQL, Identifier
from logzero import logger

def get_alea(conn,SQL,Identifier):
   try:
        cursor = conn.cursor()
        query = SQL("SELECT * FROM {schema}.{table} WHERE longueur <=2 OR largeur <=2 ORDER BY RANDOM() LIMIT 4").format(schema=Identifier('legos'),table=Identifier('piece'))
    
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
   except psycopg.Error as e:
        print(f"Error : {e}")
   return None
   
def get_nb(conn,SQL,Identifier,nom_table):
   try:
        cursor = conn.cursor()
        query = SQL("SELECT COUNT(*) as nb_instances FROM {schema}.{table}").format(schema=Identifier('legos'),table=Identifier(nom_table))
    
        cursor.execute(query)
        rows = cursor.fetchone()[0]
        return rows
   except psycopg.Error as e:
        print(f"Error : {e}")
   return None

def get_nbinstances(conn, SQL, Identifier, nom_table1, nom_table2, nom_table3):
    tab = [0, 0, 0]
    tab[0]=get_nb(conn,SQL,Identifier,nom_table1)
    tab[1]=get_nb(conn,SQL,Identifier,nom_table2)
    tab[2]=get_nb(conn,SQL,Identifier,nom_table3)
    return tab


   
def get_couleurs(conn,SQL,Identifier):
   try:
        cursor = conn.cursor()
        query = SQL("SELECT couleur, COUNT(*) AS nb_briques FROM {schema}.{table} GROUP BY couleur ORDER BY nb_briques DESC LIMIT 5").format(schema=Identifier('legos'),table=Identifier('piece'))
    
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
   except psycopg.Error as e:
        print(f"Error : {e}")
   return None
   
def get_score(conn,SQL,Identifier):
   try:
        cursor = conn.cursor()
        query = SQL("SELECT  J.prenom, MIN(D.score) AS score_minimal, MAX(D.score) AS score_maximal FROM {schema}.{table1} J LEFT JOIN {schema}.{table2} D ON J.prenom = D.prenom GROUP BY  J.prenom;").format(schema=Identifier('legos'),table1=Identifier('joueur'),table2=Identifier('derouler'))
    
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
   except psycopg.Error as e:
        print(f"Error : {e}")
   return None
   
def get_partiegf(conn, SQL, Identifier):
    try:
        cursor = conn.cursor()
        query = SQL(" SELECT id_partie, COUNT(*) AS occurrences FROM {schema}.{table} WHERE description = 'defaussee' GROUP BY id_partie ORDER BY occurrences DESC LIMIT 1;").format(schema=Identifier('legos'), table=Identifier('action'))
        
        cursor.execute(query)
        return cursor.fetchall()
    except psycopg.Error as e:
        print(f"Error: {e}")
        return None


def get_partiepf(conn, SQL, Identifier):
    try:
        cursor = conn.cursor()
        query = SQL("SELECT id_partie, COUNT(*) AS occurrences FROM {schema}.{table} WHERE description = 'defaussee' GROUP BY id_partie ORDER BY occurrences ASC LIMIT 1;").format(schema=Identifier('legos'), table=Identifier('action'))
        
        cursor.execute(query)
        return cursor.fetchall()
    except psycopg.Error as e:
        print(f"Error: {e}")
        return None


def get_partiegp(conn, SQL, Identifier):
    try:
        cursor = conn.cursor()
        query = SQL("SELECT id_partie, COUNT(*) AS occurrences FROM {schema}.{table} WHERE description = 'piochee' GROUP BY id_partie ORDER BY occurrences DESC LIMIT 1;").format(schema=Identifier('legos'), table=Identifier('action'))
        
        cursor.execute(query)
        return cursor.fetchall()
    except psycopg.Error as e:
        print(f"Error: {e}")
        return None


def get_partiepp(conn, SQL, Identifier):
    try:
        cursor = conn.cursor()
        query = SQL("SELECT id_partie, COUNT(*) AS occurrences FROM {schema}.{table} WHERE description = 'piochee' GROUP BY id_partie ORDER BY occurrences ASC LIMIT 1; ").format(schema=Identifier('legos'), table=Identifier('action'))
        
        cursor.execute(query)
        return cursor.fetchall()
    except psycopg.Error as e:
        print(f"Error: {e}")
        return None


def get_partie(conn, SQL, Identifier):
    try:
        max_defaussee = get_partiegf(conn, SQL, Identifier)
        min_defaussee = get_partiepf(conn, SQL, Identifier)
        max_piochee = get_partiegp(conn, SQL, Identifier)
        min_piochee = get_partiepp(conn, SQL, Identifier)
        
        return {
            "max_defaussee": max_defaussee,
            "min_defaussee": min_defaussee,
            "max_piochee": max_piochee,
            "min_piochee": min_piochee
        }
    except Exception as e:
        print(f"Erreur lors de l'obtention des statistiques : {e}")
        return None


def get_moyenne(conn,SQL,Identifier):
   try:
        cursor = conn.cursor()
        query = SQL("SELECT EXTRACT(YEAR FROM TO_DATE(tc.date_debut, 'YYYY-MM-DD')) AS year, EXTRACT(MONTH FROM TO_DATE(tc.date_debut, 'YYYY-MM-DD')) AS month, AVG(tc.total_tours) AS avg_tours FROM (SELECT p.date_debut, COUNT(t.numero) AS total_tours FROM {schema1}.{table1} t JOIN {schema2}.{table2} p ON t.id_partie = p.id_partie GROUP BY p.date_debut) AS tc GROUP BY year, month ORDER BY year, month; ").format(schema1=Identifier('legos'),table1=Identifier('tour'),schema2=Identifier('legos'),table2=Identifier('partie'))
    
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
   except psycopg.Error as e:
        print(f"Error : {e}")
   return None
   
def top_parties(conn,SQL,Identifier):
   try:
        cursor = conn.cursor()
        query = SQL("SELECT id_partie, MAX (p.longeur * p.largeur) AS max_surface, COUNT (*) AS total_pieces FROM {schema}.{table1} a INNER JOIN {schema}.{table2} p ON a.id_b = p.id_b GROUP BY id_partie ORDER BY total_pieces DESC, max_surface DESC LIMIT 3;").format(schema=Identifier('legos'),table1=Identifier('action'),table2=Identifier('piece'))
    
        cursor.execute(query)
        rows = cursor.fetchall()
        return rows
   except psycopg.Error as e:
        print(f"Error : {e}")
   return None
   

def get_connexion(host, username, password, db, schema):
   try:
       connexion = psycopg.connect(host=host, user=username, password=password, dbname=db, autocommit=True)
        # on sélectionne le schéma par une requête SET
       cursor = psycopg.ClientCursor(connexion)
       cursor.execute("SET search_path TO %s", [schema])
   except Exception as e:
       print(e)
       return None
   return connexion

def execute_select_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête SELECT (qui peut retourner plusieurs instances).
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.fetchall()
            return result 
        except psycopg.Error as e:
            logger.error(e)
    return None

def execute_other_query(connexion, query, params=[]):
    """
    Méthode générique pour exécuter une requête INSERT, UPDATE, DELETE.
    Utilisée par des fonctions plus spécifiques.
    """
    with connexion.cursor() as cursor:
        try:
            cursor.execute(query, params)
            result = cursor.rowcount
            return result 
        except psycopg.Error as e:
            logger.error(e)
    return None

def get_instances(connexion, nom_table):
    """
    Retourne les instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT * FROM {table}').format(table=sql.Identifier(nom_table), )
    return execute_select_query(connexion, query)

def count_instances(connexion, nom_table):
    """
    Retourne le nombre d'instances de la table nom_table
    String nom_table : nom de la table
    """
    query = sql.SQL('SELECT COUNT(*) AS nb FROM {table}').format(table=sql.Identifier(nom_table))
    return execute_select_query(connexion, query)

def get_episodes_for_num(connexion, numero):
    """
    Retourne le titre des épisodes numérotés numero
    Integer numero : numéro des épisodes
    """
    query = 'SELECT titre FROM episodes where numéro=%s'
    return execute_select_query(connexion, query, [numero])

def get_serie_by_name(connexion, nom_serie):
    """
    Retourne les informations sur la série nom_serie (utilisé pour vérifier qu'une série existe)
    String nom_serie : nom de la série
    """
    query = 'SELECT * FROM series where nomsérie=%s'
    return execute_select_query(connexion, query, [nom_serie])

def insert_serie(connexion, nom_serie):
    """
    Insère une nouvelle série dans la BD
    String nom_serie : nom de la série
    Retourne le nombre de tuples insérés, ou None
    """
    query = 'INSERT INTO series VALUES(%s)'
    return execute_other_query(connexion, query, [nom_serie])

def get_table_like(connexion, nom_table, like_pattern):
    """
    Retourne les instances de la table nom_table dont le nom correspond au motif like_pattern
    String nom_table : nom de la table
    String like_pattern : motif pour une requête LIKE
    """
    motif = '%' + like_pattern + '%'
    nom_att = 'nomsérie'  # nom attribut dans séries (à éviter)
    if nom_table == 'actrices':  # à éviter
        nom_att = 'nom'  # nom attribut dans actrices (à éviter)
    query = sql.SQL("SELECT * FROM {} WHERE {} ILIKE {}").format(
        sql.Identifier(nom_table),
        sql.Identifier(nom_att),
        sql.Placeholder())
    #    like_pattern=sql.Placeholder(name=like_pattern))
    return execute_select_query(connexion, query, [motif])



