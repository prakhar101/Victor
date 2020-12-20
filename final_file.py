import subprocess
import os  # again for running the os level commands
import pyttsx3  # for converting text to speech
import speech_recognition as sr  # for converting speech to text
import datetime  # for knowing the current time
import smtplib  # for sending the email we have to use the smtp server therefore I have import this
import shutil  # for moving and handling file and folder
from selenium import webdriver  # for using web application
import time  # for function like sleep
# for doing whatsapp(online message service of twilio)
from twilio.rest import Client
import random  # for getting the random integer using randint function
import cv2  # for capturing the image
import re  # for muli-deliminator splitting of  the string

#  assigning folders name
folders = {
    'videos': ['.mp4'],
    'audios': ['.wav', '.mp3'],
    'images': ['.jpg', '.png'],
    'documnets': ['.doc', '.xlsx', '.xls', '.pdf', ".zip", ".rar"],
    "software": ['.exe']
}
password="112233"# for authorisation for critical service
engine = pyttsx3.init()  # intializing the engine
# providing a voice to the engine from which It will speak
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
# sampling frequency rate .for converting the analog signal to digital signal
sample_rate = 20000
chunk_size = 2048  # it is a buffer..It stores 2048 samples (bytes of data)


# this function is used for converting the text to audio
def speak(audio):
    engine.say(audio)
    engine.runAndWait()


# This function will send the whatsapp message for us

def send_whatsapp_message():  # This fucntion will will help for sending message to the whatsapp
    speak("Enter security code ")
    x=input("Enter security code : ")
    if x != password:
        speak("authorisation failed")
        return
    account_sid = 'AC841f5e64e2565f344382078fb766dc04'  # it is authentication id
    auth_token = '7784117add108187069b0c70c6393d47'  # it is token number

    # here the we are doing authentication for using the twilio service
    client = Client(account_sid, auth_token)
    from_whatsapp_number = 'whatsapp:+14155238886'
    # replace this number with your own WhatsApp Messaging number
    speak("Enter the number")
    number = input("Enetr the number-:")
    if "+91" not in number:
        number = "+91" + number
    to_whatsapp_number = 'whatsapp:{}'.format(number)
    choice = takeCommand(
        "do you wan to send the message by speaking or typing")
    if "speak" in choice or "speaking" in choice or "saying" in choice:
        message = takeCommand("Speak the message you want to send")
    else:
        speak("Type the message you what to send")
        message = input("Type your message-:")

    client.messages.create(
        body=message, from_=from_whatsapp_number, to=to_whatsapp_number)
    speak("message sent succesfully")


def calculator():  # for doing voice based calculation
    input = takeCommand("tell me the expression")
    x = []
    # multi-deliminator splitting of the mathematical expression
    x = re.split(' \+| \-| \/| \*|  |x ', input)
    print(x)
    c = 0
    try:
        for i in input:
            if len(x) == 1:
                print(c)
                speak(input + "is euual to {}".format(c))
                return
            if i == '+':
                a = int(x.pop(0))
                b = int(x.pop(0))
                c = a + b
                x.insert(0, c)
            elif i == '-':
                a = int(x.pop(0))
                b = int(x.pop(0))
                c = a - b
                x.insert(0, c)
            elif i == '*' or i == 'x':
                a = int(x.pop(0))
                b = int(x.pop(0))
                c = a * b
                x.insert(0, c)
            elif i == '/':
                a = int(x.pop(0))
                b = int(x.pop(0))
                c = a / b
                x.insert(0, c)
    except Exception:  # exception handling in case of wrong input given by user
        speak("can't evalute expression")


# this function take a image show and save
def take_image():
    cam = cv2.VideoCapture(0)  # to start local web cam
    if not cam.isOpened():
        speak("camera can't be opened")
        return
    while True:
        ret, image = cam.read()
        cv2.imshow("preview", image)
        if cv2.waitKey(5000):
            break
    cv2.imshow("image", image)  # to show image
    speak("type file name")
    file_name = input("type file name hear :-")
    cv2.imwrite(os.path.join("E:\image", file_name), image)  # to save image
    cam.release()
    cv2.destroyAllWindows()
    speak("image captured")
    print("saved at {}".format(os.path.join("E:\image", file_name)))


# this function tell current time
def tell_time():
    time = datetime.datetime.now()
    date = time.date()
    hour = time.hour
    min = time.minute
    if hour < 12:
        if hour == 0:
            hour = 12
        speak("today is {} and it is  {} {} AM".format(date, hour, min))
    else:
        if hour != '12':
            hour = hour - 12
        speak("today is {} and it is  {} {} PM".format(date, hour, min))


