
import pickle
import time as time_module
import main_constants as mc
from data_worker import DataToWorker
import zmq
import random

# Membuat context ZeroMQ
context = zmq.Context()

# Socket PULL untuk menerima data dari Distributor
pull_socket = context.socket(zmq.PULL)
pull_socket.connect("tcp://localhost:5555")

# Socket PUSH untuk mengirim data ke Collector
push_socket = context.socket(zmq.PUSH)
push_socket.bind("tcp://*:5557")


# Fungsi penjumlahan
def task_1_sum(num1: float, num2: float) -> float:
    print(f"[x] {num1} + {num2}")
    return num1 + num2


# Fungsi perkalian
def task_2_multiply(num1: float, num2: float) -> float:
    print(f"[x] {num1} x {num2}")
    return num1 * num2


# Fungsi pembagian
def task_3_division(num1: float, num2: float) -> float:
    print(f"[x] {num1} / {num2}")

    if num2 == 0:
        raise ValueError("Cannot divide by zero")

    return num1 / num2


print("Successfully connected with the server ...")
print("Waiting for tasks ...")

while True:

    # Menerima pesan dari Distributor melalui socket PULL
    received_task = pull_socket.recv()

    # Mengubah bytes menjadi objek DataToWorker
    task_data: DataToWorker = pickle.loads(received_task)

    print("\nWORKER-2: Handling the task")

    # Mengambil kedua angka
    num1 = task_data.num1
    num2 = task_data.num2

    # Menentukan operasi perhitungan
    result: float = 0.0

    if task_data.op == mc.SUM:
        result = task_1_sum(num1, num2)

    elif task_data.op == mc.MUT:
        result = task_2_multiply(num1, num2)

    elif task_data.op == mc.DIV:
        result = task_3_division(num1, num2)

    else:
        print("Unknown operation")
        continue

    # Simulasi waktu pemrosesan
    work_time = random.uniform(0.5, 1)
    time_module.sleep(work_time)

    # Menyimpan hasil perhitungan
    task_data.set_result(result)

    # Menyimpan identitas Worker 2
    task_data.set_executor(mc.WORKER_2)

    print(
        f"Result: {result} --- "
        f"Task has been processed by {mc.WORKER_2}"
    )

    # Mengirim hasil ke Collector
    push_socket.send(pickle.dumps(task_data))

    print("Data has been processed, sending them to the collector ...")
    print("--- Sent ---\n")
