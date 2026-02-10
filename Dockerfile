# Build stage
FROM python:3.13-slim AS builder

RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    make \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY pyproject.toml requirements.txt ./
COPY telegram_video_repurpose_bot/ telegram_video_repurpose_bot/

RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir --prefix=/install .

# Final stage
FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY --from=builder /install /usr/local

WORKDIR /code
COPY app/ ./

CMD exec python bot_start.py -c ${CONFIG_FILE:-conf/config.ini}
