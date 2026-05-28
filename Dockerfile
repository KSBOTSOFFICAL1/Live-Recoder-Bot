# 1. अपडेटेड बेस इमेज
FROM python:3.10-slim

# 2. वर्किंग डायरेक्टरी सेट करें
WORKDIR /app

# 3. FFMPEG, FFPROBE और बाकी ज़रूरी बाइनरीज़ इंस्टॉल करना
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg ffprobe git && \
    rm -rf /var/lib/apt/lists/*

# 4. requirements.txt कॉपी करें और लाइब्रेरीज़ इंस्टॉल करें
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# 5. अपना पूरा कोड कॉपी करें
COPY . .

# 6. बॉट की मुख्य फाइल को रन करें
CMD ["python3", "main.py"]
