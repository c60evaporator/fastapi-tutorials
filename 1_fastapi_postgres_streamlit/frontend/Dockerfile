# Python公式イメージをベースとして使用
FROM python:3.11-slim

# 8501番ポートを公開
EXPOSE 8501

WORKDIR /app

# 必要パッケージをインストール
RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# 必要なPythonライブラリをrequirements.txtに基づきインストール
# (RUNはマウント前に実行されるのでCOPYが必要 https://cyanotes.com/docker-compose-%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%80%81dockerfile%E4%B8%8A%E3%81%AE-requirements-txt-%E3%82%92-pip-install-%E3%81%97%E3%82%88%E3%81%86%E3%81%A8%E3%81%97%E3%81%9F%E3%82%89%E3%80%81)
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# Streamlitを起動
ENTRYPOINT ["streamlit", "run", "main.py", "--server.port=8501", "--server.address=0.0.0.0"]