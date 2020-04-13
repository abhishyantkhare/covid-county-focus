FROM ubuntu

# Install curl
RUN apt update -y && apt upgrade -y
RUN apt install curl -y

# Install python3
RUN apt-get install python3 -y

# Install pip
RUN apt-get install python3-distutils -y
RUN curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
RUN python3 get-pip.py

COPY ./ /backend
WORKDIR /backend


# Install dependencies
RUN pip3 install -r requirements.txt


CMD gunicorn --bind 0.0.0.0:8080  --access-logfile /logs/access_log --error-logfile /logs/error_log --timeout 60 app