# This function greet the user according to time
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if (hour >= 0) and (hour < 12):
        speak("Good Morning! Sir")
    elif (hour >= 12) and (hour < 18):
        speak("Good Afternoon! Sir")
    else:
        speak("Good Evening! Sir")
    speak("I am Victor your virtual assistant . Please tell me how may I help you")


# this function converts voice to text
def takeCommand(instruction="Listening for your next instruction"):
    # initializing the recognizer..It will recognize the human audio
    r = sr.Recognizer()
    time.sleep(0.1)
    with sr.Microphone(device_index=1, sample_rate=sample_rate, chunk_size=chunk_size) as source:
        # wait for 0.2 second to let the recognizer adjust the
        # energy threshold based on the surrounding noise level
        r.adjust_for_ambient_noise(source, duration=0.1)
        # calling speak function to tell the user to say instruction
        if "Again Listening" not in instruction:
            speak(instruction)
        time.sleep(0.10)
        # it will record/capture out audio
        audio = r.listen(source)
    try:
        # it is a google api
        # it will send the captured audio and send to google
        # in will return text as output
        text = r.recognize_google(audio)
        # this convert the string haing all charcters lower case
        text = text.lower()
        # to print the instruction given by user
        print(text)
        return text
    except Exception:
        # some exception handling to handle the situation if we got exception while converitng audio to speech
        print("Unable to recognize you voice")
        return "none"


# this function send e-mail


def sendEmail():
    speak("Enter security code ")
    x=input("Enter security code : ")
    if x != password:
        speak("authorisation failed")
        return
    # connecting to the server of gmail
    # creating a session with smtp server of google
    server = smtplib.SMTP('smtp.gmail.com', 587)
    # first parameter is adress/loaction  of google's smtp server and second it port number ..for google we use port number 22
    server.starttls()
    # For security reasons,  putting the SMTP connection in the TLS mode. TLS (Transport Layer Security) encrypts all the SMTP commands
    # our e-mail id and password
    server.login('rkt574154@gmail.com', 'ydgxsufkukluayef')
    # email id of receiver
    speak("Type the receiver email id")
    receiver = input("Enter the email-id of the receiver-:")
    # to take choice from user that he want to speak or type the message
    choice = takeCommand(
        "Do you want to send the message by speaking or do you want to type")
    if ("speak" in choice) or ("speaking" in choice) or ("saying" in choice):
        subject = takeCommand("Speak the sunject of the email")
        content = takeCommand(
            "Speak  the message you want to send to the sender")
    else:
        speak("Enter the subject of the email")
        subject = input("Enter the subject of the email-:")
        speak("Type the message")
        content = input("Enter message : ")
    server.sendmail("rkt574154@gmail.com", receiver,
                    "Subject :{} \n\n {}".format(subject, content))  # sending the message
    server.close()  # closing the connection
    speak("email sent successfully")


# this function create a txt file
def create_file_in_particular_dirctory():
    # to take path of location where we want to make file
    speak("Please type  the path of the directory inside which you want to create a file")
    path = input("Enter the path here-:")
    if path[len(path) - 1] != "\\":
        path = path + "\\"
    # to take name of the file
    speak("Enter the name of the file")
    name = input("Enter the name of the file-:")
    file = open(path + name, "w+")
    file.close()
    speak("empty file created successfully")
    return path + name


# this function create a txt file and write content in it
def create_file_and_also_write_in_that_file():
    # calling create_file_in_particular_dirctory() function to creake a txt file
    path = create_file_in_particular_dirctory()
    # opening file to write content in file
    file = open(path, "w+")
    # to take choice from user that he want to speak or type the message
    choice = takeCommand(
        "Do you want to speak or do you want to type content in file")
    if ("speak" in choice) or ("speaking" in choice) or ("saying" in choice):
        content = takeCommand("Just Speak what you want to write in the file")
    else:
        speak("Type the content")
        content = input("Type the content : ")
    file.writelines(content)
    file.close()
    speak("content in the file written succesfully!!")


# this function open chrome to search something
def search_for_something_in_chrome():
    # to take input what user want to search
    x = takeCommand(
        "What you want to search like to search like today weather or something")
    print(x)
    query = ""
    for i in range(0, len(x)):
        if x[i] == " ":
            query = query + "+"
        else:
            query = query + x[i]
    print(query)
    # url for searching something in the chrome..
    os.system("start chrome https://www.google.com/search?q={}".format(query))


# this function open a txt file in notepad
def open_a_file():
    # to take path of file that user want to open
    speak("Enter the absolute path of the file")
    path = input("Enter the path here-:")
    os.system("start notepad {}".format(path))
    global app_list
    app_list.append("notepad")


