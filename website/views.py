from flask import Flask, Blueprint, render_template, request, redirect, url_for, flash, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from .utils import get_completion
from .models import User
from . import db

views = Blueprint('views', __name__)


@views.route('/get_answer', methods=['POST'])
def get_answer():
    data = request.get_json()
    question = data.get('question')
    answer = get_completion(question)  # utils.py'den get_completion fonksiyonunu kullan
    return jsonify({'answer': answer})

@views.route("/")
def home():
    return render_template('base.html')

@views.route("/kidney")
def kidney():
    return render_template(r'kidney_index.html')

@views.route("/kidney_form")
def kidney_form():
    return render_template(r'kidney.html')
@views.route("/liver")
def liver():
    return render_template(r'liver_index.html')

@views.route("/liver_form")
def liver_form():
    return render_template(r'liver.html')

@views.route("/heart")
def heart():
    return render_template(r'heart_index.html')

@views.route("/heart_form")
def heart_form():
    return render_template(r'heart.html')

@views.route("/stroke")
def stroke():
    return render_template(r'stroke_index.html')

@views.route("/stroke_form")
def stroke_form():
    return render_template(r'stroke.html')
@views.route("/diabete")
def diabete():
    return render_template(r'diabete_index.html')

@views.route("/diabete_form")
def diabete_form():
    return render_template(r'diabete.html')
@views.route("/pneumonia")
def pneumonia():
    return render_template(r'pneumonia_index.html')

@views.route("/pneumonia_form")
def pneumonia_form():
    return render_template(r'pneumonia.html')