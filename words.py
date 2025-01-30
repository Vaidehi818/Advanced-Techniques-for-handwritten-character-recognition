import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import cv2
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import tkinter as tk
from tkinter import filedialog

# Load the trained model for alphabet recognition
model = tf.keras.models.load_model('Alphabet_Recognition.keras')
alpha = list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')

# Define a function to preprocess the image and predict alphabets
def alphabet_recognize(filepath):
    image = cv2.imread(filepath)
    blur_image = cv2.medianBlur(image, 7)
    grey = cv2.cvtColor(blur_image, cv2.COLOR_BGR2GRAY)
    thresh = cv2.adaptiveThreshold(grey, 200, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 41, 25)
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    preprocessed_digits = []

    # Sort contours from left to right
    boundingBoxes = [cv2.boundingRect(c) for c in contours]
    (contours, boundingBoxes) = zip(*sorted(zip(contours, boundingBoxes), key=lambda b: b[1][0], reverse=False))

    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        digit = thresh[y:y+h, x:x+w]
        resized_digit = cv2.resize(digit, (18, 18))
        padded_digit = np.pad(resized_digit, ((5, 5), (5, 5)), "constant", constant_values=0)
        preprocessed_digits.append(padded_digit)
    
    # Prepare the figure for displaying
    plt.xticks([])
    plt.yticks([])
    plt.title("Contoured Image", color='red')
    plt.imshow(image, cmap="gray")
    plt.show()

    # Predict alphabets
    inp = np.array(preprocessed_digits)
    figr = plt.figure(figsize=(len(inp), 4))
    i = 1
    alphabets = []
    for digit in preprocessed_digits:
        [prediction] = model.predict(digit.reshape(1, 28, 28, 1) / 255.)
        pred = alpha[np.argmax(prediction)]
        alphabets.append(pred)
        figr.add_subplot(1, len(inp), i)
        i += 1
        plt.xticks([])
        plt.yticks([])
        plt.imshow(digit.reshape(28, 28), cmap="gray")
        plt.title(pred, color='green', fontsize=18, fontweight="bold")
    
    print("The Recognized Alphabets are:", *alphabets)
    plt.show()
    return alphabets

# Create the GUI for uploading and recognizing alphabets
class AlphabetRecognizerApp:
    def __init__(self, master):
        self.master = master
        self.file_path = None
        self.master.state('zoomed')   # Maximize the window
        self.master.title("Handwritten Character Recognizer")
        self.frame = tk.Frame(master)
        self.frame.pack(expand=True)

        self.button_upload = tk.Button(self.frame, text='Choose File', command=self.upload, width=20, height=3)
        self.button_upload.grid(row=0, column=0, padx=20, pady=20)
        self.button_predict = tk.Button(self.frame, text='Predict', command=self.predict, width=20, height=3)
        self.button_predict.grid(row=0, column=1, padx=20, pady=20)
        self.button_clear = tk.Button(self.frame, text='Clear', command=self.clear, width=20, height=3)
        self.button_clear.grid(row=0, column=2, padx=20, pady=20)

        self.label = tk.Label(master, text='', font=("Cooper Black", 22))
        self.label.pack(pady=20)

    def upload(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            if "LETTERS" in self.file_path or "DIGITS" in self.file_path:
                self.label.config(text='Please upload a suitable file')
            else:
                self.label.config(text='File selected: ' + self.file_path)

    def predict(self):
        if self.file_path:
            self.label.config(text='Processing...')
            alphabets = alphabet_recognize(self.file_path)
            self.label.config(text='The Recognized Alphabets are: ' + ' '.join(alphabets))
        else:
            self.label.config(text='Please choose a file first.')

    def clear(self):
        self.label.config(text='')
        self.file_path = None

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    custom_font = ("Helvetica", 20, "bold")
    app = AlphabetRecognizerApp(root)
    root.mainloop()
