import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageOps
import tkinter as tk
from tkinter import filedialog

# Load the trained model for alphabet recognition
model = tf.keras.models.load_model('Alphabet_Recognition.keras')

# Define a function to predict and display results
def predict_and_display(image):
    # Predict the alphabet
    prediction = model.predict(np.expand_dims(image, axis=0))
    predicted_label = np.argmax(prediction)
    predicted_alphabet = chr(predicted_label + 65)  # Convert to ASCII (A-Z)

    # Display the image and the prediction
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)
    plt.imshow(image.squeeze(), cmap=plt.cm.binary)
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.plot(prediction[0], 'ro-')
    plt.xticks(range(26), [chr(i) for i in range(65, 91)])
    plt.xlabel('Predicted alphabet: {}'.format(predicted_alphabet))
    plt.title('Prediction Probabilities')
    plt.show()

# Create the GUI for uploading and recognizing alphabets
class AlphabetRecognizerApp:
    def __init__(self, master):
        self.master = master
        self.image = None
        self.file_path = None
        self.master.state('zoomed')  # Maximize the window
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
        file_path = filedialog.askopenfilename()
        if file_path:
            self.label.config(text='File selected: ' + file_path)
            if "DIGITS" in file_path or "Handwritten-Alphabets-Recognition-master" in file_path:
                self.label.config(text='Please upload an English Alphabet file.')
            else:
                try:
                    self.label.config(text='Processing...')
                    img = Image.open(file_path).convert('L')  # Convert image to grayscale
                    img = ImageOps.invert(img)  # Invert the image
                    img = img.resize((28, 28))  # Resize to the model's expected input size
                    img = np.array(img).astype('float32') / 255  # Normalize pixel values
                    img = img.reshape((28, 28, 1))  # Reshape for the model
                    self.image = img
                    self.label.config(text='Image loaded successfully!')
                except Exception as e:
                    self.label.config(text=f'Error loading image: {str(e)}')

    def predict(self):
        if self.image is not None:
            try:
                predict_and_display(self.image)
                self.label.config(text='Prediction done!')
            except Exception as e:
                self.label.config(text=f'Error during prediction: {str(e)}')
        else:
            self.label.config(text='Please upload an image first.')

    def clear(self):
        self.label.config(text='')  # Reset the label text
        self.image = None  # Clear the image
        self.button_upload.config(state=tk.NORMAL)  # Re-enable the upload button

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = AlphabetRecognizerApp(root)
    root.mainloop()
