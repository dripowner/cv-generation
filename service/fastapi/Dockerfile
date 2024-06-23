FROM nvidia/cuda:12.3.1-base-ubuntu22.04

WORKDIR /app

COPY requirements.txt .

RUN apt update -y && apt install -y python3.11 python3-pip

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y

RUN pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

RUN pip3 install --no-cache-dir -r requirements.txt

# COPY main.py .

# ADD weights/add_full_sft_all_clear /app/weights/add_full_sft_all_clear

WORKDIR /app/files

CMD ["python3", "main.py"]