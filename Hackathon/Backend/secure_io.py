from dataclasses import dataclass
import csv
import secrets


def read_in(filename: str) -> tuple:
    patient_list = []
    with open(filename, 'r') as csv_read:
        csvfile_reader = csv.reader(csv_read)

        reader = csv.reader(csv_read, delimiter=',')
        header = next(reader)
        for row in reader:
            patient_list.append(row)
        return patient_list, header


def mask(info: str) -> str:
    mask_num = int(hex(secrets.randbits(len(info))), 0)
    hex_info = int(info.encode().hex(), 0)
    masked_info = mask_num ^ hex_info
    return str(masked_info)


def replace_proprietary(patient_data: list) -> list:
    curr_data = ""

    def store_proprietary(enc_val, real_val):
        with open("../key_val.csv", 'a') as key_file:
            writer = csv.writer(key_file)
            writer.writerow([enc_val, real_val])

    for i in range(1, 7):
        curr_data = patient_data[i]
        sec_data = mask(patient_data[i])
        patient_data[i] = sec_data
        store_proprietary(sec_data, curr_data)

    return patient_data


def decrypt(fmt_data: dict) -> list:
    return []


def encrypt(filename: str) -> tuple:
    patient_set, header = read_in(filename)
    for patient in patient_set:
        replace_proprietary(patient)
    return patient_set, header


def inject_data() -> tuple:
    return encrypt("patient_info.csv")
