# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 17:07:25 2020

@author: ademo

"""
import joblib
import json
import numpy as np
import base64
import cv2
from wavelet import w2d

__class_num_to_names = {}
__class_names_to_num = {}

__model = None

def image_classifier(image_base64_data, file_path=None):
    imgs = get_cropped_image_if_2_eyes(file_path, image_base64_data)
    result = []
    for img in imgs:
        scaled_raw_img = cv2.resize(img, (32,32)) 
        img_har = w2d(img, 'db1', 5)
        scaled_har_img = cv2.resize(img_har, (32,32)) 
        stacked_image = np.vstack((scaled_raw_img.reshape(32*32*3,1), scaled_har_img.reshape(32*32,1)))
        image_array_length = (32 * 32 *3) + (32 *32)
        final_array = stacked_image.reshape(1,image_array_length).astype(float)
        
       # result.append( class_num_to_names(__model.predict(final_array)[0]))
        result.append({
            'Celeb' : class_num_to_names(__model.predict(final_array)[0]),
            'confidence_level': np.round(__model.predict_proba(final_array)*100,2).tolist()[0],
            'class_dictionary' : __class_names_to_num
        })
        
        
        
        
    return result
        
        
        
def load_artifacts():
    print("loading saved artifacts....")
    global __class_num_to_names
    global __class_names_to_num
    
    
    with open("./server/artifacts/class_dictionary.json", "r") as f:
        __class_names_to_num = json.load(f)
        __class_num_to_names = {num:name for name, num in __class_names_to_num.items()}
    
    global __model
    if __model is None:
        with open('./server/artifacts/trained_model.pkl', 'rb') as f:
            __model = joblib.load(f)
    print("loading saved artifacts...done")
    

def class_num_to_names(class_num):
    return  __class_num_to_names[class_num]
    
def get_cv2_image_from_base_64_string(base64string): #Credit stack overflow
    encoded = base64string.split(',')[1]
    
    img_arr = np.frombuffer(base64.b64decode(encoded), np.uint8)
    
    img = cv2.imdecode(img_arr, cv2.IMREAD_COLOR)
    return img
    
    
    
    
    
    
    
    
    
    
    
    
def get_cropped_image_if_2_eyes(image_path, image_base64_data):
    face_cascade = cv2.CascadeClassifier('./server/opencv/haarcascades/haarcascade_frontalface_default.xml')
    eye_cascade = cv2.CascadeClassifier('./server/opencv/haarcascades/haarcascade_eye.xml')

    if image_path:
        img = cv2.imread(image_path)
    else:
        img = get_cv2_image_from_base_64_string(image_base64_data)
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    
    cropped_faces = []
    
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]                  #roi meaning region of interest
        roi_color = img[y:y+h, x:x+w]
        eyes = eye_cascade.detectMultiScale(roi_gray)
        if len(eyes) >=2:
            cropped_faces.append(roi_color)
    return cropped_faces   

    

def get_b64_test_image_for_serena():
    with open("b64.txt") as f:
        return f.read()





if __name__ == "__main__":
    load_artifacts()
    print(image_classifier(None, "./test_images/dwayne1.jpg" ))
    print(image_classifier(None, "./test_images/serena1.jpg" ))
    print(image_classifier(None, "./test_images/messi2.jpg" ))
    
    print(image_classifier(None, "./test_images/sharapova2.jpg" ))
    print(image_classifier(None, "./test_images/zlatan4.jpg" ))
    #print(class_num_to_names(0))
    
