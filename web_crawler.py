import urllib
from bs4 import BeautifulSoup
import nltk as np

qpage = 'http://www.nndb.com/people/589/000172073/'
# Page we want to visit.
with urllib.request.urlopen(qpage) as response:
    html = response.read()

print(html)

soup = BeautifulSoup(html, 'html.parser')
print(soup.get_text())
