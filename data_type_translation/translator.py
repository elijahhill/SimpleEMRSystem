from typing import Dict
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

    def add_output_path(self, output_path: str):
        self.output_path = output_path

    def get_excel_path(self):
        return self.excel_path

    def get_output_path(self):
        return self.output_path


class StudyCreator:
    def __get_data_paths(self, current_path: str) -> PathContainer:
        json_paths = path.join(current_path, "./paths.json")
        with open(json_paths) as paths_fp:
            paths = json.load(paths_fp)

        path_container = PathContainer()

        layout = [[sg.T("")], [sg.Text("Choose the excel data file: "), sg.Input(default_text=paths["excel_path"]),
                               sg.FileBrowse(key="-ExcelFile-")],
                  [sg.T("")], [sg.Text("Choose the output path (as a folder) "), sg.Input(default_text=paths["output_path"]),
                               sg.FolderBrowse(key="-OutputFolder-")],
                  [sg.Button("Submit")]]
        window = sg.Window('Locate File', layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            elif event == "Submit":
                # TODO: Need to add checks to determine file validity

                # Using indexes because the keys don't take into account pre-entered file paths
                path_container.add_excel_path(values[0])
                path_container.add_output_path(values[1])

                paths["excel_path"] = path_container.get_excel_path()
                paths["output_path"] = path_container.get_output_path()
                with open(json_paths, "w") as paths_fp:
                    json.dump(obj=paths, fp=paths_fp, indent=4)

                window.close()

        return path_container

    def __get_df(self, excel_path: str):
        df = pd.read_excel(excel_path, engine="openpyxl")
        df["EWS percentile"] = df["ecart percentile"].round(1)
        return df

    def __get_translation(self, current_path: str) -> dict:
        translation = None
        with open(f"{current_path}/stat_lookup.json") as f:
            translation = json.load(f)

        if(translation != None):
            return translation
        else:
            raise Exception("Translation file is empty")

    def __create_user_details(self, user_names: list, patients: list) -> Dict:
        print("creating user details")
        all_user_details = {}
        for user in user_names:
            user_details = {
                "last_accessed": None,
                "cases_assigned": patients,
                "cases_completed": []
            }
            all_user_details[user] = user_details
        return all_user_details

    def __create_case_details(self, case_ids: set, min_time: float = 1352687400000.0, max_time: float = 135294660000.0) -> Dict:
        print("Creating case details")
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

    def __create_data_layout(self):
        print("Creating data layout")
        return {
            "title_bar": ["id", "age", "sex", "height", "weight", "bmi", "race"],
            "risk_score_and_vitals": ["ews", "HR", "RR", "BP", "SaO2", "Temperature"],
            "neurology": ["AVPU"],
            "blood_gas_cbc_lactate": ["pC02", "HgB", "WBC", "Platelets", "Lactate"],
            "chemistry": ["Sodium", "Potassium", "Chloride", "Anion_Gap", "Gluc_Ser", "Bun", "Bun_Cr_Ratio", "Calcium"]
        }

    def __add_to_start_time(self, hours: float):
        minimum_time = 1352687400000
        # Convert hours to milliseconds
        ms = hours * 3600000
        # add to start milliseconds
        total_ms = ms + minimum_time
        # Return
        return total_ms


    def __get_new_data(self, key: str, one_patient: DataFrame):
        hours_and_hr = one_patient[["hours_since_first_vitals", key]]

        hours_and_hr_no_nan = hours_and_hr.dropna(
            subset=[key]).reset_index(drop=True)


        # TODO: What did this originally do?
        hours_and_hr_no_nan["hours_since_first_vitals"] = hours_and_hr_no_nan["hours_since_first_vitals"].map(
            self.__add_to_start_time())

        new_data = hours_and_hr_no_nan.values.tolist()

        return new_data

    

    def create_study(self):
        print("Fetching data")
        current_path = path.dirname(__file__)
        data_paths = self.__get_data_paths(current_path=current_path)
        excel_path = data_paths.get_excel_path()
        output_folder_path = data_paths.get_output_path()

        df = self.__get_df(excel_path=excel_path)
        translation = self.__get_translation(current_path=current_path)

        # patients = set(df["patient_id"])

        # Make sure all of these elements are strings
        # first_patient = [str(patients.pop())]

        case_ids = set(df["patient_id"])

        case_ids_str_list = list(map(lambda elem: str(elem), case_ids))

        users = ["testuser1"]
        user_details = self.__create_user_details(
            user_names=users, patients=case_ids_str_list)
        with open(f"{output_folder_path}/user_details.json", "w+") as fp:
            json.dump(obj=user_details['testuser1'], fp=fp, indent=4)

        case_ids = set(df["patient_id"])
        case_details = self.__create_case_details(case_ids=case_ids)
        with open(f"{output_folder_path}/case_details.json", "w+") as fp:
            json.dump(obj=case_details, fp=fp, indent=4)

        print("Creating data layout")
        data_layout = self.__create_data_layout()
        with open(f"{output_folder_path}/data_layout.json", "w+") as fp:
            json.dump(obj=data_layout, fp=fp, indent=4)

        print("Creating variable details")
        with open(f"{current_path}/variable_details.json") as fp:
            variable_details = json.load(fp=fp)

        with open(f"{output_folder_path}/variable_details.json", "w+") as fp:
            json.dump(obj=variable_details, fp=fp, indent=4)



        one_patient = df[df["patient_id"] == 610044]

        with open(f"{current_path}/observations.json", "r") as fp:
            observations = json.load(fp)

        try:
            Path(f"{output_folder_path}/cases_all").mkdir(parents=False, exist_ok=False)
        except:
            pass

        for key in keys:

            observation_key = translation[key]["internal_name"]

            # TODO: Add check to create the folders https://stackoverflow.com/questions/273192/how-can-i-safely-create-a-nested-directory-in-python

            

            if observation_key == "VTDIAV":
                observations[observation_key]["numeric_lab_data"][0]["data"] = self.__get_new_data(
                    "dbp", one_patient)
                observations[observation_key]["numeric_lab_data"][1]["data"] = self.__get_new_data(
                    "sbp", one_patient)
            else:
                observations[observation_key]["numeric_lab_data"][0]["data"] = self.__get_new_data(
                    key, one_patient)

            # TODO: Need to make sure the one_patient folder has been created for each patient
            with open(f"{output_folder_path}/cases_all/{one_patient}/observations.json", "w") as fp:
                json.dump(observations, fp)


creator = StudyCreator()
creator.create_study()



