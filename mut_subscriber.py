import main_constants as mc
from data_worker import DataToWorker
import pickle
import zmq

# Membuat context ZeroMQ
context = zmq.Context()

# Socket SUB untuk menerima data dari publisher
sub_socket = context.socket(zmq.SUB)
sub_socket.connect("tcp://localhost:5558")

# Hanya menerima pesan dengan topik SUM
sub_socket.setsockopt_string(zmq.SUBSCRIBE, mc.MUT)

print("MUT Subscriber is running ...")
print("Waiting for a new message to arrive...")

def show_content(result):
    result_obj: DataToWorker = pickle.loads(result)
    print(f"Input Numbers: {result_obj.num1} & {result_obj.num2}")
    print(f"Main Operation: {result_obj.op}")
    print(f"Result: {result_obj.result}")
    print(f"Message: {result_obj.message}")
    print(f"EXECUTOR: {result_obj.exe}")

index: int = 0

while True:
    # Menerima topic dan pesan
    topic, message = sub_socket.recv_multipart()

    print("\nReceived a new message with topic's name", str(topic.decode()))
    show_content(message)

    index += 1
    if index >= 5:
        index = 0
    print("\nRepeating ...\n")
