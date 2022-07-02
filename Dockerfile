FROM ubuntu:focal
MAINTAINER Yingming
RUN apt-get update \
    && apt-get install -y openjdk-8-jre
RUN apt-get update \
    && apt-get install software-properties-common -y
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update
RUN apt-get install python3.6 -y

RUN cp /etc/apt/sources.list /etc/apt/sources.list.bak
RUN echo > /etc/apt/sources.list
RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse \n\
deb http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse \n\
deb http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse \n\
deb http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse \n\
deb http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse \n\
deb-src http://mirrors.aliyun.com/ubuntu/ bionic main restricted universe multiverse \n\
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-security main restricted universe multiverse \n\
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-updates main restricted universe multiverse \n\
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-proposed main restricted universe multiverse \n\
deb-src http://mirrors.aliyun.com/ubuntu/ bionic-backports main restricted universe multiverse'\
 >> /etc/apt/sources.list


RUN apt-get update \
    && apt-get install -y python3-pip
WORKDIR /app
ADD target/SoundAI-1.0-SNAPSHOT.jar app.jar
ADD sound_ai sound_ai
RUN pip3 install -U pip setuptools -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
RUN pip3 install -r sound_ai/requirements.txt -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com
ADD start.sh start.sh
RUN chmod a+x start.sh
EXPOSE 8080
ENTRYPOINT ["./start.sh"]
