import datetime  # to get dateandtime
import os
import webbrowser
import openai
import pyttsx3  # to get the machine to speak
import speech_recognition as sr  # to get whatever user is speaking
import wikipedia
from config import apikey
import pyautogui

def notes(prompt):
    speak("Taking notes please start speaking:")
    notetaken = takeCommand()
    print(notetaken)
    if not os.path.exists("Notes"):
        os.mkdir("Notes")
    if notetaken is not None:
        speak("Please give a title for the notes.")
        title = takeCommand()
        with open(f"Notes/{''.join(title).strip()}.txt", "w") as f:
            f.write(notetaken)
            speak("Your query has been answered the response is available on your system now.")
    else:
        speak("Please tell me what to note")
def searchweb(query):
    results = wikipedia.summary(query, sentences=3)
    return results

chatStr = ""
def chat(query):
    global chatStr
    openai.api_key = apikey
    chatStr += f"User: {query}\nAssistant: "
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=chatStr,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    try:
        speak(response["choices"][0]["text"])
        chatStr += f"{response['choices'][0]['text']}\n"
        return response["choices"][0]["text"]
    except Exception as e:
       speak("I am sorry your I couldn't quite understand your prompt. Could you reframe it for me?")
def ai(prompt): #add ai
    openai.api_key = apikey
    text = f"OpenAI response for prompt: {prompt}\n ________________________________________ \n\n"
    response = openai.Completion.create(
        model="gpt-3.5-turbo-instruct",
        prompt=prompt,
        temperature=1,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    try:
        text += response["choices"][0]["text"]
        if not os.path.exists("Responses"):
            os.mkdir("Responses")
        with open(f"Responses/{''.join(prompt.split('intelligence')[1:]).strip() }.txt", "w") as f:
            f.write(text)
        speak("Your query has been answered the response is available on your system now.")
    except Exception as e:
       speak("I am sorry your I couldn't quite understand your prompt. Could you reframe it for me?")
    return "None"  # returning none string

eng = pyttsx3.init('sapi5')  # speech api
voices = eng.getProperty('voices')
#print(voices) #incase you want to find what voices are available on your system.
eng.setProperty('voice', voices[0].id)  # set to a particular voice available on desktop

# Add more by exporting from the registry and changing to \WOW6432Node
def speak(audio):
    eng.say(audio)  # say whatever is passed
    eng.runAndWait()  # start speech and wait till the speech is done

#the speak feature can also be implemented using os and win32com.client of gtts
def takeCommand():
    # take commands from user and returns output
    r = sr.Recognizer()  # will recognize when spoken to
    with sr.Microphone() as source:  # use microphone to get voice
        #r.pause_threshold = 1  # seconds of non-speaking duration before phase is complete
        audio = r.listen(source)
        try:
            print("Recognizing........")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}\n")
            return query
        except Exception as e:
            #print("Recognition Error:", e)
            speak("I didn't quite catch that. Can you say that again please?")

def wishMe():
    # wish acc to machine time 24 hour clock
    hour = int(datetime.datetime.now().hour)  # get current time

    if hour >= 0 and hour < 12:
        speak("Hello. Good Morning!")
    elif hour >= 12 and hour < 18:
        speak("Hello. Good Afternoon!")
    else:
        speak("Hello. Good Evening!")
    speak("I am your assistant. How may I help you?")

def main_loop():
    global chatStr
    while True:
        print("Listening...")
        query = takeCommand()
        if query is not None:

            sites = [["youtube", "https://www.youtube.com/"], ["google", "https://www.google.co.in/"],
                     ["wikipedia", "https://www.wikipedia.com/"]]  # todo: add whatever sites required
            for site in sites:
                if f"open {site[0]}".lower() in query.lower():  # can be done for any website
                    speak(f"Opening {site[0]}....")
                    webbrowser.open(site[1])
                    return

            apps = [["command prompt",
                     "C:\\Users\\Dell\\AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\System Tools\\Command Prompt.lnk"],
                    ["pycharm", "C:\\Program Files\\JetBrains\\PyCharm Community Edition 2023.2.3\\bin\\pycharm64.exe"],
                    ["edge",
                     "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"]]  # todo: add whatever apps required
            for app in apps:
                if f"open {app[0]}".lower() in query:  # can be done for any App
                    speak(f"Opening {app[0]}....")
                    os.startfile(app[1])
                    return

            if 'the time' in query.lower():
                strfTime = datetime.datetime.now().strftime("%H:%M:%S")  # string format hours mins secs
                print(strfTime)
                speak(f"The time is {strfTime}")

            elif "reset chat".lower() in query.lower():
                chatStr = ""

            elif "Quit".lower() in query.lower():
                exit()

            elif 'Using Artificial Intelligence'.lower() in query.lower():
                ai(prompt=query)

            elif 'search now'.lower() in query.lower():
                query = query.replace("search now", "")
                speak(f"Searching for {query}....")
                results = searchweb(query)
                speak("According to wikipedia")
                print(results)
                speak(results)

            elif 'take notes'.lower() in query.lower():
                notes(prompt=query)

            elif 'open app'.lower() in query.lower(): #another way to open apps
                query = query.replace("open app", "")
                pyautogui.press("super")
                pyautogui.typewrite(query)
                pyautogui.sleep(2)
                pyautogui.press("enter")

            else:
                print("Chatting:\n")
                chat(query)

if __name__ == "__main__":
    print("Hello. Welcome.")
    wishMe()
    while True:
        main_loop()
