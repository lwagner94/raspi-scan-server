FROM debian:buster-slim

RUN apt update && apt install -y --no-install-recommends sane-utils scanbd python3-sh imagemagick sudo libtiff-tools
COPY files/scanbd.conf /etc/scanbd/scanbd.conf
COPY files/dispatch.script /etc/scanbd/dispatch.script
COPY files/scan.py /usr/local/bin/scan.py
RUN useradd -d /scan -u 10000 -G scanner scan
RUN chmod +x /etc/scanbd/dispatch.script /usr/local/bin/scan.py


CMD ["scanbd", "-f"]