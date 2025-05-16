from flask import Flask, render_template, request


app = Flask(__name__, template_folder='templates')

def Recognization():
        import pyttsx3
        import speech_recognition as sr
        import wikipedia
        import webbrowser
        import smtplib
        from email.message import EmailMessage
        from geopy.geocoders import Nominatim
        from geopy import distance
        import random
        import turtle
        import pygame
        import requests
        import tkinter
        from translate import Translator
        import tkinter as tk
        import tkinter.messagebox
        from tkinter.constants import SUNKEN
        import cv2
        import numpy as np
        import face_recognition
        import os
        from datetime import datetime
        # from newsapi import NewsApiClient
        import pycountry

        engine = pyttsx3.init('sapi5')
        voices = engine.getProperty('voices')
        engine.setProperty('voice', voices[1].id)

        def speak(audio):
            engine.say(audio)
            engine.runAndWait()

        def WishMe():
            speak("hello i am eva. how may i help you ?")

        def takeCommand():
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print("listening...")
                r.pause_threshold = 0.7 
                audio = r.listen(source)
            try:
                print("recognizing...")
                query = r.recognize_google(audio, language="en-in")
                print("user said: ", query)

            except Exception:
                print("say that again please...")
                speak("say that again please...")
                return "none"
            return query

        if __name__ == '__main__':
            WishMe()
            speak("starting the verification process!!!")
            path = 'images'

            images = []
            classNames = []
            mylist = os.listdir(path)

            for cl in mylist:
                curImg = cv2.imread(f'{path}/{cl}')
                images.append(curImg)
                classNames.append(os.path.splitext(cl)[0])
            print(classNames)

            def findEncodings(images):
                encodeList = []
                for image in images:
                    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    encode = face_recognition.face_encodings(image)[0]
                    encodeList.append(encode)
                return encodeList

            def markAttendance(name):
                with open('Login History.csv', 'r+') as f:
                    myDataList = f.readlines()
                    nameList = []
                    for line in myDataList:
                        entry = line.split(',')
                        nameList.append(entry[0])
                    if name not in nameList:
                        now = datetime.now()
                        dtString = now.strftime('%H:%M:%S')
                        f.writelines(f'\n{name}, {dtString}')

            encodeListknown = findEncodings(images)
            print('Encoding complete')

            cap = cv2.VideoCapture(0)
            while True:
                success, img = cap.read()
                imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
                imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

                facesCurFrame = face_recognition.face_locations(imgS)
                encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

                for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                    matches = face_recognition.compare_faces(encodeListknown, encodeFace)
                    faceDis = face_recognition.face_distance(encodeListknown, encodeFace)
                    matchIndex = np.argmin(faceDis)

                    if matches[matchIndex]:
                        name = classNames[matchIndex].upper()
                        y1, x2, y2, x1 = faceLoc
                        y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
                        cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
                        cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)
                        markAttendance(name)

                cv2.imshow('webcam', img)
                cv2.waitKey()
                while True:
                    query = takeCommand().lower()

                    if 'wikipedia' in query:
                        speak('searching wikipedia...')
                        query = query.replace("wikipedia", "")
                        results = wikipedia.summary(query, sentences=3)
                        speak("according to wikipedia")
                        print(results)
                        speak(results)

                    elif 'open youtube' in query:
                        speak("")
                        webbrowser.open("youtube.com")

                    elif 'open google' in query:
                        speak("sure why not!!")
                        webbrowser.open("google.com")


                    elif 'open stackoverflow' in query:
                        speak("sure why not!!")
                        webbrowser.open("stackoverflow.com")

                    elif 'open outlook' in query:
                        speak("sure why not!!")
                        webbrowser.open("outlook.com")

                    elif 'open vs code' in query:
                        speak("sure why not!!")
                        codePath1 = 'C:\\Users\\Jainam\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
                        os.startfile(codePath1)

                    elif 'open microsoft word' in query:
                        speak("sure why not!!")
                        codePath2 = "C:\\Program Files\\Microsoft Office\\root\\Office16\\WINWORD.EXE"
                        os.startfile(codePath2)

                    elif 'send a mail' in query:

                        def send_email(receiver, subject, message):
                            server = smtplib.SMTP('smtp.gmail.com', 587)
                            server.starttls()
                            server.login('goswamidhruv01@gmail.com', 'dhruv0247')
                            email = EmailMessage()
                            email['From'] = 'goswamidhruv01@gmail.com'
                            email['To'] = receiver
                            email['Subject'] = subject
                            email.set_content(message)
                            server.send_message(email)

                        email_list = {
                            'JM': 'mehtajainam068@gmail.com',
                            'DM': 'Dhruvimay82@gmail.com',
                            'NI': 'gohilgnj@gmail.com',
                            'JP': 'jahnvihpandya@gmail.com'
                            # "Himani ma'am": 'himani_ce@ldrp.ac.in'
                        }

                        def get_email_info():
                            speak('To Whom you want to send email')
                            name = takeCommand()
                            receiver = email_list[name]
                            print(receiver)
                            speak('What is the subject of your email?')
                            subject = takeCommand()
                            speak('Tell me the text in your email')
                            message = takeCommand()
                            send_email(receiver, subject, message)
                            speak('Your email is sent')
                            speak('Do you want to send more email?')
                            send_more = takeCommand()
                            if 'yes' in send_more:
                                get_email_info()

                        get_email_info()

                    elif "calculate the distance" in query:

                        geolocator = Nominatim(user_agent="geoapiExercises")
                        speak('what is your current location :')
                        Input_place1 = takeCommand()
                        speak('what is your final destination:')
                        Input_place2 = takeCommand()

                        speak("calculating the distance...")
                        print('calculating the distance....')
                        place1 = geolocator.geocode(Input_place1)
                        place2 = geolocator.geocode(Input_place2)

                        Loc1_lat, Loc1_lon = place1.latitude, place1.longitude
                        Loc2_lat, Loc2_lon = place2.latitude, place2.longitude

                        location1 = (Loc1_lat, Loc1_lon)
                        location2 = (Loc2_lat, Loc2_lon)

                        result = (distance.distance(location1, location2).km, 'kilometers')
                        print(result)
                        speak(result)

                    elif "generate password" in query:

                        speak("Input the length of your password")
                        Passlength = int(input("Enter the length of the password"))
                        s = 'abcdefghijklmnopqrstuvwxyz01234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%&'
                        p = "".join(random.sample(s, Passlength))
                        speak("Generating a random password for you...")
                        print(p)

                    elif "let's play some game" in query:

                        speak("which game would you like to play")
                        speak("we have two games for you game one is snake one and game 2 is sudoku!!")
                        "snake game"
                        "sudoku game"
                        speak("select a game 1 or 2?")

                    elif "game 1" in query:

                        speak("opening snake game")
                        w = 500
                        h = 500
                        food_size = 10
                        delay = 100

                        offsets = {
                            "up": (0, 20),
                            "down": (0, -20),
                            "left": (-20, 0),
                            "right": (20, 0)
                        }

                        def reset():
                            global snake, snake_dir, food_position, pen
                            snake = [[0, 0], [0, 20], [0, 40], [0, 60], [0, 80]]
                            snake_dir = "up"
                            food_position = get_random_food_position()
                            food.goto(food_position)
                            move_snake()

                        def move_snake():
                            global snake_dir

                            new_head = snake[-1].copy()
                            new_head[0] = snake[-1][0] + offsets[snake_dir][0]
                            new_head[1] = snake[-1][1] + offsets[snake_dir][1]

                            if new_head in snake[:-1]:
                                reset()
                            else:
                                snake.append(new_head)

                                if not food_collision():
                                    snake.pop(0)

                                if snake[-1][0] > w / 2:
                                    snake[-1][0] -= w
                                elif snake[-1][0] < - w / 2:
                                    snake[-1][0] += w
                                elif snake[-1][1] > h / 2:
                                    snake[-1][1] -= h
                                elif snake[-1][1] < -h / 2:
                                    snake[-1][1] += h

                                pen.clearstamps()

                                for segment in snake:
                                    pen.goto(segment[0], segment[1])
                                    pen.stamp()

                                screen.update()

                                turtle.ontimer(move_snake, delay)

                        def food_collision():
                            global food_position
                            if get_distance(snake[-1], food_position) < 20:
                                food_position = get_random_food_position()
                                food.goto(food_position)
                                return True
                            return False

                        def get_random_food_position():
                            x = random.randint(- w / 2 + food_size, w / 2 - food_size)
                            y = random.randint(- h / 2 + food_size, h / 2 - food_size)
                            return x, y

                        def get_distance(pos1, pos2):
                            x1, y1 = pos1
                            x2, y2 = pos2
                            dist = ((y2 - y1) ** 2 + (x2 - x1) ** 2) ** 0.5
                            return dist

                        def go_up():
                            global snake_dir
                            if snake_dir != "down":
                                snake_dir = "up"

                        def go_right():
                            global snake_dir
                            if snake_dir != "left":
                                snake_dir = "right"

                        def go_down():
                            global snake_dir
                            if snake_dir != "up":
                                snake_dir = "down"

                        def go_left():
                            global snake_dir
                            if snake_dir != "right":
                                snake_dir = "left"

                        screen = turtle.Screen()
                        screen.setup(w, h)
                        screen.title("Snake")
                        screen.bgcolor("blue")
                        screen.setup(500, 500)
                        screen.tracer(0)

                        pen = turtle.Turtle("square")
                        pen.penup()

                        food = turtle.Turtle()
                        food.shape("square")
                        food.color("yellow")
                        food.shapesize(food_size / 20)
                        food.penup()

                        screen.listen()
                        screen.onkey(go_up, "Up")
                        screen.onkey(go_right, "Right")
                        screen.onkey(go_down, "Down")
                        screen.onkey(go_left, "Left")

                        reset()
                        turtle.done()

                    elif "game 2" in query:

                        speak("starting sudoku game")

                        pygame.font.init()
                        Window = pygame.display.set_mode((500, 500))
                        pygame.display.set_caption("SUDOKU GAME by DataFlair")
                        x = 0
                        z = 0
                        diff = 500 / 9
                        value = 0
                        defaultgrid = [
                            [0, 0, 4, 0, 6, 0, 0, 0, 5],
                            [7, 8, 0, 4, 0, 0, 0, 2, 0],
                            [0, 0, 2, 6, 0, 1, 0, 7, 8],
                            [6, 1, 0, 0, 7, 5, 0, 0, 9],
                            [0, 0, 7, 5, 4, 0, 0, 6, 1],
                            [0, 0, 1, 7, 5, 0, 9, 3, 0],
                            [0, 7, 0, 3, 0, 0, 0, 1, 0],
                            [0, 4, 0, 2, 0, 6, 0, 0, 7],
                            [0, 2, 0, 0, 0, 7, 4, 0, 0],
                        ]

                        font = pygame.font.SysFont("comicsans", 40)
                        pygame.font.SysFont("comicsans", 20)

                        def cord(position):
                            global x
                            x = position[0] // diff
                            global z
                            z = position[1] // diff

                        def highlightbox():
                            for k in range(2):
                                pygame.draw.line(Window, (0, 0, 0), (x * diff - 3, (z + k) * diff),
                                                 (x * diff + diff + 3, (z + k) * diff), 7)
                                pygame.draw.line(Window, (0, 0, 0), ((x + k) * diff, z * diff),
                                                 ((x + k) * diff, z * diff + diff),
                                                 7)

                        def drawlines():
                            for i in range(9):
                                for j in range(9):
                                    if defaultgrid[i][j] != 0:
                                        pygame.draw.rect(Window, (255, 255, 0), (i * diff, j * diff, diff + 1, diff + 1))
                                        text1 = font.render(str(defaultgrid[i][j]), 1, (0, 0, 0))
                                        Window.blit(text1, (i * diff + 15, j * diff + 15))
                            for l in range(10):
                                if l % 3 == 0:
                                    thick = 7
                                else:
                                    thick = 1
                                pygame.draw.line(Window, (0, 0, 0), (0, l * diff), (500, l * diff), thick)
                                pygame.draw.line(Window, (0, 0, 0), (l * diff, 0), (l * diff, 500), thick)

                        def fillvalue(val):
                            text1 = font.render(str(val), 1, (0, 0, 0))
                            Window.blit(text1, (x * diff + 15, z * diff + 15))

                        def raiseerror():
                            text1 = font.render("wrong!", 1, (0, 0, 0))
                            Window.blit(text1, (20, 570))

                        def raiseerror1():
                            text1 = font.render("wrong ! enter a valid key for the game", 1, (0, 0, 0))
                            Window.blit(text1, (20, 570))

                        def validvalue(m, k, l, val):
                            for it in range(9):
                                if m[k][it] == val:
                                    return False
                                if m[it][l] == val:
                                    return False
                            it = k // 3
                            jt = l // 3
                            for k in range(it * 3, it * 3 + 3):
                                for l in range(jt * 3, jt * 3 + 3):
                                    if m[k][l] == val:
                                        return False
                            return True

                        def solvegame(defaugrid, i, j):
                            while defaugrid[i][j] != 0:
                                if i < 8:
                                    i += 1
                                elif i == 8 and j < 8:
                                    i = 0
                                    j += 1
                                elif i == 8 and j == 8:
                                    return True
                                pygame.event.pump()
                            for it in range(1, 10):
                                if validvalue(defaugrid, i, j, it):
                                    defaugrid[i][j] = it
                                    global x, z
                                    x = i
                                    z = j
                                    Window.fill((255, 255, 255))
                                    drawlines()
                                    highlightbox()
                                    pygame.display.update()
                                    pygame.time.delay(20)
                                    if solvegame(defaugrid, i, j) == 1:
                                        return True
                                    else:
                                        defaugrid[i][j] = 0
                                    Window.fill((0, 0, 0))

                                    drawlines()
                                    highlightbox()
                                    pygame.display.update()
                                    pygame.time.delay(50)
                            return False

                        def gameresult():
                            text1 = font.render("game finished ", 1, (0, 0, 0))
                            Window.blit(text1, (20, 570))

                        flag = True
                        flag1 = 0
                        flag2 = 0
                        rs = 0
                        error = 0

                        while flag:
                            Window.fill((255, 182, 193))
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    flag = False
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    flag1 = 1
                                    pos = pygame.mouse.get_pos()
                                    cord(pos)
                                if event.type == pygame.KEYDOWN:
                                    if event.key == pygame.K_LEFT:
                                        x -= 1
                                        flag1 = 1
                                    if event.key == pygame.K_RIGHT:
                                        x += 1
                                        flag1 = 1
                                    if event.key == pygame.K_UP:
                                        z -= 1
                                        flag1 = 1
                                    if event.key == pygame.K_DOWN:
                                        z += 1
                                        flag1 = 1
                                    if event.key == pygame.K_1:
                                        value = 1
                                    if event.key == pygame.K_2:
                                        value = 2
                                    if event.key == pygame.K_3:
                                        value = 3
                                    if event.key == pygame.K_4:
                                        value = 4
                                    if event.key == pygame.K_5:
                                        value = 5
                                    if event.key == pygame.K_6:
                                        value = 6
                                    if event.key == pygame.K_7:
                                        value = 7
                                    if event.key == pygame.K_8:
                                        value = 8
                                    if event.key == pygame.K_9:
                                        value = 9
                                    if event.key == pygame.K_RETURN:
                                        flag2 = 1
                                    if event.key == pygame.K_r:
                                        rs = 0
                                        error = 0
                                        flag2 = 0
                                        defaultgrid = [
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0],
                                            [0, 0, 0, 0, 0, 0, 0, 0, 0]
                                        ]
                                    if event.key == pygame.K_d:
                                        rs = 0
                                        error = 0
                                        flag2 = 0
                                        defaultgrid = [
                                            [0, 0, 4, 0, 6, 0, 0, 0, 5],
                                            [7, 8, 0, 4, 0, 0, 0, 2, 0],
                                            [0, 0, 2, 6, 0, 1, 0, 7, 8],
                                            [6, 1, 0, 0, 7, 5, 0, 0, 9],
                                            [0, 0, 7, 5, 4, 0, 0, 6, 1],
                                            [0, 0, 1, 7, 5, 0, 9, 3, 0],
                                            [0, 7, 0, 3, 0, 0, 0, 1, 0],
                                            [0, 4, 0, 2, 0, 6, 0, 0, 7],
                                            [0, 2, 0, 0, 0, 7, 4, 0, 0],
                                        ]
                            if flag2 == 1:
                                if not solvegame(defaultgrid, 0, 0):
                                    error = 1
                                else:
                                    rs = 1
                                flag2 = 0
                            if value != 0:
                                fillvalue(value)
                                if validvalue(defaultgrid, int(x), int(z), value):
                                    defaultgrid[int(x)][int(z)] = value
                                    flag1 = 0
                                else:
                                    defaultgrid[int(x)][int(z)] = 0
                                    raiseerror1()
                                value = 0

                            if error == 1:
                                raiseerror()
                            if rs == 1:
                                gameresult()
                            drawlines()
                            if flag1 == 1:
                                highlightbox()
                            pygame.display.update()

                        pygame.quit()


                    elif "open your command list" in query:

                        speak("sure!!")
                        print("1. I can search anything from the wikipedia")
                        print("2. I can open various browsers you just have to say the name ")
                        print("3. I can play music")
                        print("4. I can send mails with subject to any recipient")
                        print("5. I can calculate the distance between two places")
                        print("6. I can generate random passwords as per your length ")
                        print("7. I can give some options to the user like to play games whe he/she is bored ")
                        print("8. I can show the weather forecast of any city worldwide")
                        print("9. I can translate any sentence in any langauge")
                        print("10. it can solve simple math arguments")

                        speak("1. I can search anything from the wikipedia")
                        speak("2. I can open various browsers you just have to say the name ")
                        speak("3. I can play music ")
                        speak("4. I can send mails with subject to any recipient")
                        speak("5. I can calculate the distance between two places")
                        speak("6. I can generate random passwords as per your length ")
                        speak("7. I can give some options to the user like to play games when the user is bored")
                        speak("8. I can show the weather forecast of any city from any part of the world..")
                        speak("9. I can translator any sentence in any langauge")
                        speak("10. it can solve simple math arguments")

                    elif "show me the weather forecast" in query:

                        "AAAAPPPPIIII_____KKKKEEEEYYYY"
                        base_url = "http://api.openweathermap.org/data/2.5/weather?"

                        speak("please say the city name ")
                        city_name = takeCommand()
                        complete_url = base_url + "appid=" + 'd850f7f52bf19300a9eb4b0aa6b80f0d' + "&q=" + city_name
                        response = requests.get(complete_url)
                        x = response.json()

                        if x["cod"] != "404":
                            y = x["main"]

                            current_temperature = y["temp"]
                            z = x["weather"]

                            weather_description = z[0]["description"]

                            speak("calculating the approximate results!!")
                            result = (" Temperature (in kelvin unit) = " + str(
                                current_temperature) + " \n description = " + str(
                                weather_description))
                            print(result)
                            speak(result)
                        else:
                            print(" City Not Found ")
                            speak("please say a valid name!!")

                    elif "translate the sentence" in query:

                        speak("opening translator")
                        Screen = Tk()
                        Screen.title("Language Translator with GUI by- TechVidvan")

                        InputLanguageChoice = StringVar()
                        TranslateLanguageChoice = StringVar()

                        LanguageChoices = {'Hindi', 'English', 'French', 'German', 'Spanish'}
                        InputLanguageChoice.set('English')
                        TranslateLanguageChoice.set('Hindi')

                        def Translate():
                            translator = Translator(from_lang=InputLanguageChoice.get(),
                                                    to_lang=TranslateLanguageChoice.get())
                            Translation = translator.translate(TextVar.get())
                            OutputVar.set(Translation)

                        InputLanguageChoiceMenu = OptionMenu(Screen, InputLanguageChoice, *LanguageChoices)
                        Label(Screen, text="Choose a Language").grid(row=0, column=1)
                        InputLanguageChoiceMenu.grid(row=1, column=1)

                        NewLanguageChoiceMenu = OptionMenu(Screen, TranslateLanguageChoice, *LanguageChoices)
                        Label(Screen, text="Translated Language").grid(row=0, column=2)
                        NewLanguageChoiceMenu.grid(row=1, column=2)

                        Label(Screen, text="Enter Text").grid(row=2, column=0)
                        TextVar = StringVar()
                        Entry(Screen, textvariable=TextVar).grid(row=2, column=1)

                        Label(Screen, text="Output Text").grid(row=2, column=2)
                        OutputVar = StringVar()
                        Entry(Screen, textvariable=OutputVar).grid(row=2, column=3)

                        Button(Screen, text="Translate", command=Translate, relief=GROOVE).grid(row=3, column=1, columnspan=3)
                        mainloop()

                    elif "open calculator" in query:

                        print("opening calculator...")
                        speak("opening calculator...")
                        window = tk.Tk()
                        window.title('Claculator-GeeksForGeeks')
                        frame = tk.Frame(master=window, bg="black", padx=10)
                        frame.pack()
                        entry = tk.Entry(master=frame, relief=SUNKEN, borderwidth=3, width=30)
                        entry.grid(row=0, column=0, columnspan=3, ipady=2, pady=2)

                        def myclick(number):
                            entry.insert(tk.END, number)

                        def equal():
                            try:
                                y = str(eval(entry.get()))
                                entry.delete(0, tk.END)
                                entry.insert(0, y)
                            except:
                                tkinter.messagebox.showinfo("Error", "Syntax Error")

                        def clear():
                            entry.delete(0, tk.END)

                        button_1 = tk.Button(master=frame, text='1', padx=15,
                                             pady=5, width=3, command=lambda: myclick(1))
                        button_1.grid(row=1, column=0, pady=2)
                        button_2 = tk.Button(master=frame, text='2', padx=15,
                                             pady=5, width=3, command=lambda: myclick(2))
                        button_2.grid(row=1, column=1, pady=2)
                        button_3 = tk.Button(master=frame, text='3', padx=15,
                                             pady=5, width=3, command=lambda: myclick(3))
                        button_3.grid(row=1, column=2, pady=2)
                        button_4 = tk.Button(master=frame, text='4', padx=15,
                                             pady=5, width=3, command=lambda: myclick(4))
                        button_4.grid(row=2, column=0, pady=2)
                        button_5 = tk.Button(master=frame, text='5', padx=15,
                                             pady=5, width=3, command=lambda: myclick(5))
                        button_5.grid(row=2, column=1, pady=2)
                        button_6 = tk.Button(master=frame, text='6', padx=15,
                                             pady=5, width=3, command=lambda: myclick(6))
                        button_6.grid(row=2, column=2, pady=2)
                        button_7 = tk.Button(master=frame, text='7', padx=15,
                                             pady=5, width=3, command=lambda: myclick(7))
                        button_7.grid(row=3, column=0, pady=2)
                        button_8 = tk.Button(master=frame, text='8', padx=15,
                                             pady=5, width=3, command=lambda: myclick(8))
                        button_8.grid(row=3, column=1, pady=2)
                        button_9 = tk.Button(master=frame, text='9', padx=15,
                                             pady=5, width=3, command=lambda: myclick(9))
                        button_9.grid(row=3, column=2, pady=2)
                        button_0 = tk.Button(master=frame, text='0', padx=15,
                                             pady=5, width=3, command=lambda: myclick(0))
                        button_0.grid(row=4, column=1, pady=2)

                        button_add = tk.Button(master=frame, text="+", padx=15,
                                               pady=5, width=3, command=lambda: myclick('+'))
                        button_add.grid(row=5, column=0, pady=2)

                        button_subtract = tk.Button(
                            master=frame, text="-", padx=15, pady=5, width=3, command=lambda: myclick('-'))
                        button_subtract.grid(row=5, column=1, pady=2)

                        button_multiply = tk.Button(
                            master=frame, text="*", padx=15, pady=5, width=3, command=lambda: myclick('*'))
                        button_multiply.grid(row=5, column=2, pady=2)

                        button_div = tk.Button(master=frame, text="/", padx=15,
                                               pady=5, width=3, command=lambda: myclick('/'))
                        button_div.grid(row=6, column=0, pady=2)

                        button_clear = tk.Button(master=frame, text="clear",
                                                 padx=15, pady=5, width=12, command=clear)
                        button_clear.grid(row=6, column=1, columnspan=2, pady=2)

                        button_equal = tk.Button(master=frame, text="=", padx=15,
                                                 pady=5, width=9, command=equal)
                        button_equal.grid(row=7, column=0, columnspan=3, pady=2)

                        window.mainloop()

                    elif "thank you" in query:

                        speak("no need to thank me that's what i do!!")

                    # elif "latest news" in query:

                    #     newsapi = NewsApiClient(api_key='4dbc17e007ab436fb66416009dfb59a8')
                    #     speak("enter the country below..")
                    #     input_country = takeCommand()
                    #     input_countries = [f'{input_country.strip()}']
                    #     countries = {}

                    #     for country in pycountry.countries:
                    #         countries[country.name] = country.alpha_2

                    #     codes = [countries.get(country.title(), 'Unknown code')
                    #              for country in input_countries]

                    #     speak("which category are you interested in? there is a list given below input any one...")
                    #     option = takeCommand()
                    #     top_headlines = newsapi.get_top_headlines(category=f'{option.lower()}', language='en',
                    #                                               country=f'{codes[0].lower()}')

                    #     Headlines = top_headlines['articles']

                    #     if Headlines:
                    #         for articles in Headlines:
                    #             b = articles['title'][::-1].index("-")
                    #             if "news" in (articles['title'][-b + 1:]).lower():
                    #                 print(f"{articles['title'][-b + 1:]}: {articles['title'][:-b - 2]}.")
                    #             else:
                    #                 result = f"{articles['title'][-b + 1:]} News: {articles['title'][:-b - 2]}."
                    #                 speak(result)
                    #                 print(f"{articles['title'][-b + 1:]} News: {articles['title'][:-b - 2]}.")
                    #     else:
                    #         print(f"Sorry no articles found for {input_country}, Something Wrong!!!")

                    elif "stop" in query:
                        exit()

                    elif "alexa" in query:
                        speak("i am eva not that alexa ")
                        speak('dont you ever call me alexa again otherwise i will not follow your command ')
                        exit()

                    elif "siri" in query:
                        speak("i am eva not that siri ")
                        speak("dont you ever call me alexa again otherwise i will not follow your command")
                        exit()

                    elif "i want to calculate tokens" in query:

                        import spacy
                        from spacy import displacy

                        nlp = spacy.load('en_core_web_sm')
                        speak("which is the text, you want to find tokens of?")
                        text = takeCommand()
                        doc = nlp(text)
                        sentences = list(doc.sents)
                        print(sentences)
                        for token in doc:
                            print(token.text)
                            speak(token.text)
                        ents = [(e.text, e.start_char, e.end_char, e.label_) for e in doc.ents]
                        print(ents)
                        speak(ents)
                        displacy.render(doc, style='ent', jupyter=True)

                    elif "sentiment" in query:

                        from transformers import pipeline

                        sentiment_pipeline = pipeline("sentiment-analysis")
                        speak("please say a sentence to calculate the sentiment behind that sentence:")
                        data = "i am jainam and i am in love with my job."
                        sentiment_pipeline(data)

                    elif "retina" in query:
                        speak("starting the iris verification")
                        import cv2

                        eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
                        cap = cv2.VideoCapture(0)
                        ret, color_img = cap.read()
                        gray_img = cv2.cvtColor(color_img, cv2.COLOR_BGR2GRAY)

                        eyes = eye_cascade.detectMultiScale(gray_img)
                        for (ex, ey, ew, eh) in eyes:
                            cv2.rectangle(color_img, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

                        cv2.imshow('img', color_img)
                        cv2.waitKey(1)
                        cv2.destroyAllWindows()

                    elif "boring" in query:
                        if True:
                            speak("what you wanna do today??")
                            if takeCommand() == "show me some movies":

                                speak("which type of movies you wanna see??")
                                speak("we have many options you can select from..")
                                speak("options like thriller , action , romance, animated series , science fiction, adventure , comedy , drama, horror, tragedy")
                                if True:

                                        if takeCommand() == "thriller":

                                            speak("opening some options of thriller movies")
                                            webbrowser.open('https://www.themoviedb.org/genre/53-thriller/movie')

                                        elif takeCommand() == "action":

                                            speak("opening some options of action movies")
                                            webbrowser.open("https://www.imdb.com/search/title/?genres=action")

                                        elif takeCommand() == "romance":
                                            speak("opening some options of romance movies")
                                            webbrowser.open(
                                                "https://www.goodhousekeeping.com/life/entertainment/g30416771/best-romantic-movies/")

                                        elif takeCommand() == "animated series":
                                            speak("opening some options of animated series")
                                            webbrowser.open(
                                                "https://www.imdb.com/search/title/?genres=animation&explore=title_type,genres&title_type=tvSeries")

                                        elif takeCommand() == "science fiction":
                                            speak("opening some options of sci-fi movies")
                                            webbrowser.open("https://www.imdb.com/genre/sci_fi")

                                        elif takeCommand() == "adventure":
                                            speak("opening some options of adventure movies")
                                            webbrowser.open(
                                                "https://www.cosmopolitan.com/entertainment/movies/g36501097/best-adventure-movies/")

                                        elif takeCommand() == "comedy":
                                            speak("opening some options of comedy movies")
                                            webbrowser.open(
                                                "https://www.imdb.com/search/title/?genres=comedy&title_type=feature&explore=genres")

                                        elif takeCommand() == "drama":
                                            speak("opening some options of drama movies")
                                            webbrowser.open(
                                                "https://www.businessinsider.com/best-drama-movies-all-time-critics-2018-7")

                                        elif takeCommand() == "horror":
                                            speak("opening some options of horror movies")
                                            webbrowser.open("https://www.timeout.com/film/best-horror-films")

                                        elif takeCommand() == "tragedy":
                                            speak("opening some options of tragedy movies")
                                            webbrowser.open("https://www.esquire.com/entertainment/movies/g32308973/best-sad-movies-of-all-time/")

                                else:
                                    exit()

                            elif takeCommand() == "lets hear some music":

                                    speak("which type of songs you wanna listen??")
                                    speak("we have many options you can select from..")
                                    speak("options like pop , rock , hip hop, bollywood, party, sad , happy, punjabi")

                                    if True:

                                        if takeCommand() == "pop":

                                            speak("playing some pop songs from youtube")
                                            webbrowser.open("https://www.youtube.com/watch?v=5zSCWKKnajU")

                                        elif takeCommand() == "rock":

                                            speak("playing some rock songs from youtube")
                                            webbrowser.open("https://www.youtube.com/watch?v=YtfNtUFOX0I")

                                        elif takeCommand() == "hiphop":

                                            speak("playing some hip-hop songs from youtube")
                                            webbrowser.open("https://www.youtube.com/watch?v=ydhMkYWycGc")

                                        elif takeCommand() == "bollywood":

                                            speak("playing some bollywood songs from youtube")
                                            webbrowser.open("https://www.youtube.com/watch?v=xsSpsUKlPKk")

                                        elif takeCommand() == "party":

                                            speak("playing some party songs from youtube")
                                            webbrowser.open("https://www.youtube.com/watch?v=PACi4CPTFUQ")

                                        elif takeCommand() == "sad":

                                            speak("playing some sad songs from youtube")
                                            webbrowser.open("https://www.youtube.com/watch?v=zkT1HjFjTCY")

                                        elif takeCommand() == "happy":

                                            speak("playing some happy songs from youtube")
                                            webbrowser.open("https://www.youtube.com/watch?v=pRbxlpvXw2s&t=247s")

                                        elif takeCommand() == "punjabi":

                                            speak("playing some punjabi songs from youtube")
                                            webbrowser.open("https://www.youtube.com/watch?v=QcDqtbtw-zI")

                                        else:
                                            speak("please give a correct song name")
                                            exit()

                    elif "detect age and gender" in query:

                        import cv2

                        def faceBox(faceNet, frame):
                            frameHeight = frame.shape[0]
                            frameWidth = frame.shape[1]
                            blob = cv2.dnn.blobFromImage(frame, 1.0, (300, 300), [104, 117, 123], swapRB=False)
                            faceNet.setInput(blob)
                            detection = faceNet.forward()
                            bboxs = []
                            for i in range(detection.shape[2]):
                                confidence = detection[0, 0, i, 2]
                                if confidence > 0.7:
                                    x1 = int(detection[0, 0, i, 3] * frameWidth)
                                    y1 = int(detection[0, 0, i, 4] * frameHeight)
                                    x2 = int(detection[0, 0, i, 5] * frameWidth)
                                    y2 = int(detection[0, 0, i, 6] * frameHeight)
                                    bboxs.append([x1, y1, x2, y2])
                                    cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                            return frame, bboxs

                        faceProto = "opencv_face_detector.pbtxt"
                        faceModel = "opencv_face_detector_uint8.pb"

                        ageProto = "age_deploy.prototxt"
                        ageModel = "age_net.caffemodel"

                        genderProto = "gender_deploy.prototxt"
                        genderModel = "gender_net.caffemodel"

                        faceNet = cv2.dnn.readNet(faceModel, faceProto)
                        ageNet = cv2.dnn.readNet(ageModel, ageProto)
                        genderNet = cv2.dnn.readNet(genderModel, genderProto)

                        MODEL_MEAN_VALUES = (78.4263377603, 87.7689143744, 114.895847746)
                        ageList = ['(0-2)', '(4-6)', '(8-12)', '(15-20)', '(25-32)', '(38-43)', '(48-53)', '(60-100)']
                        genderList = ['Male', 'Female']

                        video = cv2.VideoCapture(0)

                        padding = 20

                        while True:
                            ret, frame = video.read()
                            frame, bboxs = faceBox(faceNet, frame)
                            for bbox in bboxs:
                                # face=frame[bbox[1]:bbox[3], bbox[0]:bbox[2]]
                                face = frame[max(0, bbox[1] - padding):min(bbox[3] + padding, frame.shape[0] - 1), max(0, bbox[0] - padding):min(bbox[2] + padding, frame.shape[1] - 1)]
                                blob = cv2.dnn.blobFromImage(face, 1.0, (227, 227), MODEL_MEAN_VALUES, swapRB=False)
                                genderNet.setInput(blob)
                                genderPred = genderNet.forward()
                                gender = genderList[genderPred[0].argmax()]

                                ageNet.setInput(blob)
                                agePred = ageNet.forward()
                                age = ageList[agePred[0].argmax()]
                                label = "{},{}".format(gender, age)
                                cv2.rectangle(frame, (bbox[0], bbox[1] - 30), (bbox[2], bbox[1]), (0, 255, 0), -1)
                                cv2.putText(frame, label, (bbox[0], bbox[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8,
                                            (255, 255, 255), 2, cv2.LINE_AA)
                            cv2.imshow("Age-Gender", frame)
                            k = cv2.waitKey(1)
                            if k == ord('q'):
                                break
                        video.release()
                        cv2.destroyAllWindows()

                    elif "message or call" in query:
                        import os
                        from twilio.rest import Client

                        account_sid = "xxxxxxxxxxxxxxxxxxxxxxxx"
                        auth_token = "xxxxxxxxxxxxxxxxxxxxxxxx"
                        speak("what you wanna do send a text message or make an outbound call?")

                        if "message" in query:
                            speak(" first say the number whom you want to send the text message, then the message you wanna share via text")
                            client = Client(account_sid, auth_token)
                            client.messages.create(from_="+18129661262", to=takeCommand(), body=takeCommand())
                            print("your message has been sent to %d", to)
                            speak(print)

                        else:
                            speak("say the number whom you want make an outbound call")
                            call = client.calls.create(url='http://demo.twilio.com/docs/classic.mp3', from_="+18129661262", to=takeCommand())
                            print(call.sid)
                            speak("your outbound call is on")

                    elif "make a todo list " in query:

                        import tkinter as tk
                        from tkinter import ttk
                        from tkinter import messagebox
                        import sqlite3 as sql

                        speak("opening to-do list!!!")

                        def add_task():
                            task_string = task_field.get()

                            if len(task_string) == 0:
                                messagebox.showinfo('Error', 'Field is Empty.')
                            else:
                                tasks.append(task_string)
                                the_cursor.execute('insert into tasks values (?)', (task_string,))
                                list_update()
                                task_field.delete(0, 'end')

                        def list_update():
                            clear_list()
                            for task in tasks:
                                task_listbox.insert('end', task)

                        def delete_task():
                            try:
                                the_value = task_listbox.get(task_listbox.curselection())
                                if the_value in tasks:
                                    tasks.remove(the_value)
                                    list_update()
                                    the_cursor.execute('delete from tasks where title = ?', (the_value,))
                            except:
                                messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

                        def delete_all_tasks():
                            message_box = messagebox.askyesno('Delete All', 'Are you sure?')
                            if message_box:
                                while len(tasks) != 0:
                                    tasks.pop()
                                the_cursor.execute('delete from tasks')
                                list_update()

                        def clear_list():
                            task_listbox.delete(0, 'end')

                        def close():
                            print(tasks)
                            guiWindow.destroy()

                        def retrieve_database():
                            while len(tasks) != 0:
                                tasks.pop()
                            for row in the_cursor.execute('select title from tasks'):
                                tasks.append(row[0])

                        if __name__ == "__main__":
                            guiWindow = tk.Tk()
                            guiWindow.title("To-Do List Manager - Jainam Mehta")
                            guiWindow.geometry("500x450+750+250")
                            guiWindow.resizable(0, 0)
                            guiWindow.configure(bg="#FAEBD7")

                            the_connection = sql.connect('listOfTasks.db')
                            the_cursor = the_connection.cursor()
                            the_cursor.execute('create table if not exists tasks (title text)')

                            tasks = []

                            header_frame = tk.Frame(guiWindow, bg="#FAEBD7")
                            functions_frame = tk.Frame(guiWindow, bg="#FAEBD7")
                            listbox_frame = tk.Frame(guiWindow, bg="#FAEBD7")

                            header_frame.pack(fill="both")
                            functions_frame.pack(side="left", expand=True, fill="both")
                            listbox_frame.pack(side="right", expand=True, fill="both")

                            header_label = ttk.Label(
                                header_frame,
                                text="The To-Do List",
                                font=("Brush Script MT", "30"),
                                background="#FAEBD7",
                                foreground="#8B4513"
                            )
                            header_label.pack(padx=20, pady=20)

                            task_label = ttk.Label(
                                functions_frame,
                                text="Enter the Task:",
                                font=("Consolas", "11", "bold"),
                                background="#FAEBD7",
                                foreground="#000000"
                            )
                            task_label.place(x=30, y=40)

                            task_field = ttk.Entry(
                                functions_frame,
                                font=("Consolas", "12"),
                                width=18,
                                background="#FFF8DC",
                                foreground="#A52A2A"
                            )
                            task_field.place(x=30, y=80)

                            add_button = ttk.Button(
                                functions_frame,
                                text="Add Task",
                                width=24,
                                command=add_task
                            )
                            del_button = ttk.Button(
                                functions_frame,
                                text="Delete Task",
                                width=24,
                                command=delete_task
                            )
                            del_all_button = ttk.Button(
                                functions_frame,
                                text="Delete All Tasks",
                                width=24,
                                command=delete_all_tasks
                            )
                            exit_button = ttk.Button(
                                functions_frame,
                                text="Exit",
                                width=24,
                                command=close
                            )
                            add_button.place(x=30, y=120)
                            del_button.place(x=30, y=160)
                            del_all_button.place(x=30, y=200)
                            exit_button.place(x=30, y=240)

                            task_listbox = tk.Listbox(
                                listbox_frame,
                                width=26,
                                height=13,
                                selectmode='SINGLE',
                                background="#FFFFFF",
                                foreground="#000000",
                                selectbackground="#CD853F",
                                selectforeground="#FFFFFF"
                            )

                            task_listbox.place(x=10, y=20)

                            retrieve_database()
                            list_update()
                            guiWindow.mainloop()
                            the_connection.commit()
                            the_cursor.close()

                    elif "convert my pdf to audio book" in query:

                        import pyttsx3
                        import pdfplumber
                        import PyPDF2

                        speak("your pdf is converting in audio!!!!")
                        file = "C:\\BDA\\scholarship.pdf"

                        pdfFileObj = open(file, 'rb')

                        reader = PyPDF2.PdfReader(pdfFileObj)

                        pages = len(reader.pages)

                        with pdfplumber.open(file) as pdf:
                            for i in range(0, pages):
                                page = pdf.pages[i]
                                text = page.extract_text()
                                print(text)
                                speaker = pyttsx3.init()
                                speaker.say(text)
                                speaker.runAndWait()

        return Recognization()

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/')
@app.route('/listening.html')
def listeninghtml():
        return render_template("listening.html.html")

@app.route('/')
@app.route('/start recognization', methods=['GET', 'POST'])
def start_recognization():
    if request.method == 'POST':
        A = Recognization()
        if Recognization() == A:
            return A
    return render_template("home.html", A=Recognization())

if __name__ == '__main__':
    app.run(debug=True, port=8020)