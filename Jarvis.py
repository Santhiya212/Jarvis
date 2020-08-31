import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia #pip install wikipedia
import webbrowser
import os
import smtplib
from datetime import date
import calendar
import sqlite3
from sqlite3 import Error
# importing requests and json
import requests, json
import tkinter
import sys
from tkinter import * 
from tkinter.ttk import *
from pyttsx3.drivers import *
from pyttsx3 import *
import pyttsx3.drivers.sapi5

def stop():
    sys.exit()

window = tkinter.Tk()
MyTitle = tkinter.Label(window, text="Jarvis",font="Helvetica 16 bold")
MyTitle.pack()

p1 = PhotoImage(file = 'images.ico') 
  
# Setting icon of master window 
window.iconphoto(False, p1) 

MyButton = tkinter.Button(window, text="Stop", command=stop)
MyButton.pack()

progress = tkinter.Label(window, font="Helvetica 16 bold")
progress.pack()

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file+".db")
        cur = conn.cursor() # instantiate a cursor obj
        customers_sql = """
        CREATE TABLE IF NOT EXISTS JarvisAI (
             questions text,
             answers text)"""
        cur.execute(customers_sql)
        conn.commit()
        cursor = conn.execute("SELECT * from JarvisAI")
        rows = cursor.fetchall()
        #print(rows.__str__())
        if(len(rows) == 0):
            print("Inserting data")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('how are you','I am Good')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('creator','My creator is Santhiya. She is one of the great programmers. Who designed me')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('sad','I am sorry to hear that. If i would say, Nothing is permanent in this world. Life moves on ')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('alone','Thats so sad. You can always call upon your friends')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('dont understand','I am sorry. If you can please reiterate the command, I will try to understand')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('happy','Thats great. I wish you are always like that')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('good','Thank you. I am always grateful')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('thank you','That is my duty. My pleasure')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('be my friend','I am always with you and I will do my best to help you')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('depressed','I am sorry to hear that. My creator says there is always a way. keep going')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('tell me a joke','I am not yet featured to make you laugh.')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('master','My master is you. I am always ready to serve you')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('family','You are my family. Father and mother. i always love my family')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('father','You are my father')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('mother','you are my mother')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('my mother','I am eager to know about your mother')")
            conn.execute("INSERT INTO JarvisAI (questions, answers) VALUES ('my father','I am eager to know about your Father')")
            conn.commit()

    except Error as e:
        print(e)

    return conn

engine = pyttsx3.init('sapi5')
voices= engine.getProperty('voices') #getting details of current voice
engine.setProperty('voice', voices[0].id)

def speak(audio):
    engine.say(audio) 
    engine.runAndWait()
    #pass     #For now, we will write the conditions later.

def wishMe(name):
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Morning!")

    elif hour>=12 and hour<18:
        speak("Good Afternoon!")   

    else:
        speak("Good Evening!")  

    speak("Hello "+name+", I am Jarvis. Please tell me how may I help you")


def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        progress.configure(text="Listening..." )
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        progress.configure(text="Recognizing..." )
        print("Recognizing...")    
        query = r.recognize_google(audio, language='en-in')
        progress.configure(text=f"User said: {query}\n" )
        print(f"User said: {query}\n")

    except Exception as e:
        # print(e)    
        progress.configure(text="Say that again please..." )
        print("Say that again please...")  
        return "None"
    return query

def weatherReport():
    BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
    CITY = "Delhi"
    API_KEY = "ae480f2ff048ad85bbee554eb986c978"
    LAT="27.2038"
    LON="77.5011"
    URL = "https://api.openweathermap.org/data/2.5/onecall?lat="+LAT+"&lon="+LON+"&exclude=hourly,daily&appid=" + API_KEY
    # HTTP request
    response = requests.get(URL)
    # checking the status code of the request
    if response.status_code == 200:
        data = response.json()
        main = data['main']
        temperature = main['temp']
        humidity = main['humidity']
        pressure = main['pressure']
        report = data['weather']
        speak("Sir, Right now in "+CITY+", Temperature is "+temperature+"Humidity "+humidity+"Overall it is "+report)
    else: 
        speak(" City Not Found ")


HEAR = True

name = "Sir"
wishMe(name)

def listen():
    
    conn = create_connection("Jarvis_DB")
    questions = conn.execute("SELECT questions from JarvisAI")
    rows=questions.fetchall()
    #print(rows.__str__())

    while HEAR==True:
    # if 1:
        query = takeCommand().lower()
        
        for row in rows:
            if row[0] in query:
                answer = conn.execute("SELECT answers from JarvisAI where questions = ?",(row[0],) )
                ans = answer.fetchall()
                print(ans[0][0])
                speak("Sir,"+ans[0][0])

        # Logic for executing tasks based on query
        if 'search for' in query:
            speak('Searching Wikipedia...')
            query = query.replace("search for", "")
            results = wikipedia.summary(query, sentences=2)
            speak(name+", According to Wikipedia")
            print(results)
            speak(results)

        elif 'open youtube' in query:
            speak(name+", Opening youtube")
            webbrowser.open("youtube.com")

        elif 'open google' in query:
            speak(name+", Opening Google")
            webbrowser.open("google.com")

        elif 'open stackoverflow' in query:
            webbrowser.open("stackoverflow.com")   


        elif 'play music' in query:
            webbrowser.open("music.amazon.in")

        elif 'the time' in query:
            strTime = datetime.datetime.now().strftime("%H:%M:%S")    
            speak(name+", the time is "+strTime)

        elif 'day' in query:
            my_date = date.today()
            strday = calendar.day_name[my_date.weekday()]
            speak(name+", today is "+strday)

        elif 'bored' in query:
            speak(name+", Here are some recommendations")
            speak("Call a friend, play Ludo, watch youtube, watch Netflix")

        elif 'weather' in query:
            #weatherReport()
            speak("Sorry Sir, I could not provide you the data now. In my next release, my creator will add that feature to me")


MyButton = tkinter.Button(window, text="Start Listening", command=listen)
MyButton.pack()
  

window.mainloop()
        
        
    