# Dockerfile (Final Version)
FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

FROM python:3.10-slim as runtime

WORKDIR /app
# Copy from builder and app files
COPY --from=builder /root/.local /root/.local
COPY . .

# Set environment and permissions
ENV PATH=/root/.local/bin:$PATH \
    PYTHONPATH=/app

RUN chmod +x startup.sh

CMD ["./startup.sh"]