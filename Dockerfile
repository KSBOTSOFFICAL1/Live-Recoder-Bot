# 1. Base Image (Python)
FROM python:3.10-slim-buster

# 2. Working Directory सेट करें
WORKDIR /app

# 3. सबसे पहले सिस्टम को अपडेट करके FFMPEG और ज़रूरी पैकेजेस इंस्टॉल करें
RUN apt-get update && apt-get upgrade -y && \
    apt-get install -y ffmpeg git libsm6 libxext6 && \
    rm -rf /var/lib/apt/lists/*

# 4. requirements.txt को कॉपी करके लाइब्रेरीज़ इंस्टॉल करें
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 5. बाकी का सारा कोड कंटेनर में कॉपी करें
COPY . .

# 6. बॉट को चालू करने की सही कमांड (main.py के हिसाब से)
CMD ["python3", "main.py"]
