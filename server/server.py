# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 16:57:29 2020

@author: ademo
"""
from flask import Flask, request, jsonify
#from flask_cors import CORS, cross_origin
import util

app = Flask(__name__)

#CORS(app, support_credentials=True )

#import util

@app.route('/image_classifier', methods = ['GET', 'POST'])
#@cross_origin(support_credentials=True)

def image_classifier():
    image_data = request.form['image_data']
    
    response = jsonify(util.image_classifier(image_data))
    
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response




if __name__ == "__main__":
    print("starting python flask server for sports celebrity image classification") 
    util.load_artifacts()
    app.run(port=5000)
    #app.run(host='0.0.0.0', port=8000, debug=True)