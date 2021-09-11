from flask import Flask, render_template, request, jsonify, Blueprint, abort
from flask_cors import CORS, cross_origin
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
from DBHelper import DBHelper

index_page = Blueprint('index_page', __name__,
                        template_folder='templates')

@index_page.route('/',  methods=['GET', 'POST'])
def index():
    #Check for type of request
    #Get´
    if request.method == "GET":
        return render_template('index.html') 
    #POst
    searchString = request.form['content']
    
    #Create collection object
    # dbConn = pymongo.MongoClient("mongodb://localhost:27017")    
    # db = dbConn.WebScrapperDB
    # collection = db.WebScrapper

    # reviewCUrsor = collection.find({"Product":searchString}) 
    # reviews = []
    # for doc in reviewCUrsor:
    #     reviews.append(doc) 
    reviews = []
    reviews = DBHelper.Search(searchString)
    if len(reviews) > 0: 
        return render_template('results.html',reviews=reviews) 
    else:
        flipkart_url = "https://www.flipkart.com/search?q=" + searchString
        uClient = uReq(flipkart_url) 
        flipkartPage = uClient.read() 
        uClient.close() 
        flipkart_html = bs(flipkartPage, "html.parser")
        bigbox = flipkart_html.find_all('div', {'class':"_1AtVbE col-12-12"}) 
       
        box = bigbox[3]
        
        productLink = "https://www.flipkart.com" + box.div.div.div.a['href'] 
        prodRes = requests.get(productLink) 
        prod_html = bs(prodRes.text, "html.parser")
        commentboxes = prod_html.find_all('div', {'class':"col _2wzgFH"}) 
         
        for commentbox in commentboxes:
            try:              
                custName = commentbox.find_all('p', {'class':"_2sc7ZR _2V5EHH"})[0].text
            except:
                custName = 'No Customer Name' 
            try:
                rating = commentbox.find_all('div', {'class':"_3LWZlK _1BLPMq"})[0].text
                
            except:
                rating = 'No Rating'
            try:
                commentHead = commentbox.find_all('p', {'class':"_2-N8zT"})[0].text
            except:
                commentHead = 'No Comment Heading'
            try:
              
                custComment = commentbox.find_all('div', {'class':"t-ZTKy"})[0].div.div.text
            except:
                custComment = 'No Customer Comment'   
        
            mydict = {"Product": searchString, "Name": custName, "Rating": rating, "CommentHead": commentHead,  "Comment": custComment} 
            
            DBHelper.insert(mydict)
        reviews = DBHelper.Search(searchString)
        return render_template('results.html', reviews=reviews) 