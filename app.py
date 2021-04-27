import flask
from flask import Flask, request
import face_recognition
import urllib.request
import json
import os
from dotenv import dotenv_values
from supabase_py import create_client, Client


config = dotenv_values(".env")

url = config['SUPABASE_URL']
key = config["SUPABASE_KEY"]
supabase: Client = create_client(url, key)




app = Flask(__name__)
app.config["DEBUG"] = True

def faceLoop(array):
  baseImg = array[0]['img']
  baseImg = urllib.request.urlopen(baseImg)
  baseEncode = face_recognition.load_image_file(baseImg)
  if(len(face_recognition.face_encodings(baseEncode)) == 0):
    return array
  baseEncode = face_recognition.face_encodings(baseEncode)[0]
  for obj in array:
    if 'img' in obj: 
      testImg = urllib.request.urlopen(obj['img'])
      imageTest = face_recognition.load_image_file(testImg)
      try:
        imageTest = face_recognition.face_encodings(imageTest)[0]
        # Compare faces
        results = face_recognition.compare_faces(
            [baseEncode], imageTest)

        if results[0]:
            obj['verified'] = 1
        else:
            obj['verified'] = 0
      except IndexError as e:
        print(e)       
  return array



@app.route('/', methods=['GET'])
def home():
  return "<h1>Image classifier.</p>"
@app.route('/classify', methods=['POST'])
def classify_image():
  data = request.json
  print(data)
  objRes = faceLoop(data)
  return json.dumps(objRes), 200

if __name__ == '__main__':
    app.run()