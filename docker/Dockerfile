FROM ubuntu:xenial-20180417 as base

COPY sources.list /etc/apt/sources.list
COPY get-pip.py /get-pip.py
COPY miniupnpc-1.9.20140401.tar.gz /
COPY dstrad /root/


VOLUME /root/.dstra

ENV PYTHONIOENCODING=utf-8

RUN \
 apt-get update && \
 apt-get -y install software-properties-common && \
 add-apt-repository ppa:jonathonf/python-3.6 && \
 apt-get update && \
 apt-get install -y python3.6 && \
 \
 python3.6 get-pip.py && \
 update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1 && \
 update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2 && \
 rm -rf get-pip.py && \
 \
 pip install -i http://mirrors.aliyun.com/pypi/simple --trusted-host mirrors.aliyun.com aiomysql apscheduler && \
 \
 python3 -m pip install -U https://github.com/Rapptz/discord.py/archive/rewrite.zip && \
 \
 apt-get -y install libboost-all-dev libdb++-dev make && \
 tar -xzvf miniupnpc-1.9.20140401.tar.gz && \
 cd miniupnpc-1.9.20140401 && \
 make && \
 make install && \
 cd .. && \
 rm -rf miniupnpc-1.9.20140401.tar.gz miniupnpc-1.9.20140401 && \
 apt-get -y autoremove && \
 apt-get clean && \
 echo 'alias dst=/root/dstrad' >> /root/.bashrc


FROM base as tmp

COPY trawd /root/

VOLUME /root/.traw

RUN \
     echo 'alias traw=/root/trawd' >> /root/.bashrc


