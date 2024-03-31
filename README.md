本项目基于django、uwsgi、sqlite构建，支持docker部署，环境要求linux系统。
docker build -t mydjangoproject:v1 .
docker run -p 8000:8000 --name mydjangoproject mydjangoproject:v1