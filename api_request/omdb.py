import locale
import requests
from datetime import datetime
import os
from dotenv import load_dotenv

class OMDB:
    


    def __init__(self, id):
        self.id = id
        
           
        load_dotenv()
        API_KEY = os.getenv('api_key')

        data = requests.get(f"http://www.omdbapi.com/?apikey={API_KEY}&i={id}").json()

        self.title = data['Title']

        self.duration = int(data['Runtime'].split('m')[0].strip())

        released = data['Released'].strip()
        release_date = datetime.strptime(released, '%d %b %Y')
        release_date_string = release_date.strftime('%Y-%m-%d')
        self.release_date = release_date_string

        self.original_title = data['Title']

        self.rating = data['Rated']
        if self.rating == "PG":
            self.rating = "TP"
        

     
        locale.setlocale(locale.LC_ALL, 'en_US.UTF8')
        if data['BoxOffice'] != "N/A":
            self.revenu = int(locale.atof(data['BoxOffice'].strip("$")))
        else:
            self.revenu = None
        

        self.actors = []
        actor = data['Actors'].split(',')
        for person in range(len(actor)):
            name_separated = actor[person].strip().split(' ')
            self.actors.append(name_separated)
