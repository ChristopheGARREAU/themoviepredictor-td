#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TheMoviePredictor script
Author: Arnaud de Mouhy <arnaud@admds.net>
"""

import os
from dotenv import load_dotenv

import mysql.connector
import sys
import argparse
import csv

from movie import Movie
from person import Person
from omdb import OMDB

def connectToDatabase():
    load_dotenv()
    mysql_user = os.getenv('mysql_user')
    mysql_password = os.getenv('mysql_password')
    mysql_host = os.getenv('mysql_host')
    mysql_database = os.getenv('mysql_database')
    return mysql.connector.connect(user=mysql_user, password=mysql_password,
                              host=mysql_host,
                              database=mysql_database)
    # return mysql.connector.connect(user='predictor', password='predictor', host='database', database='predictor')

def disconnectDatabase(cnx):
    cnx.close()

def createCursor(cnx):
    return cnx.cursor(dictionary=True)

def closeCursor(cursor):    
    cursor.close()

def findQuery(table, id):
    return ("SELECT * FROM {} WHERE id = {} LIMIT 1".format(table, id))

def findAllQuery(table):
    return ("SELECT * FROM {}".format(table))

def insert_people_query(person):
    return (f"INSERT INTO `people` (`firstname`, `lastname`) VALUES ('{person.firstname}', '{person.lastname}');")

def insert_movie_query(movie):  # méthode cursor connector statement pour gérer quand donnée manque
    add_movie = (
        "INSERT INTO `movies` (`title`, `original_title`, `duration`, `rating`, `release_date`, `revenu`, `imdbId`)"
        "VALUES (%(title)s, %(original_title)s, %(duration)s, %(rating)s, %(release_date)s, %(revenu)s, %(imdbId)s)"
    )    
    data_movie = {
        'title' : movie.title,
        'original_title' : movie.original_title,
        'duration' : movie.duration,
        'rating' : movie.rating,
        'release_date' : movie.release_date,
        'revenu' : movie.revenu,
        'imdbId' : movie.imdbId}
    return (add_movie, data_movie)

def insert_movie_people_rule_query(movie_id, person_id, rule_id):
    return(f"INSERT INTO `movies_people_rules` (`movie_id`, `people_id`, `rule_id`) VALUES ('{movie_id}', '{person_id}', '{rule_id}');")

def find(table, id):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    query = findQuery(table, id)
    cursor.execute(query)
    results = cursor.fetchall()

    entity = None
    if (cursor.rowcount == 1):
        row = results[0]
        if (table == "movies"):
            entity = Movie(row['title'], row['original_title'], row['duration'], row['release_date'], row['rating'])

        if (table == "people"):
            entity = Person(
                row['firstname'],
                row['lastname']
            )
        
        entity.id = row['id']

    closeCursor(cursor)
    disconnectDatabase(cnx)

    return entity

def findAll(table):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(findAllQuery(table))
    results = cursor.fetchall() # liste de dictionnaires contenant des valeurs scalaires
    closeCursor(cursor)
    disconnectDatabase(cnx)
    if (table == "movies"):
        movies = []
        for result in results: # result: dictionnaire avec id, title, ...
            movie = Movie(
                title=result['title'],
                original_title=result['original_title'],
                duration=result['duration'],
                release_date=result['release_date'],
                rating=result['rating']
            )
            movie.id = result['id']
            movies.append(movie)
        return movies

    if (table == "people"):
        people = []
        for result in results: # result: dictionnaire avec id, title, ...
            person = Person(
                firstname=result['firstname'],
                lastname=result['lastname'],
            )
            person.id = result['id']
            people.append(person)
        return people

def insert_people(person):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(insert_people_query(person))
    cnx.commit()
    last_id = cursor.lastrowid
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return last_id

def insert_movie(movie):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    (add_movie, data_movie) = insert_movie_query(movie) # méthode cursor connector statement suite
    cursor.execute(add_movie, data_movie)
    cnx.commit()
    last_id = cursor.lastrowid
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return last_id

def insert_movie_people_rule(movie_id, person_id, rule_id):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(insert_movie_people_rule_query(movie_id, person_id, rule_id))
    cnx.commit()
    last_id = cursor.lastrowid
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return last_id

def printPerson(person):
    print("#{}: {} {}".format(person.id, person.firstname, person.lastname))

def printMovie(movie):
    print("#{}: {} released on {}".format(movie.id, movie.title, movie.release_date))

parser = argparse.ArgumentParser(description='Process MoviePredictor data')

parser.add_argument('context', choices=('people', 'movies', 'import'), help='Le contexte dans lequel nous allons travailler')

known_args = parser.parse_known_args()[0]
if known_args.context == "import":
    parser.add_argument('--api', help='API utilisé', required=True)
    parser.add_argument('--imdbId', help='Id IMDB du film cherché', required=True)

action_subparser = parser.add_subparsers(title='action', dest='action')

list_parser = action_subparser.add_parser('list', help='Liste les entitées du contexte')
list_parser.add_argument('--export' , help='Chemin du fichier exporté')

find_parser = action_subparser.add_parser('find', help='Trouve une entité selon un paramètre')
find_parser.add_argument('id' , help='Identifant à rechercher')

import_parser = action_subparser.add_parser('import', help='Importer un fichier CSV')
import_parser.add_argument('--file', help='Chemin vers le fichier à importer', required=True)

insert_parser = action_subparser.add_parser('insert', help='Insert une nouvelle entité')
known_args = parser.parse_known_args()[0]

if known_args.context == "people":
    insert_parser.add_argument('--firstname' , help='Prénom de la nouvelle personne', required=True)
    insert_parser.add_argument('--lastname' , help='Nom de la nouvelle personne', required=True)

if known_args.context == "movies":
    insert_parser.add_argument('--title' , help='Titre en France', required=True)
    insert_parser.add_argument('--duration' , help='Durée du film', type=int, required=True)
    insert_parser.add_argument('--original-title' , help='Titre original', required=True)
    insert_parser.add_argument('--release-date' , help='Date de sortie en France', required=True)
    insert_parser.add_argument('--rating' , help='Classification du film', choices=('TP', '-12', '-16'), required=True)





args = parser.parse_args()
#print(args)
if args.context == "people":
    if args.action == "list":
        people = findAll("people")
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].__dict__.keys())
                for person in people:
                    writer.writerow(person.__dict__.values())
        else:
            for person in people:
                printPerson(person)
    if args.action == "find":
        peopleId = args.id
        person = find("people", peopleId)
        printPerson(person)
    if args.action == "insert":
        print(f"Insertion d'une nouvelle personne: {args.firstname} {args.lastname}")
        person = Person(
            firstname=args.firstname,
            lastname=args.lastname
        )
        people_id = insert_people(person)
        print(f"Nouvelle personne insérée avec l'id '{people_id}'")

if args.context == "movies":
    if args.action == "list":  
        movies = findAll("movies")
        for movie in movies:
            printMovie(movie)
    if args.action == "find":  
        movieId = args.id
        movie = find("movies", movieId)
        if (movie == None):
            print(f"Aucun film avec l'id {movieId} n'a été trouvé ! Try Again!")
        else:
            printMovie(movie)
    if args.action == "insert":
        print(f"Insertion d'un nouveau film: {args.title}")
        movie = Movie(args.title, args.original_title, args.duration, args.release_date, args.rating)
        movie_id = insert_movie(movie)
        print(f"Nouveau film inséré avec l'id '{movie_id}'")
    if args.action == "import":
        with open(args.file, 'r', encoding='utf-8', newline='\n') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                movie_id = insert_movie(
                    title=row['title'],
                    original_title=row['original_title'],
                    duration=row['duration'],
                    rating=row['rating'],
                    release_date=row['release_date']
                )
                print(f"Nouveau film inséré avec l'id '{movie_id}'")

if args.context == "import":
    nouveau_film = OMDB(args.imdbId)
    movie= Movie(nouveau_film.title, nouveau_film.original_title, nouveau_film.duration, nouveau_film.release_date, nouveau_film.rating)
    movie.revenu = nouveau_film.revenu
    movie.imdbId = nouveau_film.imdbId
    movie_id = insert_movie(movie)
    print(f"Nouveau film inséré avec l'id '{movie_id}'")
    for person in range(len(nouveau_film.actors)):
        actor = Person(
            firstname = nouveau_film.actors[person][0],
            lastname = nouveau_film.actors[person][1])
        actor_id = insert_people(actor)
        insert_movie_people_rule(movie_id, actor_id, 1)
        print(f"Nouvelle personne insérée avec l'id '{actor_id}' avec le rule '{1}")
    for person in range(len(nouveau_film.directors)):
        director = Person(
            firstname = nouveau_film.directors[person][0],
            lastname = nouveau_film.directors[person][1])
        director_id = insert_people(director)
        insert_movie_people_rule(movie_id, director_id, 2)
        print(f"Nouvelle personne insérée avec l'id '{director_id}' avec le rule '{2}")
    
