from flask import Flask
from threading import Thread

app = Flask('')


import logging
log = logging.getLogger('werkzeug')
log.disabled = True


@app.route('/')
def home():
    return "alive"

def run():
  app.run(host='0.0.0.0',port=8082)

def monitoring():
    t = Thread(target=run)
    t.start()