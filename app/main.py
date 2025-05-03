import bcrypt
import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from free import handle_free  # ←追加
from admin import admin_search  # ←追加
from jansou import insert_jansou  # ←追加


app = Flask(__name__) 
app.secret_key = 'your_secret_key'

# ログインマネージャーの設定
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# MySQL 設定（環境変数がない場合はデフォルトを使用）
app.config['MYSQL_HOST'] = os.getenv('DB_HOST', 'localhost')
app.config['MYSQL_USER'] = os.getenv('DB_USER', 'user')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD', 'password')
app.config['MYSQL_DB'] = os.getenv('DB_NAME', 'mahjong')

mysql = MySQL(app)

# ユーザークラス
class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def get_id(self):
        return str(self.id)  # Flask-Loginはstr型のIDを期待する

# セッションからユーザーを復元
@login_manager.user_loader
def load_user(user_id):
    cursor = mysql.connection.cursor()
    query = "SELECT id, username FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    user_data = cursor.fetchone()
    cursor.close()

    if user_data:
        return User(user_data[0], user_data[1])
    return None

# ログイン画面
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cursor = mysql.connection.cursor()
        query = "SELECT id, username, password FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        user = cursor.fetchone()
        cursor.close()

        if user and password == user[2]:  # 本来はハッシュで比較すべき
            user_obj = User(user[0], user[1])
            login_user(user_obj)
            return redirect(url_for("home"))
        else:
            flash("ユーザー名またはパスワードが違います", "error")
    
    return render_template("login.html")

# ログアウト
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ホームページ
@app.route("/")
@login_required
def home():
    return render_template("home.html", username=current_user.username)

# フリーのページ
@app.route("/free", methods=["GET", "POST"])
@login_required
def free():
    if request.method == "POST":
        # フォームから送信されたusenameを変数に格納
        user = current_user.username  
    return handle_free(mysql)  # ← free.py の関数を呼ぶ
    
    return render_template("free.html", username=current_user.username)

#管理画面
@app.route("/admin", methods=["GET", "POST"])
@login_required
def admin():
    return admin_search(mysql)
    #return render_template("admin.html", username=current_user.username)
    
#雀荘登録画面
@app.route("/jansou", methods=["GET", "POST"])
@login_required
def jansou():
    user = current_user.username
    return insert_jansou(mysql)
    #return render_template("admin.html", username=current_user.username)

    
#いじらない
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
