from flask import Blueprint, request, redirect, url_for, flash
from .models import Messages
from . import db
import re
import os
from datetime import datetime

messages = Blueprint('messages', __name__)

def get_user_ip():
    if "X-Forwarded-For" in request.headers:
        x_forwarded_for = request.headers.get('X-Forwarded-For')
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.remote_addr
    return ip

@messages.route("/msg", methods=['GET', 'POST'])
def msg():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message_text = request.form.get('message')
        if not name or not email or not message_text:
            flash('All fields are required.', 'error')
            return redirect(url_for('views.home') + '#contact-form') 
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            flash('Invalid email address.', 'error')
            return redirect(url_for('views.home') + '#contact-form') 

        user_ip = get_user_ip()

        new_message = Messages(name=name, email=email, messages=message_text, user_ip=user_ip) 
        db.session.add(new_message)
        db.session.commit()

        return redirect(url_for('views.home'))
    else:
        return redirect(url_for('views.home'))

