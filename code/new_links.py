# -*- coding: utf-8 -*-
"""
Created on Thu Jun  8 11:57:43 2017

@author: a93701011
"""

import requests
from bs4 import BeautifulSoup
import re

def get_link():
    url = 'https://theinitium.com'
    re = requests.get(url)
    soup = BeautifulSoup(re.content,"html.parser")

    section_all = soup.find_all('div', attrs={'class': 'nav-section'})

    section_dist = {}
    #{"專題":{"世界公民在香港":"href"}}
    for section in section_all:
        link_dist = {}
        # print(section.h2.text)
        links_all_tags = section.ul.find_all('a')
        for link in links_all_tags:
            # print(url + link['href'])
            link_dist[link.text] = url + link['href']
        section_dist[section.h2.text] = link_dist
    
    #頻道 #專題
    #first_tag = section_all.find('h2', attrs={'class': 'nav-section-title'}).parent
    #second_tag = soup.find('h2', attrs={'class': 'nav-section-title'}).parent.find_next_sibling()


    


def get_data(url):   
    
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
