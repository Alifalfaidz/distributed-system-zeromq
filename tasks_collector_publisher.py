
import zmq
import pickle
from data_worker import DataToWorker
import main_constants as mc

# Membuat context ZeroMQ
context = zmq.Context()

# Socket PULL untuk menerima data dari Worker 1
pull_worker_1 = context.socket(zmq.PULL)
pull_worker_1.connect("tcp://localhost:5556")

# Socket PULL untuk menerima data dari Worker 2
pull_worker_2 = context.socket(zmq.PULL)
pull_worker_2.connect("tcp://localhost:5557")

# Socket PUB untuk mempublikasikan hasil
pub_socket = context.socket(zmq.PUB)
pub_socket.bind("tcp://*:5558")

# Poller untuk memantau kedua socket Worker
poller = zmq.Poller()
poller.register(pull_worker_1, zmq.POLLIN)
poller.register(pull_worker_2, zmq.POLLIN)


# Fungsi untuk menambahkan pesan ke data
def set_data_message(data: DataToWorker, message: str):
    data.set_message(message)
    return data


# Pesan berdasarkan jenis operasi
message_sum = "The summation process has been executed successfully"
message_multiply = "The multiplication process has been executed successfully"
message_div = "The division process has been executed successfully"

print("Tasks collector is running ...")
print("Waiting for results from workers ...")

while True:

    # Memantau kedua socket PULL
    events = dict(poller.poll())

    # Memeriksa Worker yang mengirim hasil
    for worker_socket in [pull_worker_1, pull_worker_2]:

        # Periksa apakah socket menerima pesan
        if worker_socket not in events:
            continue

        # Menerima pesan dari Worker
        received_task = worker_socket.recv()

        # Mengubah bytes menjadi objek DataToWorker
        task_data: DataToWorker = pickle.loads(received_task)

        print("\nTask is received")

        # Menentukan pesan berdasarkan operasi
        if task_data.op == mc.SUM:
            result = set_data_message(task_data, message_sum)

        elif task_data.op == mc.MUT:
            result = set_data_message(task_data, message_multiply)

        elif task_data.op == mc.DIV:
            result = set_data_message(task_data, message_div)

        else:
            print("Unknown operation")
            continue

        # Menampilkan hasil yang diterima
        print(f"Operation: {result.op}")
        print(f"Numbers: {result.num1} & {result.num2}")
        print(f"Result: {result.result}")
        print(f"Executor: {result.exe}")

        # Mengubah topic dan objek menjadi bytes
        topic = result.op.encode("utf-8")
        message = pickle.dumps(result)

        print("Sending the results to subscribers...")

        # Mempublikasikan pesan berdasarkan topic
        pub_socket.send_multipart([topic, message])

        print(f"Published topic: {result.op}")
        print("--- Sent ---\n")
