from models import Publisher, Platform, Game
import requests
import pandas as pd
from datetime import date, datetime


def db_initiate_data(db):
    db_initiate_publishers(db)
    db_initiate_platform(db)


def db_initiate_publishers(db):
    r = requests.get('https://en.wikipedia.org/wiki/List_of_video_game_publishers')
    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    df = df_list[1]
    for index, row in df.iterrows():
        publisher = Publisher()
        publisher.name = row['Publisher']
        publisher.headquarters = row['Headquarters']
        publisher.established = row['Est.']
        try:
            db.session.add(publisher)
            db.session.commit()
        except:
            db.session.rollback()
    return df.to_string()


def db_initiate_platform(db):
    r = requests.get('https://en.wikipedia.org/wiki/List_of_best-selling_game_consoles')
    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    df = df_list[0]
    for index, row in df.iterrows():
        platform = Platform()
        platform.name = row['Platform'].replace('#', '').rstrip()
        platform.released = row['Released[2]']
        publisher = db.session.query(Publisher).filter_by(name=row['Firm']).first()
        if publisher is None:
            publisher = Publisher()
            publisher.name = row['Firm']
            db.session.add(publisher)
            db.session.commit()
        platform.publisher_id = publisher.id
        try:
            db.session.add(platform)
            db.session.commit()
        except:
            db.session.rollback()
    return df.to_string()


def db_initiate_game(db):
    year = date.today().strftime('%Y')
    month = date.today().strftime('%m')
    r = requests.get(f'http://www.gameblog.fr/sorties.php?mois={year}-{month}')
    df_list = pd.read_html(r.text)  # this parses all the tables in webpages to a list
    df = df_list[1]
    for index, row in df.iterrows():
        game = Game()
        game.name = row['Nom']
        if row['Sortie'].count('/') == 2:
            game.release_date = datetime.strptime(row['Sortie'],'%d/%m%y')
        elif row['Sortie'].count('/') == 1:
            game.release_date = datetime.strptime(row['Sortie'], '%m%Y')
        publisher = db.session.query(Publisher).filter_by(name=row['Firm']).first()
        if publisher is None:
            publisher = Publisher()
            publisher.name = row['Firm']
            db.session.add(publisher)
            db.session.commit()
        platform.publisher_id = publisher.id
        try:
            db.session.add(platform)
            db.session.commit()
        except:
            db.session.rollback()
    return df.to_string()
