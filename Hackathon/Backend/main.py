import gemini

if __name__ == '__main__':
    #print ui
    #read user info
    #enter patient that you want
    patient = "foo"
    message = ("[past info]. using the patients past info fill out the information needed"
               "to fill out an admissions form from the given template into a json style format.")

    response = gemini.gemini_call(message)







