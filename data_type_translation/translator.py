from numpy.core.numeric import NaN
import pandas as pd
import json
from pathlib import Path
from pandas.core.frame import DataFrame
import PySimpleGUI as sg

class StudyCreator:
    def __init__(self):
        self.minimum_time = 1352687400000
        self.maximum_time = 1352946600000

    def __read_data(self):

        data_path = self.__get_data_path()

        df = pd.read_excel(data_path, engine="openpyxl")

        df["ecart percentile"] = df["ecart percentile"].round(1)

        self.df = df
    
        translation = None
        with open("./data_type_translation/stat_lookup.json") as f:
            translation = json.load(f)

        if(translation != None):
            self.keys = translation.keys()
        else:
            raise Exception("Translation file is empty")

    def __get_data_path(self):
        ret_value = ""
        
        # sg.theme("DarkTeal2")
        layout = [[sg.T("")], [sg.Text("Choose the excel data file: "), sg.Input(),
                            sg.FileBrowse(key="-IN-")], [sg.Button("Submit")]]
        window = sg.Window('Locate File', layout, size=(600, 150))
        
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            elif event == "Submit":
                ret_value = values["-IN-"]
                window.close()

        return ret_value
    
    def __create_user_details(self, user_names: list, patients: list):
        all_user_details = {}
        for user in user_names:
            user_details = {
                "last_accessed": None,
                "cases_assigned": patients,
                "cases_completed": []
            }
            all_user_details[user] = user_details
        return all_user_details

    def __create_case_details(self):
        pass

    def create_study(self):
        self.__read_data()

        patients = set(self.df["patient_id"])
        first_patient = [patients.pop()]

        users = ["testuser1"]
        user_details = self.__create_user_details(user_names=users, patients=first_patient)
        return user_details



user_index = 0
user_name = f"user{user_index}"
creator = StudyCreator()
# print(creator.create_study([user_name]))
print(creator.create_study())


# def add_to_start_time(self, hours: float):
#     # Convert hours to milliseconds
#     ms = hours * 3600000
#     # add to start milliseconds
#     total_ms = ms + minimum_time
#     # Return
#     return total_ms

# def get_new_data(self, key: str, one_patient: DataFrame):
#     hours_and_hr = one_patient[["hours_since_first_vitals", key]]

#     hours_and_hr_no_nan = hours_and_hr.dropna(
#         subset=[key]).reset_index(drop=True)

#     hours_and_hr_no_nan["hours_since_first_vitals"] = hours_and_hr_no_nan["hours_since_first_vitals"].map(
#         add_to_start_time)

#     new_data = hours_and_hr_no_nan.values.tolist()

#     return new_data



#     one_patient = df[df["patient_id"] == 610044]

#     for key in keys:

#         path = Path(r"C:\Users\Elijah\simpleemr\SimpleEMRSystem\resources\manual_data_entry_study\cases_all\10000101\observations.json")

#         observations = None
#         with open(path, "r") as fp:
#             observations = json.load(fp)

#         observation_key = translation[key]["internal_name"]

#         if observation_key == "VTDIAV":
#             observations[observation_key]["numeric_lab_data"][0]["data"] = get_new_data(
#                 "dbp", one_patient)
#             observations[observation_key]["numeric_lab_data"][1]["data"] = get_new_data(
#                 "sbp", one_patient)
#         else:
#             observations[observation_key]["numeric_lab_data"][0]["data"] = get_new_data(key, one_patient)

#         with open(path, "w") as fp:
#             json.dump(observations, fp)
