from wordpress_xmlrpc import Client
from wordpress_xmlrpc.methods import posts
from wordpress_xmlrpc import Client, WordPressPost
from slugify import slugify
import requests
import os.path
from bs4 import BeautifulSoup

client = Client('http://local.wordpress.dev/xmlrpc.php', 'xmlrpc', 'password')

def getPage(url, filename):
    if filename == '':
        print "No File Name"
        exit()
    c = ''
    if os.path.isfile('pages/'+filename):
        print("Loading the data via the file.")
        f = open('pages/'+filename, 'r')
        c = f.read()
    else:
        print("Fetching the data via the URL.")
        result = requests.get(url)
        c = result.content
        f = open('pages/'+filename,'w')
        f.write(c)
    f.close()
    c = BeautifulSoup(c)
    return c

html = getPage("http://news.ycombinator.com/", "page1.html")

rows = html.select('#hnmain > tr:nth-of-type(3) > td > table > tr');

for row in rows:
    if row.select('.title'):
        link = row.select('td:nth-of-type(3) a')
        print link[0].texts
        post = WordPressPost()
        post.title = link[0].text
        post.post_type = "post"
        post.content = link[0].get('href')
        post.post_status = "publish"
        addpost = client.call(posts.NewPost(post))
