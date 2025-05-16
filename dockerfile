# Use Debian bookworm as base (ARM compatible).
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
COPY . /home/pi/LepmonOS

# Copy startup script to /opt and make it executable.
COPY LepmonOS_start.sh /opt/LepmonOS_start.sh
RUN chmod +x /opt/LepmonOS_start.sh

# Set the working directory.
WORKDIR /home/pi/LepmonOS

# Run the startup script by default.
CMD ["/opt/LepmonOS_start.sh"]