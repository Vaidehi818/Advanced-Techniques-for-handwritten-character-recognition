import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import tkinter as tk
from tkinter import filedialog

# Load the trained model
model = tf.keras.models.load_model('handwritten_digit_recognition_model.keras')

# Define a function to predict and display results
def predict_and_display(image):
    # Predict the digit
    prediction = model.predict(np.expand_dims(image, axis=0))
    predicted_label = np.argmax(prediction)

    # Display the image and the prediction
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(image.squeeze(), cmap=plt.cm.binary)
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.plot(prediction[0], 'ro-')
    plt.xticks(range(10))
    plt.xlabel('Predicted digit: {}'.format(predicted_label))
    plt.show()

# Create the GUI for uploading and recognizing digits
class DigitRecognizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Handwritten Digit Recognizer")
        self.master.state('zoomed') # Maximize the window
        self.button_upload = tk.Button(master, text='Upload Image', command=self.upload, width=20, height=3)
        self.button_upload.pack(pady=20)
        self.button_clear = tk.Button(master, text='Clear', command=self.clear, width=20, height=3)
        self.button_clear.pack(pady=20)
        self.label = tk.Label(master, text='')
        self.label.pack()

    def upload(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            if "LETTERS" in file_path or "Handwritten-Alphabets-Recognition-master" in file_path:
                self.label.config(text='Please upload Digit(0-9) file')
            else:
                self.label.config(text='Processing...')
                img = Image.open(file_path).convert('L')
                img = ImageOps.invert(img)
                img = img.resize((28, 28))
                img = np.array(img).astype('float32') / 255
                img = img.reshape((28, 28, 1))
                predict_and_display(img)
                self.label.config(text='')

    def clear(self):
        self.label.config(text='')

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = DigitRecognizerApp(root)
    root.mainloop()
