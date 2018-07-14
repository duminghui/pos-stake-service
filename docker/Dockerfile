FROM ubuntu:xenial-20180525

COPY sources.list /etc/apt/sources.list
COPY get-pip.py /get-pip.py
COPY dstrad /root/
COPY trawd /root/
COPY bash_aliases /root/.bash_aliases
COPY libs/usr/lib/ /usr/lib

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
 echo 'end'
CMD ["bash"]

