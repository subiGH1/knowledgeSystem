# 安定版の Python 3.12 を使用
FROM python:3.12-slim

# システムレベルで日本語（UTF-8）を扱えるように設定
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONIOENCODING=utf-8

# 作業ディレクトリの設定
WORKDIR /app

# SQLite のバージョン問題を解決するためのライブラリを含め、必要なパッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 依存ライブラリのインストール
RUN pip install --no-cache-dir \
    langchain \
    langchain-community \
    langchain-google-genai \
    langchain-huggingface \
    langchain-chroma \
    pypdf \
    sentence-transformers \
    pysqlite3-binary

# コードをコピー（docker-compose の volume で上書きされますがビルド用にも必要）
COPY . .

# 実行コマンド
CMD ["python", "1.py"]