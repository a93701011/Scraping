# Scraping news from website
### Run application
```
  $ python new.py
```
### Functions
1. add all daily highlight news from [端傳媒](https://theinitium.com/)
2. view the news 
3. search new with the keyword
  1. search keyword : 主義
  
  ![Image of search](https://github.com/a93701011/Scraping/blob/master/pic/sr_kword.PNG)
  2. search result
  
  ![Image of search](https://github.com/a93701011/Scraping/blob/master/pic/search.PNG)
### Code
scarpe, extract, parse information
```python
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
        
```
