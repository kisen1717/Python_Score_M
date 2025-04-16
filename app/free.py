# free.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

#一局ごと登録処理
def handle_free(mysql):
    if request.method == "POST":
        rank = request.form["rank"]
        user = current_user.username

        cursor = mysql.connection.cursor()
        query = "INSERT INTO free_results_all (username, juni) VALUES (%s, %s)"
        cursor.execute(query, (user, rank))
        mysql.connection.commit()
        cursor.close()
        flash("登録完了", "success")

    return render_template("free.html", username=current_user.username)
