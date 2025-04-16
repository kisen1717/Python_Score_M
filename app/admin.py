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
        
        #画面から日付の終わりと始まりと雀荘を取得
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
　　　　　jannsou_name = request.form.get("jannsou")
        # 入力チェック：start_dateと end_dateと jannsou_name が選択されていなければエラーメッセージを表示
        if not start_date or not jannsou_name or not end_date:
            flash("日付または雀荘を選択してください", "error")
            return redirect(url_for("admin"))
        
        user = current_user.username

        # free_results_all から平均着順を算出
            query1 = "SELECT juni FROM free_results_all WHERE username = %s AND jannsou_name = %s BETWEEN %s AND %S "
            query2 = "SELECT COUNT juni FROM free_results_all WHERE username = %s AND jannsou_name = %s "
            
        cursor.execute(query1, (user, jannsou_name, start_date, end_date))
        #計算
        
        
        
        
        
        #最後にこれ↓
        @return redirect(url_for("free"))

    cursor.close()
    return render_template("free.html", username=current_user.username, jannsou_list=jannsou_list)