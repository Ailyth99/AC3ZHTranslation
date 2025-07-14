# infrid/ac3es-tools
FROM python:3.10-bullseye

RUN mkdir -p /opt/ac3es-tools \
    && cd /opt/ac3es-tools

ADD ac3es /opt/ac3es-tools/ac3es
ADD ac3es.spec /opt/ac3es-tools
ADD setup.py /opt/ac3es-tools

SHELL ["/bin/bash", "-c"]

RUN cd /opt/ac3es-tools \
    && python3 -m venv venv \
    && apt-get update \
    && apt-get install tini -y \
    && source venv/bin/activate \
    && pip3 install pyinstaller -q \
    && pyinstaller ac3es.spec \
    && cp dist/ac3es /usr/local/bin \
    && chmod +x /usr/local/bin \
    && cd / && rm -rf /opt/ac3es-tools

ENTRYPOINT ["tini", "--", "/usr/local/bin/ac3es"]
