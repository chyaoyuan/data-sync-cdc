FROM python:3.9

WORKDIR /opt

COPY ./requirement.txt ./requirement.txt
COPY ./packages/data_sync_packages-0.0.1-py3-none-any.whl ./data_sync_packages-0.0.1-py3-none-any.whl

RUN pip install -r requirement.txt -i https://mirrors.aliyun.com/pypi/simple \
    && pip install data_sync_packages-0.0.1-py3-none-any.whl -i https://mirrors.aliyun.com/pypi/simple
COPY . .