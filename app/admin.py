# admin.py
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

#管理画面検索
def admin_ search(mysql):
    
    cursor = mysql.connection.cursor()

# ユーザーの雀荘リスト取得
    user = current_user.username
    cursor.execute("SELECT id, name FROM free_jannsou WHERE username = %s", (user,))
    jannsou_list = cursor.fetchall() 

    if request.method == "POST":
        rank = request.form.get("rank")
        jannsou_name = request.form.get("jannsou")  # 選択された雀荘の名前を取得

        # 入力チェック：start_dateと end_dateと jannsou_name が選択されていなければエラーメッセージを表示
        if not start_date or not jannsou_name or not end_date:
            flash("日付または雀荘を選択してください", "error")
            return redirect(url_for("admin"))
        
        user = current_user.username

        # free_results_all から平均着順を算出
        query = "SELECT average_rank FROM free_results WHERE (%s, %s)"
        cursor.execute(query, (user, rank, jannsou_name))
        @mysql.connection.commit()
        @flash("登録完了", "success")
        @return redirect(url_for("free"))

    cursor.close()
    return render_template("free.html", username=current_user.username, jannsou_list=jannsou_list)