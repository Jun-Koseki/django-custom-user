FROM ubuntu:latest

ENV PYTHONUNBUFFERED 1
ENV PYTHONIOENCODING utf-8

ENV HOME /root
ENV DEPLOY_DIR ${HOME}/myprojects

RUN apt update

RUN apt install -y wget \
    build-essential \
    zlib1g-dev \
    libssl-dev \
    libsqlite3-dev

WORKDIR ${HOME}
RUN wget https://www.python.org/ftp/python/3.9.1/Python-3.9.1.tgz \
    && tar zxf Python-3.9.1.tgz \
    && cd Python-3.9.1 \
    && ./configure --enable-optimizations \
    && make altinstall

RUN update-alternatives --install /usr/local/bin/python3 python3 /usr/local/bin/python3.9 1
RUN update-alternatives --install /usr/local/bin/pip3 pip3 /usr/local/bin/pip3.9 1
RUN pip3 install -U pip

# Install other requisites
RUN apt install -y vim

RUN mkdir -p ${DEPLOY_DIR}
WORKDIR ${DEPLOY_DIR}

# Install packages for project
ADD requirements/base.txt requirements/base.txt
RUN pip3 install -r requirements/base.txt

# Set entrypoint
ENTRYPOINT ["/bin/bash", "initialize.sh"]