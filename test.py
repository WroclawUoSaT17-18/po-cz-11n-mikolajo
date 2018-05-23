
from tkinter import *
from PIL import Image
from PIL import ImageTk
from tkinter import filedialog
import cv2
import copy

#detekcja twarzy
face_cascade = cv2.CascadeClassifier(
    "C:/Users/okrzesa/Documents/uczelnia/faceR/opencvenv/haarcascade_frontalface_default.xml")


def select_image():
    # "Panele" - widżet w tkiner - gui
    global panelA, panelB

    # możliwość wyboru pliku
    path = filedialog.askopenfilename()

    # potwierdzenie wyboru pliku
    if len(path) > 0:
        # załadowanie zdjęcia następnie wykonianie jego kopii nastepnie przekształcenie do grayscale <- wymagane w
        # detekcji twarzy
        image = cv2.imread(path)
        fix = copy.copy(image)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # detekcja
        detect = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=6,
        )
        # tworzenie obramowania
        for (x, y, w, h) in detect:
            detect = cv2.rectangle(fix, (x, y), (x+w, y+h), (255, 0, 0), 2)

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
            panelA.pack(side="left", padx=10, pady=10)
            panelB = Label(image=fix)
            panelB.image = fix
            panelB.pack(side="right", padx=10, pady=10)
        # jezeli nie laduje to wgrywa nowe zdjecie
        else:
            panelA.configure(image=image)
            panelB.configure(image=fix)
            panelA.image = image
            panelB.image = fix


# właczenie okna
root = Tk()
panelA = None
panelB = None
#przyciski
btn = Button(root, text="Select an image", command=select_image)
btn.pack(side="bottom", fill="both", expand="yes", padx="10", pady="10")
root.mainloop()
