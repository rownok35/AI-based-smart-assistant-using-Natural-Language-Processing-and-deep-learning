import pymongo
from pymongo import MongoClient
import streamlit as st
import nltk
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

import numpy
import tflearn
import tensorflow
import random
import json
import pickle
import pyaudio
import speech_recognition as sr
from PIL import Image

from datetime import datetime
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

cluster= MongoClient("mongodb+srv://chatbot:a4s@cluster0.rqhb3.mongodb.net/query?retryWrites=true&w=majority")
db=cluster["query"]
collection=db["query"]


# initialize the recognizer
r = sr.Recognizer()

import base64
@st.cache(allow_output_mutation=True)
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    
    st.markdown(page_bg_img, unsafe_allow_html=True)
    return

# set_png_as_page_bg('.jpg')


st.title("Welcome to AI Based Chatbot")
st.subheader("A Thesis Project Under The Supervision of Col Siddharth Malik, SM")

inp="hello"
with open("intents.json", encoding='UTF-8') as file:
	data = json.load(file)

with open("data.pickle", "rb") as f:
		words, labels, training, output = pickle.load(f)

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)


model.load("model.tflearn")


def bag_of_words(s, words):
	bag = [0 for _ in range(len(words))]

	s_words = nltk.word_tokenize(s)
	s_words = [stemmer.stem(word.lower()) for word in s_words]

	for se in s_words:
		for i, w in enumerate(words):
			if w == se:
				bag[i] = 1
			
	return numpy.array(bag)


	
	

string = st.text_input("chat here")
if st.button("submit"):
	inp=string

st.write("For Audio Input click below")

if st.button('English'):
	with sr.Microphone() as source:
	# read the audio data from the default microphone
		st.write("speak")
		audio_data = r.record(source, duration=8)
		st.write("Recognizing...")
		# convert speech to text
		# text = r.recognize_google(audio_data, language="bn-BD") #using bangla
		text = r.recognize_google(audio_data)
		st.warning(text)
		inp=text

if st.button('Bangla'):
	with sr.Microphone() as source:
	# read the audio data from the default microphone
		st.write("speak")
		audio_data = r.record(source, duration=8)
		st.write("Recognizing...")
		# convert speech to text
		text = r.recognize_google(audio_data, language="bn-BD") #using bangla
		# text = r.recognize_google(audio_data)
		st.warning(text)
		inp=text


# if inp.lower() == "quit":
# 	break
# st.write(type(inp))
results = model.predict([bag_of_words(inp, words)])[0]
results_index = numpy.argmax(results)
tag = labels[results_index]

if results[results_index] > 0.5:

    for tg in data["intents"]:

        if tg['tag'] == tag:
            responses = tg['responses']

    st.write("Bot: ")
    result = random.choice(responses)
    st.success(result)
else:
    st.write("Bot: ")
    st.error("i didn't get it. Ask another question")
    collection.insert_one({"_id": dt_string, "query": inp})


st.sidebar.markdown("<h1 style='text-align: center; color: black;'>Developed By</h1>", unsafe_allow_html=True)
# st.sidebar.title("Developed By")
st.sidebar.subheader("1.Rezwan Rownok")


img=Image.open("rownok.jpg")
st.sidebar.image(img,width=300,caption="Rezwan Rownok")
st.sidebar.write("Email: rownokrezwan@gmail.com")
st.sidebar.write("linkedin: https://www.linkedin.com/in/rezwan-rownok-538978198")

st.sidebar.subheader("2.Shahriar Rahman Khan")
img=Image.open("shahriar.jpg")
st.sidebar.image(img,width=300,caption="Shahriar Rahman")
st.sidebar.write("Email: shahriarkhan.ndc@gmail.com")
st.sidebar.write("linkedin: https://www.linkedin.com/in/shahriar-rahman-khan-nehal-322351152")

st.sidebar.subheader("3.Samiha Raisa Zaman")
img=Image.open("sam.jpg")
st.sidebar.image(img,width=300,caption="Samiha Raisa")
st.sidebar.write("Email: samiharaisa031@gmail.com")
st.sidebar.write("linkedin: https://www.linkedin.com/in/samiha-raisa-zaman-0b472512b")

st.sidebar.subheader("4.Sharmila Rahman Prithula")
img=Image.open("prithula.jpg")
st.sidebar.image(img,width=300,caption="Sharmila Rahman")
st.sidebar.write("Email: sharmilarahmanprithula@gmail.com")
st.sidebar.write("linkedin: ")


