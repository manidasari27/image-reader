from flask import Flask,redirect, request, render_template, url_for
from database import create_connection
import os
import requests

application = Flask(__name__)

application.config['UPLOAD_FOLDER'] = './static'

@application.route("/",methods=["GET","POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        if name and email and password:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("insert into mstr_user (name, email, password) values (%s,%s,%s)",(name, email, password))
            conn.commit()
            cur.close()
        else:
            return "Data not found"
        return render_template("signup.html")
    else:
        return render_template("signup.html")


@application.route("/login",methods=["GET","POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        if email and password:
            conn = create_connection()
            cur = conn.cursor()
            cur.execute("select * from mstr_user where email=%s and password=%s",(email, password))
            res = cur.fetchone()
            if res is None:
                return "Wrong email id password"
            else:
                return redirect("/home")
        else:
            return "Data not found"
    else:
        return render_template("login.html")


@application.route("/home", methods=["GET", "POST"])
def home():
    #API_URL = "http://127.0.0.1:4040/ocr" 
    API_URL = "http://54.206.95.67:8080/ocr"
    extracted_text = None

    if request.method == "POST":
        image_file = request.files['image']
        if image_file:
            
            file_path = os.path.join(application.config['UPLOAD_FOLDER'], image_file.filename)
            image_file.save(file_path)
            
            
            with open(file_path, 'rb') as f:
                files = {'file': (image_file.filename, f, image_file.content_type)}
                try:
                    
                    response = requests.post(API_URL, files=files)
                    
                    if response.status_code == 200:
                        data = response.json()
                        extracted_text = data.get("Extracted Text", "No text extracted")
                        print("EXTRACTED TEXT ---------->> ", extracted_text)
                    else:
                        extracted_text = f"Failed to extract text. API Response: {response.status_code}"
                except Exception as e:
                    extracted_text = f"An error occurred: {str(e)}"

    return render_template("all.html", extracted_text=extracted_text)


@application.route("/text_to_speech", methods=["GET", "POST"])
def text_to_speech():
    download_url = None
    #API_URL = "http://127.0.0.1:4040/text-to-speech"
    API_URL = "http://54.206.95.67:8080/text-to-speech"

    if request.method == "POST":

        text_input = request.form['text']
        
        if text_input:
           
            json_data = {"text": text_input}
            try:
                response = requests.get(API_URL, json=json_data, stream=True)
            
                if response.status_code == 200:
                    
                    file_path = os.path.join(application.config['UPLOAD_FOLDER'], 'api_audio.mp3')
                    with open(file_path, 'wb') as f:
                        for chunk in response.iter_content(chunk_size=1024):
                            if chunk:
                                f.write(chunk)
                    
                    download_url = url_for('static', filename='api_audio.mp3')
                else:
                    download_url = "Error generating audio. Try again."
            except Exception as e:
                download_url = f"An error occurred: {str(e)}"
    
    return render_template("all.html", download_url=download_url)


@application.route("/translator",methods=["GET","POST"])
def translator():
    translated_text = None
    if request.method == "POST":
        text_input = request.form['text']
        #API_URL = "http://127.0.0.1:5050/translate"
        API_URL = "http://translationapi-x23302712.eba-kkxumgu2.ap-northeast-1.elasticbeanstalk.com/translate"

        try:
            json_data = {"text": text_input}
            response = requests.get(API_URL, json=json_data, stream=True)
            if response.status_code == 200:
                data = response.json()
                translated_text = data.get("Translated Text", "No text translated")
                print("TRANSLATED TEXT ---------->> ",translated_text)
            else:
                translated_text = "Failed to translate text. Error from API."
        except Exception as e:
            translated_text = f"An error occurred: {str(e)}"
    return render_template("all.html",translated_text=translated_text)
    

@application.route("/summarization",methods=["GET","POST"])
def summarization():
    summary_text = None
    if request.method == "POST":
        text_input = request.form['text']
        #API_URL = "http://127.0.0.1:3030/summarize"
        API_URL = "http://x23344440-scalable-api.eba-vj4crcif.ap-southeast-2.elasticbeanstalk.com/summarize"

        try:
            json_data = {"text": text_input}
            response = requests.get(API_URL, json=json_data, stream=True)
            if response.status_code == 200:
                data = response.json()
                summary_text = data.get("Summarized Text", "No text translated")
                print("SUMMARIZED TEXT ---------->> ",summary_text)
            else:
                summary_text = "Failed to translate text. Error from API."
        except Exception as e:
            summary_text = f"An error occurred: {str(e)}"
    return render_template("all.html",summary_text=summary_text)


@application.route("/all",methods=["GET","POST"])
def all():
    if request.method == "POST":
        return render_template("all.html")
    return render_template("all.html")




if __name__ == '__main__':
    application.run(host='0.0.0.0', port=5000)


