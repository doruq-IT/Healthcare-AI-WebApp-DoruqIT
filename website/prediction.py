from flask import Blueprint, render_template, request, send_from_directory
from .app_functions import pred, ValuePredictor, model 
import os
import time
import tempfile
from werkzeug.utils import secure_filename

prediction = Blueprint('prediction', __name__)

@prediction.route('/predict', methods=["POST", 'GET'])
def predict():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        
        
        print("Girdi verileri: ", to_predict_list)

        print("Girdi verilerinin uzunluğu: ", len(to_predict_list))

        try:
            to_predict_list = list(map(float, to_predict_list))
            print("İşlenmiş girdi verileri: ", to_predict_list)
        except ValueError as e:
            print("Girdi verileri dönüştürme hatası: ", e)
            return "Hatalı girdi verileri", 400

        result, page = ValuePredictor(to_predict_list)
        
        print("Tahmin sonucu: ", result, "Sayfa: ", page)

        return render_template("result.html", prediction=result, page=page)
    else:
        return render_template('base.html')

@prediction.route('/upload', methods=['POST','GET'])
def upload_file():
    if request.method == "POST":
        file = request.files["file"]
        if file:
            filename = secure_filename(file.filename)
            file_path = tempfile.mktemp()

            file.save(file_path)

            indices = {0: 'Normal', 1: 'Pneumonia'}
            result = pred(file_path, model)

            os.remove(file_path)

            if result > 0.5:
                label = indices[1]
                accuracy = result * 100
            else:
                label = indices[0]
                accuracy = 100 - result
            return render_template('deep_pred.html', image_file_name=filename, label=label, accuracy=accuracy)
        else:
            return render_template('pneumonia.html', error="Dosya yüklenemedi veya hatalı.")
    else:
        return render_template('pneumonia.html', title='Pneumonia Disease')



@prediction.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory('uploads', filename)
