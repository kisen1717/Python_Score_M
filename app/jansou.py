from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

@login_required
def insert_jansou(mysql):
    if request.method == "POST":
        jansou_name = request.form.get("jansou")
        user = current_user.username

        if not jansou_name:
            flash("雀荘名を入力してください。")
            return redirect(url_for("insert_jansou"))  # ルート名に合わせて変更

        cursor = mysql.connection.cursor()
        query = """
            INSERT INTO free_jannsou (username, name)
            VALUES (%s, %s);
        """
        cursor.execute(query, (user, jansou_name))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for("jansou"))  # 成績画面など適切なリダイレクト先に変更

    # GETリクエスト時は登録画面を表示
    return render_template("jansou.html")
