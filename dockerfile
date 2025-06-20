# Use Debian bookworm as base (ARM compatible).
# build it using `docker build -t lepmonos .`
# run privileged container using `docker run --privileged -it --rm -v /dev:/dev -v /tmp:/tmp -v /home/pi/LepmonOS:/home/pi/LepmonOS lepmonos
# docker run --privileged -it --rm lepmonos:latest 
FROM debian:bookworm

# Install dev tools and Python (comments in English only).
RUN apt-get update && apt-get install -y --no-install-recommends \
  gnupg \
  apt-utils \
  build-essential \
  python3 \
  python3-distutils \
  python3-pip \
  python3-setuptools \
  python3-dev \   
  && rm -rf /var/lib/apt/lists/*

# Create a symlink so 'python' calls 'python3'.
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 1

# Add Raspberry Pi repository.
RUN echo "deb http://archive.raspberrypi.org/debian/ bookworm main" > /etc/apt/sources.list.d/raspi.list \
  && apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 82B129927FA3303E \
  && apt-get update \
  && apt-get -y upgrade \
  && apt-get install -y --no-install-recommends python3-picamera2 \
  && apt-get clean \
  && apt-get autoremove -y \
  && rm -rf /var/lib/apt/lists/*

# Copy in requirements and install with pip.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --break-system-packages --no-cache-dir -r /tmp/requirements.txt

# Copy project files into /home/pi/LepmonOS.
RUN mkdir -p /home/pi/LepmonOS

# print date to breakup layers 
RUN date
COPY . /home/pi/LepmonOS

RUN apt-get update && apt-get install -y --no-install-recommends \
  sudo

# Set the working directory.
WORKDIR /home/pi/LepmonOS

# Run the Python main script by default.
CMD ["python3", "main.py"]