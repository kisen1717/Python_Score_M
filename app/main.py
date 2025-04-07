import bcrypt
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッションやフラッシュメッセージのために必要です

# MySQLの設定
app.config['MYSQL_HOST'] = 'db'  # MySQLサーバーのホスト
app.config['MYSQL_USER'] = 'user'  # MySQLのユーザー名
app.config['MYSQL_PASSWORD'] = 'password'  # MySQLのパスワード
app.config['MYSQL_DB'] = 'mahjong'  # データベース名

mysql = MySQL(app)

# ログインページ
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # MySQLデータベースに接続
        conn = mysql.connect()
        cursor = conn.cursor()

        # SQLクエリでユーザー情報を取得
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))  # プレースホルダを使ってSQLインジェクションを防止
        user = cursor.fetchone()

        if user:  # ユーザーが存在すればホームページにリダイレクト
            return redirect(url_for("home"))
        else:
            flash("Invalid username or password!", "error")
        
        cursor.close()
        conn.close()
    
    return render_template("login.html")

# ホームページ
@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
