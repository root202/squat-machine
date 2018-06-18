FROM ubuntu:16.04
RUN apt update
RUN apt upgrade -y
RUN apt install -y --fix-missing python3 python3-dev python3-venv build-essential
RUN mkdir -p /opt/app
WORKDIR /opt/app
ADD ./exec.sh /opt/app/
ADD ./app.py /opt/app/
ADD ./requirements.txt /opt/app/
ADD ./settings.py /opt/app/
ADD ./install.sh /opt/app/
RUN mkdir -p /opt/app/logs
RUN python3 -m venv venv
RUN bash /opt/app/install.sh

ENTRYPOINT ["bash", "/opt/app/exec.sh"]