# free.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

# 一局ごと登録処理
def handle_free(mysql):
    
    cursor = mysql.connection.cursor()

    # ユーザーの雀荘リスト取得
    user = current_user.username
    cursor.execute("SELECT id, name FROM free_jannsou WHERE username = %s", (user,))
    jannsou_list = cursor.fetchall()  # → [(1, '○○荘'), (2, '△△荘')]

    if request.method == "POST":
        rank = request.form["rank"]
        jannsou_id = request.form["jannsou"]  # 選択された雀荘のIDを取得
        user = current_user.username

        # free_results_all にデータを挿入
        query = "INSERT INTO free_results_all (username, juni, jansou) VALUES (%s, %s, %s)"
        cursor.execute(query, (user, rank, jannsou_id))
        mysql.connection.commit()
        flash("登録完了", "success")
        return redirect(url_for("free"))

    cursor.close()
    return render_template("free.html", username=current_user.username, jannsou_list=jannsou_list)
