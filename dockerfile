# Use an Ubuntu base image for Raspberry Pi (ARM64)
# build it using `docker buildx build --platform linux/arm64 -t lepmonos-arm64 .`
# run privileged container using `docker run --privileged -it --rm -v /dev:/dev -v /tmp:/tmp -v /home/pi/LepmonOS:/home/pi/LepmonOS lepmonos-arm64`
FROM debian:bookworm

RUN apt update && apt install -y --no-install-recommends gnupg

RUN echo "deb http://archive.raspberrypi.org/debian/ bookworm main" > /etc/apt/sources.list.d/raspi.list \
  && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E

RUN apt update && apt -y upgrade

RUN apt update && apt install -y --no-install-recommends \
         python3-pip \
         python3-picamera2 \
     && apt-get clean \
     && apt-get autoremove \
     && rm -rf /var/cache/apt/archives/* \
     && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Copy and install Python dependencies
RUN pip install --break-system-packages --no-cache-dir -r requirements.txt

# mkdir and then copy files into /home/pi/LepmonOS 
RUN mkdir -p /home/pi/LepmonOS
COPY . /home/pi/LepmonOS

# Set the working directory
WORKDIR /home/pi/LepmonOS

# Copy startup script and allow execution
COPY LepmonOS_start.sh /opt/LepmonOS_start.sh
RUN chmod +x /opt/LepmonOS_start.sh

# Entrypoint starts the script
CMD ["/opt/LepmonOS_start.sh"]