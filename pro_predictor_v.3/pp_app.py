# import dependencies
from flask import Flask,render_template,request, redirect
import pandas as pd
from sklearn.model_selection import train_test_split
from joblib import dump, load
from sklearn.ensemble import RandomForestClassifier
import pro_predict_formver
 
app = Flask(__name__)

@app.route('/')
def home():
    return redirect('/form')
 
@app.route('/form')
def form():
    return render_template('form.html')
 
@app.route('/data/', methods = ['POST', 'GET'])
def data():
    if request.method == 'GET':
        return f"The URL /data is not accessed directly. Try going to '/form' to submit form"
    if request.method == 'POST':
        # access the input values from the form
        form_data = request.form.to_dict()

        # run the dictionary from the form through the modeling function
        response_string = pro_predict_formver.predict_from_form(form_data)

        # pass the modeling function response string to the page template
        return render_template('data.html',response_string = response_string)
 
 
app.run(host='localhost', port=5000)