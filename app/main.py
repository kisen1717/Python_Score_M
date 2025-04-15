import bcrypt
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # セッションやフラッシュメッセージのために必要です

login_manager = LoginManager()
login_manager.init_app(app)


# MySQLの設定
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'db')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'user')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'password')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'mahjong')

mysql = MySQL(app)

class User(UserMixin):
    def __init__(self, id, name):
        self.id = id
        self.name = name

@login_manager.user_loader
def load_user(user_id):
    # MySQLからユーザー情報を取得
    cursor = mysql.connection.cursor()
    query = "SELECT username, name FROM users WHERE username = %s"
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()
    cursor.close()
    
    if user_data:
        return User(user_data[0], user_data[1])  # ユーザーIDと名前を設定
    return None


# ログインページ
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        # MySQLデータベースに接続
        cursor = mysql.connection.cursor()

         # SQLクエリでユーザー情報を取得
        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))  # プレースホルダを使ってSQLインジェクションを防止
        user = cursor.fetchone()

        if user:  # ユーザーが存在すればホームページにリダイレクト
            user_obj = User(user[0], user[1])  # DB から取得したユーザー情報をUserクラスに設定
            login_user(user_obj)  # ユーザーをログイン状態にする
            return redirect(url_for("home"))
        else:
            flash("ユーザー名、パスワードを再入力してください", "error")
        
        cursor.close()
    
    return render_template("login.html")

# ログアウト
@app.route("/logout")
@login_required
def logout():
    logout_user()  # ユーザーのセッションを削除
    return redirect(url_for("home"))  # ログアウト後にホームページへリダイレクト

# ホームページ
@app.route("/")
@login_required  # ログインが必要なページ
def home():
    print(f"Current User: {current_user}")  # デバッグ用
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
