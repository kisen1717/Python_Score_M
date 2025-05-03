from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

def insert_jansou(mysql):
    cursor = mysql.connection.cursor()
    user = current_user.username

    # ユーザーの雀荘リスト取得
    cursor.execute("SELECT id, name FROM free_jannsou WHERE username = %s", (user,))
    jannsou_list = cursor.fetchall()

    avg = None
    selected_jannsou = None
    start_date = end_date = ""
    results = []

    if request.method == "POST":
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        selected_jannsou = request.form.get("jansou")
        
        print("start_date:", start_date)
        print("end_date:", end_date)
        print("selected_jannsou:", selected_jannsou)

        if not start_date or not end_date or not selected_jannsou:
            flash("日付または雀荘を選択してください", "error")
            return redirect(url_for("admin"))

        query = """
                    SELECT juni FROM free_results_all 
                    WHERE username = %s AND jansou = %s 
                    AND play_date BETWEEN %s AND %s
                """
        
        
        cursor.execute(query, (user, selected_jannsou, start_date, end_date))
        rows = cursor.fetchall()
        juni_list = [row[0] for row in rows]

        if juni_list:
            avg = sum(juni_list) / len(juni_list)
            results = [{"juni": j, "jansou": selected_jannsou} for j in juni_list]
        else:
            flash("該当するデータがありません", "info")

    cursor.close()

    return render_template(
        "admin.html",
        username=user,
        jannsou_list=jannsou_list,
        avg=avg,
        selected_jannsou=selected_jannsou,
        start_date=start_date,
        end_date=end_date,
        results=results,
        
    )
