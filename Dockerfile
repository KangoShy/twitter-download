FROM python:3.12.8

WORKDIR /usr/src/app
ENV PROFILE pro

COPY requirements.txt ./
RUN pip install --no-cache-dir -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt
ENV PYTHONPATH /usr/src/app

COPY . .

CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0"]