# this function reply to user by speaking
def reply():
    speak("Hi Sir! I am fine Hope you are good in this pandemic situation")


# this function kill the application running in computer
def close_application():
    global app_list
    app = takeCommand("Which Appliaction do you want to close")
    # if "chrome" in app:
    #     app = "chrome"
    if "notepad" in app:
        app = "notepad"
    elif "media player" in app:
        app = "wmplayer"
    elif "vlc" in app:
        app = "vlc"
    elif "music" in app or "song" in app or "songs" in app:
        app="Music.UI"
    subprocess.getoutput("taskkill /IM {}.exe /f".format(app))
    # removing that particular appliaction from the list....
    if app in app_list:
        app_list.remove(app)
        speak("{} killed".format(app))
    else:
        speak("No such pocess is running")


# this function change the name of folder or file
def rename_folder(directry):
    for folder in os.listdir(directry):
        if os.path.isdir(os.path.join(directry, folder)):
            os.rename(os.path.join(directry, folder),
                      os.path.join(directry, folder.lower()))


# this function move the file in directry to its specific subfolder


def create_move(ext, file_name, directry, other_name):
    # find=false is flag to check that file that is to arrange is associated to subfolders or not
    find = False
    for folder_name in folders:
        # to check extension of the file in order to place it in subfolder
        if "." + ext in folders[folder_name]:
            if folder_name not in os.listdir(directry):
                os.mkdir(os.path.join(directry, folder_name))
            # moving the file from directry to subfolder
            shutil.move(os.path.join(directry, file_name),
                        os.path.join(directry, folder_name))
            # flag true the file belong to subfolder
            find = True
            break
    # if file is not associated with any subfolder
    if not find:
        if other_name not in os.listdir(directry):
            os.mkdir(os.path.join(directry, other_name))
        # moving the file from directry to other folder
        shutil.move(os.path.join(directry, file_name),
                    os.path.join(directry, other_name))


# this function arrange all the file of directory in subfolder


def sort_files():
    # to take the path of directry that we want to arrange
    speak("Please enter the name of the directory whose files you want to sort")
    directry = input("enter path of directory:")
    # to make a folder to transfer the file that not fit to the subfolder we created
    speak('Enter the name of the folder in which you want your want your unknown files should be put ')
    other_name = input("Enter the Folder name for unknown files:")
    # rename the all directory to the lower case in order to handle multiple folder of same name
    rename_folder(directry)
    all_files = os.listdir(directry)
    length = len(all_files)
    count = 1
    # processing all files in directry
    for i in all_files:
        # to check weather the element is is a file or not
        if os.path.isfile(os.path.join(directry, i)):
            # calling create_move() function to arrange the file in subfolder
            create_move(i.split(".")[-1], i, directry, other_name)
        print("total files:{}|Done: {} | left: {}".format(
            length, count, length - count))
        count += 1


def play_song():
    music_directory = "C:\\Users\\prakh\\Music"  # Default music directory
    choice = takeCommand(
        "Do you want to make the use of your default song directory")
    if "no" in choice or ("new" in input_from_user and "directory" in input_from_user):
        speak("Enter the new directory path ")
        music_directory = input("Enter the new directory path-:")
    songs = os.listdir(music_directory)
    n = random.randint(0, len(songs)-1)
    if(songs[n]=='desktop.ini'):
        if n!=0 :
            n=0
        else :
            speak("There is no music in the directory")
            return 
    os.startfile(os.path.join(music_directory, songs[n]))
    global app_list
    app_list.append("Music.UI")


# this function login to facebook
def login_to_facebook():
    # taking detail of facebook id
    speak("Enter your registered mobile number ")
    mobile = input("enter mobile no : ")
    speak("Enter your password")
    passwd = input("enter password : ")
    driver = webdriver.Chrome()
    # filling the information in facebook
    driver.get("https://facebook.com")
    driver.maximize_window()
    # time.sleep(2)
    search_box = driver.find_element_by_xpath('//*[@id="email"]')
    search_box.send_keys(mobile)
    password = driver.find_element_by_xpath('//*[@id="pass"]')
    password.send_keys(passwd)
    enter_button = driver.find_element_by_xpath('//*[@id="u_0_b"]')
    enter_button.click()
    speak("welcome to facebook")


