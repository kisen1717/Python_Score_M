from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

def insert_jansou(mysql):
    cursor = mysql.connection.cursor()
    user = current_user.username
    return render_template("jansou.html")
