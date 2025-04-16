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
        rank = request.form.get("rank")
        jannsou_name = request.form.get("jannsou")  # 選択された雀荘の名前を取得

        # 入力チェック：rank と jannsou_name が選択されていなければエラーメッセージを表示
        if not rank or not jannsou_name:
            flash("着順または雀荘を選択してください", "error")
            return redirect(url_for("free"))
        
        user = current_user.username

        # free_results_all にデータを挿入（名前を保存）
        query = "INSERT INTO free_results_all (username, juni, jansou) VALUES (%s, %s, %s)"
        cursor.execute(query, (user, rank, jannsou_name))
        mysql.connection.commit()
        flash("登録完了", "success")
        return redirect(url_for("free"))

    cursor.close()
    return render_template("free.html", username=current_user.username, jannsou_list=jannsou_list)
