本项目基于django、uwsgi、sqlite构建，支持docker部署，环境要求linux系统。

docker build -t mydjangoproject:v1 .

docker run -dp 8001:8001 --name mydjangoproject mydjangoproject:v1
