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
import lzma
import tempfile
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)


# Specify the paths to the local zip files
model_compressed = os.environ.get('MODEL_XZ_FILE')
# model_compressed = 'compressed_amazon_fashion_overall_score_generator_model_3.xz'
print("MODEL_XZ_FILE:", os.getenv("MODEL_XZ_FILE"))
tfidf_file = os.environ.get('TFIDF_FILE')
# tfidf_file = 'tfidf_vectorizer_3.pkl'
tfidf_zip = os.environ.get('TFIDF_ZIP')
# tfidf_zip = 'tfidf_vectorizer_3.pkl.zip'


# Path of volume to be created
extracted_dir = os.environ.get('VOLUME_FILES_PATH')
# extracted_dir = '/app/model_files'
print(f"extracted_dir: {extracted_dir}")

model_compressed_file = os.path.join(extracted_dir, model_compressed)
# model_zip_file = os.path.join(extracted_dir, model_zip)
vectorizer_zip_file = os.path.join(extracted_dir, tfidf_zip)
print('done with file naming')
print(f"os list: {os.listdir(extracted_dir)}");

# Placeholder for the loaded model
loaded_model = None
tfidf_vectorizer = None

def create_model():
    global loaded_model
    global tfidf_vectorizer
    
    
    # decompress the model file
    with lzma.open(model_compressed_file, 'rb') as compressed_file:
        model_content = compressed_file.read()

    # Save the model content to a temporary file
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        temp_file.write(model_content)
        temp_file_path = temp_file.name

    print('done loading model')
    print(f"os list: {os.listdir(extracted_dir)}");

    # Load the model using joblib
    loaded_model = joblib.load(temp_file_path)

    print("Model has been loaded successfully.")

    #----------------

    print(f"vectorizer_zip_file: {vectorizer_zip_file}")
    # # Unzip the vectorizer zip file
    with zipfile.ZipFile(vectorizer_zip_file, 'r') as zip_ref:
        zip_ref.extractall(extracted_dir)

    print(f"os list: {os.listdir(extracted_dir)}");
    # # Load the model file from the extracted directory
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

        # Transform the text column
        new_text_tfidf = tfidf_vectorizer.transform([reviews_cleaned])

        # # Predict on the new data
        new_prediction = loaded_model.predict(new_text_tfidf)

        print(new_text_tfidf)
        
        return render_template('index.html', prediction=new_prediction)
    except Exception as e:
        error_message = str(e)
        return render_template('error.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)