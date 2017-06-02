# Scraping news from website
### Run application
'''
  $ python new.py
'''
### Functions
1. add all daily highlight news from [端傳媒](https://theinitium.com/)
2. view the news 
3. search new with the keyword
   search keyword : 主義
  ![Image of search](https://github.com/a93701011/Scraping/blob/master/pic/sr_kword.PNG)
   search result
   ![Image of search](https://github.com/a93701011/Scraping/blob/master/pic/search.PNG)
### Code
1. scarpe, extract, parse information
'''
 if r.status_code == requests.codes.ok:
         # Extracts the response as html: html_doc
        html_doc = r.text
        
        # Create a BeautifulSoup object from the HTML: soup
        soup = BeautifulSoup(html_doc,"html.parser")
        
        title_tags = soup.find_all('h4', attrs={'class': 'article-title'})
        intro_tags = soup.find_all('p', attrs={'class': 'article-intro'})
'''
