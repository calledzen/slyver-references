import datetime

from flask import Flask, render_template
from threading import Thread
import utils.database as db

from dotenv import load_dotenv

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True


#import logging
#log = logging.getLogger('werkzeug')
#log.disabled = True

load_dotenv()
db.connect("mariadb")
db.tableSetup()


@app.route('/')
def index():

    opendata = db.getData("tickets", "*", "state = 'open'")
    closeddata = db.getData("tickets", "*", "state = 'closed'")
    return render_template('index.html', opendata=opendata, closeddata=closeddata)


def run():
  app.run(host='0.0.0.0',port=8080,debug=True)

def webpanel():
    t = Thread(target=run)
    t.start()


run()