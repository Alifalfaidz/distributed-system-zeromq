from data_worker import DataToWorker
import main_constants as mc
import zmq
import time
import random
import pickle

### Here's the step by step
### Create your context 
### Create 1 socket using the PUSH socket type
### Bind your PUSH socket to your desired endpoint.

# Membuat context ZeroMQ
context = zmq.Context()

#membuat socket PUSH
socket = context.socket(zmq.PUSH)

# Menentukan alamat dan port Distributor
address = "tcp://*:5555"
socket.bind(address)

print(f"Tasks distributor is running on {address}")
print("Sending tasks to workers")
print("There are 3 available tasks")
print("Sum; Multiply; Division")

while True:
    ### Generate 2 random numbers
    ### set the appropriate value for the given variables
    ## send the data
    time.sleep(5)

    #menghasilkan 2 angka random antara 1 dan 20
    num1 = random.randint(1, 20)
    num2 = random.randint(1, 20)

    # Memilih operasi secara acak dari daftar operasi yang tersedia
    task_code = random.choice([mc.SUM, mc.MUT, mc.DIV])

    # Membuat objek tugas
    task_data = DataToWorker(num1, num2, task_code)

    # Mengubah objec menjadi bytes
    sent_task = pickle.dumps(task_data)

    print(
        f"Sending task --- {task_code} "
        f"({num1} & {num2}) waiting for available worker to handle"
    )

    # Mengirim data ke worker melalui socket PUSH
    socket.send(sent_task)

    print("--- Sent --- ")
