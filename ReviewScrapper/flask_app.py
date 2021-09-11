from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from index import index_page

app = Flask(__name__)
app.register_blueprint(index_page)


app.run(port=5000,debug=True)