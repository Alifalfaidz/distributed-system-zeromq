# Docker Task C: Python 3.9 sesuai README dosen
FROM python:3.9-slim

WORKDIR /app
ENV PYTHONUNBUFFERED=1

COPY . .

# Dependensi mengikuti environment lokal yang telah berhasil dipakai.
RUN python -m pip install --no-cache-dir pyzmq==27.2.0 numpy==2.0.2

# Di Docker, 'localhost' hanya menunjuk ke container itu sendiri.
# Ganti alamat koneksi PADA IMAGE, tanpa mengubah file Python di MacBook.
RUN sed -i 's|tcp://localhost:5555|tcp://distributor:5555|g' worker_1.py worker_2.py \
    && sed -i \
       -e 's|tcp://localhost:5556|tcp://worker1:5556|g' \
       -e 's|tcp://localhost:5557|tcp://worker2:5557|g' \
       tasks_collector_publisher.py \
    && sed -i 's|tcp://localhost:5558|tcp://collector:5558|g' \
       sum_subscriber.py mut_subscriber.py div_subscriber.py

# Pastikan struktur port dari file yang sudah kamu kerjakan masih cocok.
RUN grep -q 'tcp://distributor:5555' worker_1.py \
    && grep -q 'tcp://distributor:5555' worker_2.py \
    && grep -q 'tcp://worker1:5556' tasks_collector_publisher.py \
    && grep -q 'tcp://worker2:5557' tasks_collector_publisher.py \
    && grep -q 'tcp://collector:5558' sum_subscriber.py \
    && grep -q 'tcp://collector:5558' mut_subscriber.py \
    && grep -q 'tcp://collector:5558' div_subscriber.py
