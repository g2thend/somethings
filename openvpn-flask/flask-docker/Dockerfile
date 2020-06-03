FROM tiangolo/uwsgi-nginx-flask:python3.8
COPY ./openvpn  /app
RUN pip install -r /app/requirement.txt -i  https://pypi.tuna.tsinghua.edu.cn/simple some-package --no-cache-dir
