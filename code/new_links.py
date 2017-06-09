# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 11:57:43 2017

@author: a93701011
"""
from collections import OrderedDict 
import datetime
import sys
import os

import jieba
import jieba.analyse

from peewee import *

import requests
from bs4 import BeautifulSoup
import re

db = SqliteDatabase("news.db")

class Daily_news_org(Model):
    catalog = CharField(max_length = 255)
    section = CharField(max_length = 255)
    title = CharField(max_length = 255)
    content = TextField()
    timestamp = DateTimeField(default = datetime.datetime.now)
    key = TextField()
    
    class Mete:
        database = db 

def clear():
    """Clear screen"""
    os.system("cls" if os.name == 'nt' else "clear")

def initialize():
    """Create the database """
    db.connect()
    db.create_tables([Daily_news_org], safe = True)
    
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

def get_link():
    """get everyone href link """
    url = 'https://theinitium.com'
    response = requests.get(url)
    soup = BeautifulSoup(response.content,"html.parser")

    section_all = soup.find_all('div', attrs={'class': 'nav-section'})

    section_dist = dict()
    #{"專題":{"世界公民在香港":"href"}}
    for section in section_all:
        link_dist = {}
        # print(section.h2.text)
        links_all_tags = section.ul.find_all('a')
        for link in links_all_tags:
            # print(url + link['href'])
            link_text = re.search(r"[^\n\W]+",link.text).group()
            link_dist[link_text] = url + link['href']
        section_dist[section.h2.text] = link_dist
#    print(section_dist)
    return section_dist
    #頻道 #專題
    #first_tag = section_all.find('h2', attrs={'class': 'nav-section-title'}).parent
    #second_tag = soup.find('h2', attrs={'class': 'nav-section-title'}).parent.find_next_sibling()

    
def get_content(url):   
    '''get title content from website '''    
    # Package the request, send the request and catch the response: r
    r = requests.get(url)
    nn =list()
    if r.status_code == requests.codes.ok:
    # Extracts the response as html: html_doc
        html_doc = r.text
            
        # Create a BeautifulSoup object from the HTML: soup
        soup = BeautifulSoup(html_doc,"html.parser")
            
        title_tags = soup.find_all('h4', attrs={'class': 'article-title'})
        intro_tags = soup.find_all('p', attrs={'class': 'article-intro'})
            
        for i in range(len(title_tags)):
            dd = dict()
            dd["title"] = title_tags[i].text
            dd["intro"] = intro_tags[i].text    
            nn.append(dd)
    return nn 

def add_news():
    """ add all record """
    link_dict = get_link()
    for catalog , value in link_dict.items():
        for section, value in value.items():
#            print()
            for new in get_content(value):
                if new != list():
                    print(new["title"])
                    print(catalog)
                    print(section)
                    Daily_news_org.create(catalog = catalog, section = section, title = new["title"], content = new["intro"])
    print("Add Successfully!")

def view_entries(search_query = None ):
    """ view the entries """
    entries = Daily_news_org.select().order_by(Daily_news_org.timestamp.desc())
    if search_query != None:
        entries = entries.where(Daily_news_org.title.contains(search_query))
    
    for entry in entries:
        timestamp = entry.timestamp.strftime('%A %B %d, %Y %I:%M%p')
        clear()
        print(timestamp)
        print("="*len(timestamp))
        print("catalog:")
        print(entry.catalog)
        print("section:")
        print(entry.section)
        print("\n"+"="*len(timestamp))
        print(entry.title)
        print(entry.content)
        print("\n"+"="*len(timestamp))
        print("key:")
        print(entry.key)
        analysis_key = add_analysis(entry.content)
        #print(analysis_key)
        print("\n"+"="*len(timestamp))
        print("n) next content")
        print("d) delete the entry")
        print("q) back to menu")
        print("a) add analysis key")    
        next_action = input("Action: [Ndq] ").lower()
        if next_action == 'q':
            break
        elif next_action == 'd':
            delete_entry(entry)
        elif next_action == 'a':
            print(entry.id)
            add_key(entry.id, analysis_key)
           
def add_key(number, string):
    """ updata a record's keys"""
    if input("Are you sure to add analysis keys? [Yn] ").lower() != "n":
        q = Daily_news_org.update( key = string).where(Daily_news_org.id == number)
        q.execute()

def add_all_key(search_query):
    """ updata all records' keys"""
    entries = Daily_news_org.select().order_by(Daily_news_org.timestamp.desc())
    if search_query != None:
        entries = entries.where(Daily_news_org.title.contains(search_query)) 
    for entry in entries:
        analysis_key = add_analysis(entry.content)
        q = Daily_news_org.update( key = analysis_key).where(Daily_news_org.id == entry.id)
        q.execute()
    
def add_analysis(string):
    """ jieba keys word analysis """ 
    #news = Daily_news_org.select().order_by(Daily_news_org.timestamp.desc())
    content_key_list = jieba.analyse.extract_tags(string, topK=20, withWeight=False, allowPOS=())
    str_content = ",".join(content_key_list)
    return str_content
         
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
        ("s",search_entry),
        ("n",add_all_key)
        
    ])

if __name__ == "__main__":
    initialize()
    menu_loop()