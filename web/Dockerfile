FROM python:3
WORKDIR /usr/src/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN apt install wget
RUN wget http://magnitude.plasticity.ai/word2vec/GoogleNews-vectors-negative300.magnitude
CMD ["python", "app.py"]