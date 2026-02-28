#personal
import gemini
import secure_io

if __name__ == '__main__':
    #print ui

    #read data
    patients = secure_io.read_csv('patients.csv')

    #enter patient that you want

    patient_name = "foo"
    for patient in patients:
        if patient[1] == patient[patient_name]:
            formatted_info = [patients[0], patient]
            message = (f"past information = {formatted_info}. using the patients past info fill out the information needed"
                       "to fill out an admissions form from the given template into a json style format.")
            response = gemini.gemini_call(message)












