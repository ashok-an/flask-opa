######
FROM python:3.10-slim

RUN groupadd -g 1000 app && useradd -u 1000 -g 1000 app

WORKDIR /usr/local/bin
RUN apt-get update \
&& apt-get install -y wget \
&& apt-get clean \
&& wget https://github.com/open-policy-agent/opa/releases/download/v0.60.0/opa_linux_arm64_static \
&& apt-get remove -y wget \
&& mv /usr/local/bin/opa_linux_arm64_static /usr/local/bin/opa \
&& chmod 755 /usr/local/bin/opa

WORKDIR /usr/src/app
COPY . .
RUN chmod 755 /usr/src/app/run.sh \
&& pip install --no-cache-dir -r requirements.txt

EXPOSE 12345
EXPOSE 8181

USER app
CMD [ "/usr/src/app/run.sh" ]

