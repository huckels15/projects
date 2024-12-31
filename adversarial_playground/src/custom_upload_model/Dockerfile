FROM python:3.9-slim

ENV PYENV_SHELL=/bin/bash
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=UTC

RUN set -ex; \
    apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --no-install-recommends \
        ffmpeg \
        libavcodec-extra \
        vim \
        git \
        libgl1-mesa-glx \
        build-essential \
        python3-pip \
        python3-dev \
        lsb-release \
        software-properties-common \
        apt-transport-https \
        ca-certificates \
        gnupg2 \
        gnupg-agent \
        curl \
        openssh-client \
        libnss3 \
        libcurl4 && \
    for i in $(seq 1 8); do mkdir -p "/usr/share/man/man${i}"; done && \
    curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - && \
    echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list && \
    curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add - && \
    echo "deb http://packages.cloud.google.com/apt gcsfuse-bionic main" > /etc/apt/sources.list.d/gcsfuse.list && \
    apt-get update && \
    apt-get install -y \
        gcsfuse \
        google-cloud-sdk && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    pip install --no-cache-dir --upgrade pip && \
    useradd -ms /bin/bash app -d /home/app -u 1000 -p "$(openssl passwd -1 Passw0rd)" && \
    mkdir -p /app && \
    chown app:app /app

RUN mkdir -p /mnt/gcs_data && chown app:app /mnt/gcs_data

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app
RUN chmod +x /app/docker-entrypoint.sh

EXPOSE 8000

# ENTRYPOINT ["/bin/bash"]
ENTRYPOINT ["./docker-entrypoint.sh"]