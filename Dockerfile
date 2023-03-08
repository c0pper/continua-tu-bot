FROM python:3.10
WORKDIR /app
COPY requirements.txt requirements.txt

RUN apt-get install -y -q curl
RUN curl https://sh.rustup.rs -sSf | sh -s -- -y
# Add .cargo/bin to PATH
ENV PATH="/root/.cargo/bin:${PATH}"

# Check cargo is visible
RUN cargo --help
RUN pip3 install -r requirements.txt
COPY . .
CMD [ "python3", "./main.py"]