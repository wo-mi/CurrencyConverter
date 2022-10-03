FROM python:3.9
WORKDIR /converter
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
RUN echo 'alias converter="python3 /converter/app.py"' >> ~/.bashrc