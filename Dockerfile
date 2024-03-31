FROM python:3.9
MAINTAINER eilhyo
COPY pip.conf /root/.pip/pip.conf
RUN mkdir -p /var/www/html/mysite4
WORKDIR /var/www/html/mysite4
ADD . /var/www/html/mysite4
# RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt
RUN sed -i 's/\r//' ./start.sh
RUN chmod +x ./start.sh 

# 设置容器启动时执行的命令和参数
CMD ["./start.sh"]