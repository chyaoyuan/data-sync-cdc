FROM python:3.9

WORKDIR /opt

COPY ./requirement.txt ./requirement.txt


RUN pip install -r requirement.txt -i https://mirrors.aliyun.com/pypi/simple

COPY . .