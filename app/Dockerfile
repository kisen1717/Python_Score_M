


# Pythonの公式イメージをベースに
FROM python:3.9

# 作業ディレクトリを設定
WORKDIR /app

# requirements.txt をコンテナにコピー
COPY requirements.txt .

# 必要なライブラリをインストール
RUN pip install -r requirements.txt

# アプリケーションのコードをコンテナにコピー
COPY . .

# Gunicorn を使用して Flask アプリを起動
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "main:app"]

# ポート5000を公開
EXPOSE 5000








