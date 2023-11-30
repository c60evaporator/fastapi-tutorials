# FastAPI公式イメージを使用 (参考 https://fastapi.tiangolo.com/ja/deployment/docker/)
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

# 必要なPythonライブラリをrequirements.txtに基づきインストール 
# (RUNはマウント前に実行されるのでCOPYが必要 https://cyanotes.com/docker-compose-%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%80%81dockerfile%E4%B8%8A%E3%81%AE-requirements-txt-%E3%82%92-pip-install-%E3%81%97%E3%82%88%E3%81%86%E3%81%A8%E3%81%97%E3%81%9F%E3%82%89%E3%80%81)
WORKDIR /app
COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

# 8000番ポートをFrontend向けにに公開
EXPOSE 8000

# UvicornとFastAPIでAPI公開 (appフォルダのmain.pyの中のappインスタンスを実行)
CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]