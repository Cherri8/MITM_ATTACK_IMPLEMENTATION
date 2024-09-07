import socket
import json
import datetime
import uuid
import random
import time

class StudentDetails:
    def __init__(self, seq_no, rollno, name, class_, cgpa, message):
        self.header = self.create_header(seq_no)
        self.body = self.create_body(rollno, name, class_, cgpa, message)
        self.footer = self.create_footer()

    def create_header(self, seq_no):
        message_id = uuid.uuid4().hex
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        return {'message_id': message_id, 'sequence_no': seq_no, 'timestamp': timestamp}

    def create_body(self, rollno, name, class_, cgpa, message):
        return {'Roll No': rollno, 'Name': name, 'Class': class_, 'CGPA': cgpa, 'Message': message}

    def create_footer(self):
        return {'eof': True}

    def to_json(self):
        message_data = {
            'header': self.header,
            'body': self.body,
            'footer': self.footer
        }
        return message_data

def get_student_details():
    student_list = []

    rollnos = [f"R{i:03d}" for i in range(1, 16)]
    names = ["Alice", "Bob", "Charlie", "David", "Eve", "Faythe", "Grace", "Heidi", "Ivan", "Judy"]
    classes = ["10th", "11th", "12th"]
    cGPAs = [round(random.uniform(2.0, 4.0), 2) for _ in range(15)]
    messages = ["Good", "Average", "Excellent", "Needs Improvement"]

    seq_no = 1
    for class_name in classes:
        for i in range(5):
            rollno = random.choice(rollnos)
            name = random.choice(names)
            cgpa = random.choice(cGPAs)
            message = random.choice(messages)

            student_obj = StudentDetails(seq_no, rollno, name, class_name, cgpa, message)
            student_list.append(student_obj)
            seq_no += 1
            time.sleep(0.002)

    return student_list

def main():
    SERVER_IP = "192.168.0.105"
    SERVER_PORT = 12345
    BUFFER_SIZE = 2048

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_address = (SERVER_IP, SERVER_PORT)

    try:
        student_messages = get_student_details()

        for student_obj in student_messages:
            student_data = student_obj.to_json()
            student_str = json.dumps(student_data)

            sock.sendto(student_str.encode(), server_address)
            print(f"Sent Student Details Message ID {student_obj.header['message_id']} to Server")

            with open("sample_log.txt", "a") as log_file:
                log_file.write(student_str + "\n")

            data, _ = sock.recvfrom(BUFFER_SIZE)
            print(f"Server response for Student Details Message {student_obj.header['message_id']}: {data.decode()}")

    except Exception as e:
        print(f"Error occurred: {e}")

    finally:
        sock.close()

if __name__ == "__main__":
    main()
