# -*- coding: utf-8 -*-
"""
Created on Sun Jun  4 15:34:08 2017

@author: a93701011
"""

# https://github.com/fxsjy/jieba
# 全自动安装：easy_install jieba 或者 pip install jieba / pip3 install jieba
import jieba
import jieba.analyse

from collections import OrderedDict 
import sys
import os
import datetime
from peewee import *

db = SqliteDatabase("news.db")

class Daily_news(Model):
    title = CharField(max_length = 255)
    content = TextField()
    timestamp = DateTimeField(default = datetime.datetime.now)
    keys = TextField()
    class Mete:
        database = db 
        
class Daily_news_Keys(Model):
    title = CharField(max_length = 255)
    content = TextField()
    keys = TextField()
    class Mete:
        database = db 
        
def clear():
    os.system("cls" if os.name == 'nt' else "clear")

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
       
def initialize():
    """Create the database """
    db.connect()
    db.create_tables([Daily_news], safe = True)
    db.create_tables([Daily_news_Keys], safe = True)

def add_analysis():
    """ jieba keys word """ 
    news = Daily_news.select().order_by(Daily_news.timestamp.desc())
    for new in news:
        content_key_list = jieba.analyse.extract_tags(new.content, topK=20, withWeight=False, allowPOS=())
        str_content = ",".join(content_key_list)
        Daily_news_Keys.create(title = new.title, content = new.content, keys =  str_content )

def view_entries(search_query = None ):
    """ view the entries """
    entries = Daily_news_Keys.select()
    if search_query != None:
        entries = entries.where(Daily_news_Keys.title.contains(search_query))
    
    for entry in entries:

        clear()
        print(entry.title)
        print("="*len(entry.title))
        print(entry.content)
        print("keys:")
        print(entry.keys)
        print("\n\n"+"="*len(entry.title))
        print("n) next content")
        print("q) back to menu")
    
        next_action = input("Action: [Ndq] ").lower()
        if next_action == 'q':
            break

menu = OrderedDict([
        ("a",add_analysis),
        ("v",view_entries),
        
    ])
         
if __name__ == "__main__":
    initialize()
    menu_loop()