#!/usr/bin/env python3
# 
# A buggy web service in need of a database.

from flask import Flask, request, redirect, url_for
from newsdb import get_most_popular_articles,get_most_popular_authors,get_most_errors
app = Flask(__name__)

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>DB Forum</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { border: 1px solid #999;
                 padding: 10px 10px;
                 margin: 10px 20%%; }
      hr.postbound { width: 50%%; }
      em.date { color: #999 }
    </style>
  </head>
  <body>
  <ul>
    <!-- post content will go here -->
  %s
   </ul>
  </body>
</html>
'''

# HTML template for an individual comment
POST = '''\
    <li><em class=date>%s</em><em class=total>%s</em></li>
'''


@app.route('/', methods=['GET'])
def main():
  '''Main page of the forum.'''
  data = "".join(POST % (path, total) for path, total in get_most_popular_articles())
  html = HTML_WRAP % data
  return html

@app.route('/authors', methods=['GET'])
def authors():
  '''Main page of the forum.'''
  data = "".join(POST % (name, total) for name, total in get_most_popular_authors())
  html = HTML_WRAP % data
  return html

@app.route('/errors', methods=['GET'])
def errors():
  '''Main page of the forum.'''
  data = "".join(POST % (date, total*100+'%') for date, total in get_most_errors())
  html = HTML_WRAP % data
  return html


if __name__ == '__main__' or __name__ == '__authors__' or __name__ == '__errors__':
  app.run(host='0.0.0.0', port=8000)

