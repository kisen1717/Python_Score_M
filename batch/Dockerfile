# ベースイメージ
FROM python:3.10

# 作業ディレクトリを設定
WORKDIR /batch

# 必要なファイルをコピー
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# バッチスクリプトをコピー
COPY . .

# バッチ処理を実行
CMD ["python", "batch.py"]
