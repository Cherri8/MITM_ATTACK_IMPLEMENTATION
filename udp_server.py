import socket
import json
import select
from prettytable import PrettyTable

def server():
    UDP_IP = "0.0.0.0"
    NORMAL_PORT = 12345
    REPLAY_PORT = 12346  # Different port for replay messages
    BUFFER_SIZE = 2048

    sock_normal = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_normal.bind((UDP_IP, NORMAL_PORT))

    sock_replay = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_replay.bind((UDP_IP, REPLAY_PORT))

    print(f"Server listening on {UDP_IP}:{NORMAL_PORT} for normal messages")
    print(f"Server listening on {UDP_IP}:{REPLAY_PORT} for replay messages")

    student_data_10th = []
    student_data_11th = []
    student_data_12th = []

    while True:
        try:
            ready_socks, _, _ = select.select([sock_normal, sock_replay], [], [])

            for sock in ready_socks:
                data, addr = sock.recvfrom(BUFFER_SIZE)
                message = data.decode()
                print(f"Received data from {addr}: {message}")

                try:
                    student_data = json.loads(message)
                    class_name = student_data['body']['Class']

                    if class_name == "10th":
                        student_data_10th.append((student_data, addr[0]))
                    elif class_name == "11th":
                        student_data_11th.append((student_data, addr[0]))
                    elif class_name == "12th":
                        student_data_12th.append((student_data, addr[0]))

                    response_message = f"Data received for {student_data['body']['Name']} in class {class_name}"
                    sock.sendto(response_message.encode(), addr)

                    if student_data_10th:
                        print("\n10th Class Students:")
                        table_10th = PrettyTable()
                        table_10th.field_names = ["Sequence No", "Timestamp", "Roll No", "Name", "Class", "CGPA", "Message", "IP Address"]
                        for student, ip in student_data_10th:
                            header = student['header']
                            body = student['body']
                            table_10th.add_row([header['sequence_no'], header['timestamp'], body['Roll No'], body['Name'], body['Class'], body['CGPA'], body['Message'], ip])
                        print(table_10th)

                    if student_data_11th:
                        print("\n11th Class Students:")
                        table_11th = PrettyTable()
                        table_11th.field_names = ["Sequence No", "Timestamp", "Roll No", "Name", "Class", "CGPA", "Message", "IP Address"]
                        for student, ip in student_data_11th:
                            header = student['header']
                            body = student['body']
                            table_11th.add_row([header['sequence_no'], header['timestamp'], body['Roll No'], body['Name'], body['Class'], body['CGPA'], body['Message'], ip])
                        print(table_11th)

                    if student_data_12th:
                        print("\n12th Class Students:")
                        table_12th = PrettyTable()
                        table_12th.field_names = ["Sequence No", "Timestamp", "Roll No", "Name", "Class", "CGPA", "Message", "IP Address"]
                        for student, ip in student_data_12th:
                            header = student['header']
                            body = student['body']
                            table_12th.add_row([header['sequence_no'], header['timestamp'], body['Roll No'], body['Name'], body['Class'], body['CGPA'], body['Message'], ip])
                        print(table_12th)

                    with open("received_data.txt", "a") as f:
                        f.write(message + "\n")

                except json.JSONDecodeError:
                    print("Received data is not valid JSON")

        except KeyboardInterrupt:
            print("\nServer terminated by user")
            break

if __name__ == "__main__":
    server()
