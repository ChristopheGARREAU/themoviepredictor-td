#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
TheMoviePredictor script
Author: Arnaud de Mouhy <arnaud@admds.net>
"""

import mysql.connector
import sys
import argparse
import csv

def connectToDatabase():
    return mysql.connector.connect(user='predictor', password='predictor',
                              host='127.0.0.1',
                              database='predictor')

def disconnectDatabase(cnx):
    cnx.close()

def createCursor(cnx):
    return cnx.cursor(dictionary=True)

def closeCursor(cursor):    
    cursor.close()

def findQuery(table, id):
    return ("SELECT * FROM {} WHERE id = {}".format(table, id))

def findAllQuery(table):
    return ("SELECT * FROM {}".format(table))

def insertpeopleQuery(first_name, last_name):
    return ("INSERT INTO people (`firstname`, `lastname`) VALUES ('{}', '{}')".format(first_name, last_name))

def find(table, id):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    query = findQuery(table, id)
    cursor.execute(query)
    results = cursor.fetchall()
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return results

def findAll(table):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    cursor.execute(findAllQuery(table))
    results = cursor.fetchall()
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return results

def insertpeople(first_name, last_name):
    cnx = connectToDatabase()
    cursor = createCursor(cnx)
    results = cursor.execute(insertpeopleQuery(first_name, last_name))
    cnx.commit()
    closeCursor(cursor)
    disconnectDatabase(cnx)
    return results

def printPerson(person):
    print("#{}: {} {}".format(person['id'], person['firstname'], person['lastname']))

def printMovie(movie):
    print("#{}: {} released on {}".format(movie['id'], movie['title'], movie['release_date']))

parser = argparse.ArgumentParser(description='Process MoviePredictor data')

parser.add_argument('context', choices=['people', 'movies'], help='Le contexte dans lequel nous allons travailler')

action_subparser = parser.add_subparsers(title='action', dest='action')

list_parser = action_subparser.add_parser('list', help='Liste les entitÃ©es du contexte')
list_parser.add_argument('--export' , help='Chemin du fichier exportÃ©')

find_parser = action_subparser.add_parser('find', help='Trouve une entitÃ© selon un paramÃ¨tre')
find_parser.add_argument('id' , help='Identifant Ã  rechercher')

insert_parser = action_subparser.add_parser('insert', help='Inserrer un people selon un parmètre')
insert_parser.add_argument('--firstname', help='Prénom du people')
insert_parser.add_argument('--lastname', help='Nom du people')

args = parser.parse_args()

if args.context == "people":
    if args.action == "list":
        people = findAll("people")
        if args.export:
            with open(args.export, 'w', encoding='utf-8', newline='\n') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(people[0].keys())
                for person in people:
                    writer.writerow(person.values())
        else:
            for person in people:
                printPerson(person)
    if args.action == "find":
        peopleId = args.id
        people = find("people", peopleId)
        for person in people:
            printPerson(person)
    if args.action == "insert":
        firstname = args.firstname
        lastname = args.lastname
        people = insertpeople(firstname, lastname)

if args.context == "movies":
    if args.action == "list":  
        movies = findAll("movies")
        for movie in movies:
            printMovie(movie)
    if args.action == "find":  
        movieId = args.id
        movies = find("movies", movieId)
        for movie in movies:
            printMovie(movie)