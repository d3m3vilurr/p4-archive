FROM library/python:2.7-slim

WORKDIR /opt

RUN set -x \
    && cd /etc/apt \
    && sed -i 's/deb.debian.org/ftp.kaist.ac.kr/g' sources.list \
    && sed -i 's/security.debian.org/ftp.kaist.ac.kr\/debian-security/g' sources.list \
    && builds='build-essential curl libssl-dev' \
    && apt-get update && apt-get install -y $builds --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* \
    && curl http://cdist2.perforce.com/perforce/r15.1/bin.linux26x86_64/p4 -o /usr/local/bin/p4 \
    && chmod 755 /usr/local/bin/p4 \
    && cd /opt \
    && curl -L https://github.com/d3m3vilurr/p4-archive/raw/master/requirement.txt -o requirement.txt \
    && pip install -r requirement.txt \
    && apt-get purge -y --auto-remove build-essential

COPY archive.py /opt/archive.py

CMD ["python", "archive.py"]
