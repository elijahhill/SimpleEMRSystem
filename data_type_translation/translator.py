from numpy.core.numeric import NaN
import pandas as pd
import json
from pathlib import Path
from pandas.core.frame import DataFrame
from os import path
import PySimpleGUI as sg

class PathContainer:
    def __init__(self):
        pass

    def add_excel_path(self, excel_path: str):
        self.excel_path = excel_path

    def add_output_folder(self, output_folder: str):
        self.output_folder = output_folder

    def get_excel_path(self):
        return self.excel_path

    def get_output_folder(self):
        return self.output_folder

    
class StudyCreator:

    def __read_data(self):

        data_paths = self.__get_data_path()

        df = pd.read_excel(data_paths.get_excel_path(), engine="openpyxl")

        df["ecart percentile"] = df["ecart percentile"].round(1)

        self.df = df
    
        translation = None
        with open("./data_type_translation/stat_lookup.json") as f:
            translation = json.load(f)

        if(translation != None):
            self.keys = translation.keys()
        else:
            raise Exception("Translation file is empty")

    def __get_data_path(self) -> PathContainer:
        dirname = path.dirname(__file__)
        json_paths = path.join(dirname, "./paths.json")
        with open(json_paths) as paths_fp:
            paths = json.load(paths_fp)

        path_container = PathContainer()
        
        layout = [[sg.T("")], [sg.Text("Choose the excel data file: "), sg.Input(default_text=paths["excel_path"]),
                            sg.FileBrowse(key="-ExcelFile-")], 
                  [sg.T("")], [sg.Text("Choose the output folder "), sg.Input(default_text=paths["output_path"]),
                               sg.FileBrowse(key="-OutputFolder-")], [sg.Button("Submit")]]
        window = sg.Window('Locate File', layout)
        
        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            elif event == "Submit":
                # TODO: Need to add checks to determine file validity
                path_container.add_excel_path(values["-ExcelFile-"])
                path_container.add_output_folder(values["-OutputFolder-"])

                paths["excel_path"] = path_container.get_excel_path()
                paths["output_path"] = path_container.get_output_folder()
                with open(json_paths, "w") as paths_fp:
                    json.dump(paths, paths_fp)

                window.close()

        return path_container
    
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

    def __create_case_details(self, case_ids: set, min_time: float=1352687400000.0, max_time: float=135294660000.0):
        all_case_details = {}
        for case_id in case_ids:
            details_list = [
                {
                    "min_t": min_time,
                    "max_t": max_time,
                    "check_boxes": 0,
                    "instruction_set": "familiar"
                }, 
                {
                    "min_t": min_time,
                    "max_t": max_time,
                    "check_boxes": 1,
                    "instruction_set": "select"
                }
            ]
            all_case_details[case_id] = details_list
        return all_case_details

    def create_study(self):
        self.__read_data()

        patients = set(self.df["patient_id"])
        first_patient = [patients.pop()]

        users = ["testuser1"]
        user_details = self.__create_user_details(user_names=users, patients=first_patient)

        case_ids = set(self.df["patient_id"])
        case_details = self.__create_case_details(case_ids=case_ids)
        return case_details



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
