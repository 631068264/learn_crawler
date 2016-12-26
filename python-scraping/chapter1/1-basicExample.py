# Retrieve HTML string from the URL
from urllib2 import urlopen

html = urlopen("http://www.pythonscraping.com/exercises/exercise1.html")
print(html.read())
