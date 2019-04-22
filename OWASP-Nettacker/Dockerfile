# I didnt write these
FROM ubuntu
RUN apt update
RUN apt install -y python python-pip python-dev openssl libffi-dev musl-dev make gcc git curl librtmp* libxml2-dev libxslt-dev
WORKDIR /usr/src/owaspnettacker
RUN git clone https://github.com/zdresearch/OWASP-Nettacker.git .
RUN pip install -r requirements.txt

# entry point is the command ran with "docker run"
ENTRYPOINT ["python", "./nettacker.py"]

# CMD is the default, but whatever you add after "docker run <imagename>" will replace these
CMD ["-i", "10.0.0.44", "-m", "icmp_scan", "-o", "/root/.owasp-nettacker/results/scan_02.json"]
