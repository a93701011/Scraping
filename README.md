# Scraping news from website
### Run application
```
  $ python new.py  #import news
  $ ptyhon new+analysis.py # jieba analysis
```
### news Functions
1. add all daily highlight news from [端傳媒](https://theinitium.com/)
2. view the news 
3. search new with the keyword
  * search keyword : 主義
  
  ![Image of search](https://github.com/a93701011/Scraping/blob/master/pic/sr_kword.PNG)
  * search result
  
  ![Image of search](https://github.com/a93701011/Scraping/blob/master/pic/search.PNG)
### analysis Functions
1. jeiba analysis
2. view the news
  * view the contenxt keys form the jieba analysis package
  ![Image of analysis](https://github.com/a93701011/Scraping/blob/master/pic/keys_word.PNG)
  
### Code
* scarpe, extract, parse information
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
* jieba analysis
```python
def add_analysis():
    """ jieba keys word """ 
    news = Daily_news.select().order_by(Daily_news.timestamp.desc())
    for new in news:
        content_key_list = jieba.analyse.extract_tags(new.content, topK=20, withWeight=False, allowPOS=())
        str_content = ",".join(content_key_list)
        Daily_news_Keys.create(title = new.title, content = new.content, keys =  str_content )

```