# this function search and play what we serch on youtube
def start_youtube():
    # asking user that what he want to search on youtube
    choice = takeCommand("what do you want to search on youtube : ")
    print(choice)
    # searching and playing the video on youtube
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get("https://youtube.com")
    searchb = driver.find_element_by_xpath(
        '/html/body/ytd-app/div/div/ytd-masthead/div[3]/div[2]/ytd-searchbox/form/div/div[1]/input')
    searchb.send_keys(choice)
    enter_but = driver.find_element_by_xpath('//*[@id="search-icon-legacy"]')
    enter_but.click()
    play = driver.find_element_by_xpath('//*[@id="video-title"]')
    play.click()
    app_list.append("chrome")


app_list = list()
# main function
if __name__ == "__main__":
    wishMe()
    message = "Listening"
    while True:
        # taking instruction from user
        input_from_user = takeCommand(message)
        if input_from_user == "none":
            print("Again Listening")
            message = ""
            continue
        message = "Listening"

        # local application part
        if ("launch" in input_from_user) or ("go to" in input_from_user) or ("start" in input_from_user) or ("get back" in input_from_user) or ("take me" in input_from_user) or ("open" in input_from_user and "file" not in input_from_user):
            if "chrome" in input_from_user:
                cmd = "chrome"
            elif "notepad" in input_from_user:
                cmd = "notepad"
            elif "media player" in input_from_user:
                cmd = "wmplayer"
            elif ("vlc" in input_from_user) or ("videoplayer" in input_from_user):
                cmd = "vlc"
            else:
                speak("Sorry I Unable to understand  Can you please speak again")
                continue

            if cmd in app_list:
                if cmd == "wmplayer":
                    cmd = "media player"
                st = "automate.bat \"{}\"".format(cmd)
                os.system(st)
                continue
            app_list.append(cmd)
            os.system("start {}".format(cmd))

        # create txt file
        elif ("create" in input_from_user) and ("file" in input_from_user):
            if "write" in input_from_user:
                create_file_and_also_write_in_that_file()
                continue
            else:
                create_file_in_particular_dirctory()
                continue

        # searching on google
        elif ("search" in input_from_user) or ("tell me about" in input_from_user):
            app_list.append("chrome")
            search_for_something_in_chrome()
            continue

        # file opening
        elif ("open" in input_from_user) and ("file" in input_from_user):
            open_a_file()
            continue

        # send mail
        elif ("send" in input_from_user) and ("email" in input_from_user):
            sendEmail()
            continue

        # asking the victor
        elif ("listening" in input_from_user or "listening" in input_from_user) and (("me" in input_from_user) or ("us" in input_from_user)):
            speak("I am listening to you sir waititng for your next instruction.")
            continue
        elif ((("hi" in input_from_user) or ("hello" in input_from_user)) and ("victor" in input_from_user)) or (
                "how are you" in input_from_user):
            reply()
            continue
        elif "good morning" in input_from_user or "good evening" in input_from_user or "good afternoon" in input_from_user:
            wishMe()
            continue
        elif ("what is time" in input_from_user) or ("tell me time" in input_from_user):
            tell_time()
            continue

        # closing local application or victor
        elif ("close" in input_from_user) or ("exit" in input_from_user) or ("shut down" in input_from_user) or ("shut" in input_from_user) or ("stop" in input_from_user) or ("terminate" in input_from_user) or ("exit" in input_from_user):
            if ("application" not in input_from_user) and ("app" not in input_from_user):
                speak("Okay! I am shutting down sir Have a nice day")
                exit()
            else:
                close_application()
                continue

        # send whatsapp
        elif ("send" in input_from_user) and (("message" in input_from_user) or ("whatsapp" in input_from_user)):
            send_whatsapp_message()
            continue

        # take image
        elif ("take" in input_from_user) and (("image" in input_from_user) or ("photo" in input_from_user) or "picture" in input_from_user or "snapshot" in input_from_user):
            take_image()
            continue

        # sort file in a directry
        elif (("sort" in input_from_user) or ("arrange" in input_from_user) or ("short" in input_from_user)) and (("file" in input_from_user) or ("files" in input_from_user) or ("content" in input_from_user) or ("element" in input_from_user) or ("contents" in input_from_user)):
            sort_files()
            continue

        # login to facebook
        elif ("login" in input_from_user) and ("facebook" in input_from_user):
            login_to_facebook()
            continue

        # play video on youtube
        elif ("play" in input_from_user) and ("youtube" in input_from_user):
            start_youtube()
            continue
        # play song for me
        elif "play" in input_from_user and ("song" in input_from_user or "songs" in input_from_user or "music" in input_from_user or "musics" in input_from_user):
            play_song()
            continue
        # do some calculations
        elif "calculator" in input_from_user or "calculation" in input_from_user or "calculations" in input_from_user:
            calculator()
            continue

        else:
            speak("sorry I am unable to perfom this task")
