FROM python:3.9-slim-buster

ENV QDRANT_HOST "qdrant"
ENV QDRANT_PORT 6333
ENV DATA_DIR "/data"

RUN apt-get update \
    && apt-get install -y wget \
    && rm -rf /var/lib/apt/lists/*

# Download the image assets (wget is used on purpose, as file added with ADD command
# will be downloaded every time the image is built)
WORKDIR $DATA_DIR
RUN wget --no-verbose --show-progress --progress=dot:giga \
    https://storage.googleapis.com/demo-hnm/h-and-m-images.tar.gz
RUN tar zxf h-and-m-images.tar.gz
RUN rm h-and-m-images.tar.gz

# Install python dependencies
COPY requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt --extra-index-url https://download.pytorch.org/whl/cpu

# Run the Streamlit application
WORKDIR /app
COPY . /app
EXPOSE 8501
ENTRYPOINT ["streamlit", "run", "demo.py"]
