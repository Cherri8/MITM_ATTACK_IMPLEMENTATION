from scapy.all import rdpcap
import json
from prettytable import PrettyTable

def log_to_file(data, filename="received.txt"):
    with open(filename, "a") as file:
        file.write(data + "\n")

def extract_necessary_data(student_data):
    header = student_data['header']
    body = student_data['body']
    return {
        'Sequence No': header['sequence_no'],
        'Timestamp': header['timestamp'],
        'Roll No': body['Roll No'],
        'Name': body['Name'],
        'Class': body['Class'],
        'CGPA': body['CGPA'],
        'Message': body['Message']
    }

def process_pcap(pcap_file):
    packets = rdpcap(pcap_file)
    received_data_list = []

    for packet in packets:
        try:
            if packet.haslayer('UDP'):
                data = packet['UDP'].payload.load.decode()
                student_data = json.loads(data)
                necessary_data = extract_necessary_data(student_data)
                received_data_list.append(necessary_data)
                log_to_file(json.dumps(necessary_data))
        except Exception as e:
            print(f"Error processing packet: {e}")

    # Sort received_data_list by 'Sequence No' and 'Timestamp'
    sorted_data = sorted(received_data_list, key=lambda x: (x['Sequence No'], x['Timestamp']))

    # Display sorted data in tabular format
    table = PrettyTable()
    table.field_names = ["Sequence No", "Timestamp", "Roll No", "Name", "Class", "CGPA", "Message"]
    for entry in sorted_data:
        table.add_row([entry["Sequence No"], entry["Timestamp"], entry["Roll No"], entry["Name"], entry["Class"], entry["CGPA"], entry["Message"]])
    print(table)

if __name__ == "__main__":
    process_pcap("two.pcap")
