from dataclasses import dataclass
import csv
def read_in(filename : str ) -> list:
    patient_list = []

    with open(filename, 'r') as csv_read:
        csvfile_reader = csv.reader(csv_read)

        reader = csv.reader(csv_read, delimiter=',')
        if next(csvfile_reader, None) is None:
            next(reader)
        for row in reader:
            patient_list.append(row)
        return patient_list

def mask(info :str, index: int) -> str:

    masked_info = str(index) +

    return masked_info

def replace_proprietery(patient_data :list) -> list:
    curr_data = ""
    def store_proprietery(enc_val, real_val):
        pass
    for i in range(7):
        curr_data = patient_data[i]
        sec_data = mask(patient_data[i], i)
        patient_data[i] = sec_data
        store_proprietery(sec_data, curr_data)

    return []
def prep_inejct(masked_data: list):
    return 0

def decrypt():
    pass


def encrypt(filename :str):
    patient_set = read_in(filename)
    for patient in patient_set:
        replace_proprietery(patient)


if __name__ == "__main__":

    encrypt("..\patient_info.csv")