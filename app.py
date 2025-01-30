from flask import Flask, render_template_string
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    # HTML content with a link to open the Tkinter window
    html_content = '''
    <!doctype html>
    <html lang="en">
      <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <title>Handwritten Character Recognition</title>
        <style>
            body, html {
              margin: 0;
              padding: 0;
              font-family: Arial, sans-serif;
              overflow-x: hidden;
              }
              .header {
                text-align: left;
                padding: 10px;
                background: #FFAE42;
                color: black;
                }

.button-container {
    margin: 0 auto;
    margin-top: 60px;
    margin-bottom: 20px;
    border: 2px solid #333;
    border-radius: 10px;
    width: 240px;
    padding: 20px;
    text-align: center;
    border: 2px solid #333;
    border-radius: 10px;
    width: 240px;
    font-size: x-large;
}

.big-button {
    background-color: blue;
    color: white;
    padding: 14px 25px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
}

.big-button:hover {
  background-color: #0056b3;
}

.output {
    margin-top: 20px;
    border: 1px solid #333;
    padding: 10px;
    width: 80%;
    text-align: left;
}

.footer {
    text-align: center;
    padding: 20px;
    background: #333;
    color: white;
}
        </style>
      </head>
      <body>
      <header class="header">
        <h1>Handwritten Character Recognition</h1>
    </header>
        <div class="button-container">
          <p class="mt-5">Predict Digit</p>
          <a href="/launch" class="big-button">Launch Digit Recognizer</a>
        </div>

        <div class="button-container">
          <p class="mt-5">Predict Alphabet</p>
          <a href="/start" class="big-button">Launch Alphabet Recognizer</a>
        </div>

        <div class="button-container">
          <p class="mt-5">Predict Word</p>
          <a href="/begin" class="big-button">Launch Word Recognizer</a>
        </div>

        <footer class="footer">
        <p>&copy; 2024 Handwritten Character Recognition Project. Author - Vaidehi.D</p>
        </footer>

      </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/launch')
def launch_tkinter():
    # Launch the Tkinter application
    subprocess.Popen(["python", "digit_recognizer_gui.py"])
    return "Processing request.............."

@app.route('/start')
def start_tkinter():
    # Launch the Tkinter application
    subprocess.Popen(["python", "predict.py"])
    return "Processing request............."

@app.route('/begin')
def begin_tkinter():
    # Launch the Tkinter application
    subprocess.Popen(["python", "words.py"])
    return "Processing request................"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
