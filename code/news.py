# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 12:59:22 2017

@author: a93701011
"""
from collections import OrderedDict 
import datetime
import sys
import os

from peewee import *

import requests
from bs4 import BeautifulSoup
import re

db = SqliteDatabase("news.db")


class Daily_news(Model):
    title = CharField(max_length = 255)
    content = TextField()
    timestamp = DateTimeField(default = datetime.datetime.now)
    keys = TextField()
    class Mete:
        database = db 

def clear():
    os.system("cls" if os.name == 'nt' else "clear")

def initialize():
    """Create the database """
    db.connect()
    db.create_tables([Daily_news], safe = True)
    
def menu_loop():
    """ show the menu """
    choice = None

    while choice != "q":
        clear()
        print("Enter 'q' to leave")
        for key, value in menu.items():
            print("{}) {}".format(key, value.__doc__))
        choice = input("Action:").lower().strip()
    
        if choice in menu:
            clear()
            menu[choice]()
            
def get_data():
# Specify url: url
    url = 'https://theinitium.com/'
    
    # Package the request, send the request and catch the response: r
    r = requests.get(url)

    if r.status_code == requests.codes.ok:
         # Extracts the response as html: html_doc
        html_doc = r.text
        
        # Create a BeautifulSoup object from the HTML: soup
        soup = BeautifulSoup(html_doc,"html.parser")
        
        title_tags = soup.find_all('h4', attrs={'class': 'article-title'})
        intro_tags = soup.find_all('p', attrs={'class': 'article-intro'})
        
    nn = []
    for i in range(len(title_tags)):
        dd = dict()
        title_body = re.search(r"[^class]+", title_tags[i].text)
        dd["title"] = title_body.group()
        intro_body = re.search(r"[^class]+", intro_tags[i].text)
        dd["intro"] = intro_body.group()    
        nn.append(dd)
    return nn 

def add_news():
    """ add a entry """
    for new in get_data():
        Daily_news.create(title = new["title"], content = new["intro"])
    print("Add Successfully!")

def view_entries(search_query = None ):
    """ view the entries """
    entries = Daily_news.select().order_by(Daily_news.timestamp.desc())
    if search_query != None:
        entries = entries.where(Daily_news.title.contains(search_query))
    
    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print("="*len(timestamp))
        print(entry.title)
        print(entry.content)
        print("keys:")
        print(entry.keys)
        print("\n\n"+"="*len(timestamp))
        print("n) next content")
        print("d) delete the entry")
        print("q) back to menu")
    
        next_action = input("Action: [Ndq] ").lower()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)
            
def delete_entry(entry):
    """ delete a entry """
    if input("Are you sure to delete? [Yn] ").lower() != "n":
        entry.delete_instance()
    print("Entry deleted!")
    
    
def search_entry():
     """ search entry with a string"""
     view_entries(input("Enter search query: ").lower())
    

menu = OrderedDict([
        ("a",add_news),
        ("v",view_entries),
        ("s",search_entry)
        
    ])


if __name__ == "__main__":
    initialize()
    menu_loop()