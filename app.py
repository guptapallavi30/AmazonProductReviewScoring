import atexit
from flask import Flask, redirect, url_for, request, render_template, jsonify
import threading
# from tensorflow.keras.models import load_model
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.sparse import hstack
import zipfile
import os
import shutil


app = Flask(__name__)

# Specify the paths to the local zip files
model_file = os.environ.get('MODEL_FILE')
model_zip = os.environ.get('MODEL_ZIP')
tfidf_file = os.environ.get('TFIDF_FILE')
tfidf_zip = os.environ.get('TFIDF_ZIP')


# Path of volume to be created
extracted_dir = os.environ.get('VOLUME_FILES_PATH')

model_zip_file = os.path.join(extracted_dir, model_zip)
vectorizer_zip_file = os.path.join(extracted_dir, tfidf_zip)


# Placeholder for the loaded model
loaded_model = None
tfidf_vectorizer = None

def create_model():
    global loaded_model
    global tfidf_vectorizer
    
    print(f"model_zip_file: {model_zip_file}")
    # Unzip the model zip file
    with zipfile.ZipFile(model_zip_file, 'r') as zip_ref:
        print("begin unzipping")
        zip_ref.extractall(extracted_dir)
    print("done unzipping!")
    print(f"os list: {os.listdir(extracted_dir)}");
    # # Load the model file from the extracted directory
    # model_file_to_load = os.listdir(extracted_dir)[0]
    model_path = os.path.join(extracted_dir, model_file)
    
    print(model_path);
    # # Load the model using joblib
    loaded_model = joblib.load(model_path)

    # # print(os.path.join(extracted_dir, model_file_to_load));
    print("Model has been loaded successfully.")


    print(f"vectorizer_zip_file: {vectorizer_zip_file}")
    # # Unzip the vectorizer zip file
    with zipfile.ZipFile(vectorizer_zip_file, 'r') as zip_ref:
        zip_ref.extractall(extracted_dir)

    print(f"os list: {os.listdir(extracted_dir)}");
    # # Load the model file from the extracted directory
    # tfidf_file_to_load = os.listdir(extracted_dir)[0]
    tfidf_path = os.path.join(extracted_dir, tfidf_file)
    
    print(tfidf_path);
    # # Load the model using joblib
    tfidf_vectorizer = joblib.load(tfidf_path)

    print("tfidf_vectorizer has been loaded successfully.")

# Create and start a thread to load the model
model_thread = threading.Thread(target=create_model)
model_thread.start()

@app.route('/')
def hello():
    print("Hello, Flask! Testing")
    # return redirect(url_for('login'));
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input from user
        reviews_cleaned = request.form['reviewsCleaned']
        vote_classification = 0
        verified_encoded = 0

        # Transform the text column
        new_text_tfidf = tfidf_vectorizer.transform([reviews_cleaned])

        # # Combine TF-IDF features with numerical features for the new data
        new_numerical = [[vote_classification, verified_encoded]]
        new_combined = hstack([new_text_tfidf, new_numerical])

        # # Predict on the new data
        new_prediction = loaded_model.predict(new_combined)

        print(new_text_tfidf)
        print(new_numerical)
        print(new_combined)

        # return render_template('index.html', prediction=new_prediction[0])  # Rendering prediction on a result page
        return render_template('index.html', prediction=new_prediction)
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)