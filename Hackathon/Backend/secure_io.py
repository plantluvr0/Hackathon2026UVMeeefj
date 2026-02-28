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

def replace_proprietery() -> list:
    def store_proprietery(name_mask_pair: dict):
        return 0
    return []
def prep_inejct(masked_data: list):
    return 0

def decrypt():
    pass


def encrypt(filename :str):
    patient_set = read_in(filename)
    for patient in patient_set:
        p_key = patient[0]+patient[1]+patient[2]+patient[3]+patient[4]+patient[5]+patient[6]+patient[7]
        print(p_key)

if __name__ == "__main__":
    encrypt("..\patient_info.csv")