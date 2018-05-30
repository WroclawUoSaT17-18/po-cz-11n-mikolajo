from tkinter import *
from PIL import Image
from PIL import ImageTk
import numpy as np
from tkinter import filedialog
import cv2
import copy
import sqlite3
import os


class popupWindow(object):
    def __init__(self, master):
        top=self.top = Toplevel(master)
        self.l = Label(top,text="Rozpoznawanie twarzy")
        self.l.pack()
        self.e = Entry(top)
        self.e.pack()
        self.b = Button(top,text='Ok',command=self.cleanup)
        self.b.pack()

    def cleanup(self):
        self.value=self.e.get()
        self.top.destroy()


class mainWindow(object):
    def __init__(self, master):
        self.master = master
        self.b = Button(master,text="Znajdz osobe",command=search_sql)
        self.b.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
        self.b2 = Button(master,text="Wprowadz osobe",command=select_image)
        self.b2.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
        self.b3 = Button(master, text="Wprowadz imie", command=self.popup)
        self.b3.pack(side="top", fill="both", expand="yes", padx="10", pady="10")

    def popup(self):
        self.w=popupWindow(self.master)
        self.b["state"] = "disabled"
        self.master.wait_window(self.w.top)
        self.b["state"] = "normal"

    def entryValue(self):
        return self.w.value


conn = sqlite3.connect('database.db')
c = conn.cursor()
sql = """
DROP TABLE IF EXISTS users;
CREATE TABLE users (
           id integer unique primary key autoincrement,
           name text
);
"""
c.executescript(sql)
conn.commit()
conn.close()

# detekcja twarzy
face_cascade = cv2.CascadeClassifier(
    "C:/Users/okrzesa/Documents/uczelnia/Projekt/opencvenv/haarcascade_frontalface_default.xml")


def search_sql():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    path = 'dataset'
    if not os.path.exists('./recognizer'):
        os.makedirs('./recognizer')

    def getImagesWithID(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faces = []
        IDs = []
        for imagePath in imagePaths:
            faceImg = Image.open(imagePath).convert('L')
            faceNp = np.array(faceImg, 'uint8')
            ID = int(os.path.split(imagePath)[-1].split('.')[1])
            faces.append(faceNp)
            IDs.append(ID)
            cv2.imshow("training", faceNp)
            cv2.waitKey(10)
        return np.array(IDs), faces

    Ids, faces = getImagesWithID(path)
    recognizer.train(faces, Ids)
    recognizer.save('recognizer/trainingData.yml')
    cv2.destroyAllWindows()

    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    fname = "recognizer/trainingData.yml"
    if not os.path.isfile(fname):
        print("Please train the data first")
        exit(0)
    face_cascade = cv2.CascadeClassifier(
        "C:/Users/okrzesa/Documents/uczelnia/Projekt/opencvenv/haarcascade_frontalface_default.xml")
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read(fname)
    path = filedialog.askopenfilename()
    image = cv2.imread(path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.08,
        minNeighbors=7,
    )
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 3)
        ids, conf = recognizer.predict(gray[y:y + h, x:x + w])
        c.execute("select name from users where id = (?);", (ids,))
        result = c.fetchall()
        name = result[0][0]
        if conf < 50:
            cv2.putText(image, name, (x + 2, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (150, 255, 0), 2)
        else:
            cv2.putText(image, 'Brak osoby w bazie', (x + 2, y + h - 5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow('Face Recognizer', image)
    cv2.waitKey(30) & 0xff
    cv2.waitKey(0)
    conn.commit()
    conn.close()



def select_image():

    conn = sqlite3.connect('database.db')
    if not os.path.exists('./dataset'):
        os.makedirs('./dataset')
    c = conn.cursor()
    # "Panele" - widżet w tkiner - gui
    global panelA, panelB

    # możliwość wyboru pliku
    path = filedialog.askopenfilename()

    # potwierdzenie wyboru pliku
    if len(path) > 0:
        c.execute('INSERT INTO users (name) VALUES (?)', (m.entryValue(),))
        uid = c.lastrowid
        sampleNum = 0
        while True:
            # załadowanie zdjęcia następnie wykonianie jego kopii nastepnie przekształcenie do grayscale <- wymagane w
            # detekcji twarzy
            image = cv2.imread(path)
            fix = copy.copy(image)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            # detekcja
            detect = face_cascade.detectMultiScale(
                gray,
                scaleFactor=1.08,
                minNeighbors=7,
            )
            # tworzenie obramowania
            for (x, y, w, h) in detect:
                sampleNum = sampleNum + 1
                cv2.imwrite("dataset/User." + str(uid) + "." + str(sampleNum) + ".jpg", gray[y:y + h, x:x + w])
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.waitKey(100)
            if sampleNum > 2:
                break

        conn.commit()
        conn.close()

        # zamiana kanałów kolorów
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        fix = cv2.cvtColor(fix, cv2.COLOR_BGR2RGB)

        # zamiana zdjecia na format z zgodny z biblioteka Pillow, a nastepnie konwersja do formatu tkinter
        image = Image.fromarray(image)
        fix = Image.fromarray(fix)
        image = ImageTk.PhotoImage(image)
        fix = ImageTk.PhotoImage(fix)

            # wlaczenie paneli - podział aplikacji
        if panelA is None or panelB is None:
            panelA = Label(image=image)
            panelA.image = image
            panelA.pack(side="right", padx=10, pady=10)
            panelB = Label(image=fix)
            panelB.image = fix
            panelB.pack(side="left", padx=10, pady=10)
            # jezeli nie laduje to wgrywa nowe zdjecie
        else:
            panelA.configure(image=image)
            panelB.configure(image=fix)
            panelA.image = image
            panelB.image = fix


# # właczenie okna
# root = Tk()
# panelA = None
# panelB = None
# # przyciski
# btn = Button(root, text="Wgraj osobe", command=select_image)
# btn.pack(side="top", fill="both", expand="yes", padx="10", pady="10")
# btn = Button(root, text="Przeglądanie bazy dancyh", command=write_sql)
# btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
# btn = Button(root, text="Select an image", command=search_sql)
# btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
# root.mainloop()

if __name__ == "__main__":
    root=Tk()
    panelB = None
    panelA = None
    m=mainWindow(root)
    root.mainloop()