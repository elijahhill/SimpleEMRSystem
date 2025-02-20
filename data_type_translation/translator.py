from typing import Dict
import pandas as pd
import json
from pathlib import Path
from pandas.core.frame import DataFrame
from os import path
import PySimpleGUI as sg


class PathContainer:
    def __init__(self):
        pass

    def add_hospitalrisk_path(self, hospitalrisk_path: str):
        self.hospitalrisk_path = hospitalrisk_path

    def get_hospitalrisk_path(self):
        return self.hospitalrisk_path

    def add_output_path(self, output_path: str):
        self.output_path = output_path

    def get_output_path(self):
        return self.output_path

    def add_hospitalrisk_demo(self, hospitalrisk_demo: str):
        self.hospitalrisk_demo = hospitalrisk_demo

    def get_hospitalrisk_demo(self):
        return self.hospitalrisk_demo


class StudyCreator:
    def __get_data_paths(self, current_path: str) -> PathContainer:
        """
        Paths will be under the 1_Contextual_Interviews folder
        hospitalrisk_path: Path to hospitalrisk_ecart_wpercentilescoring.xlsx
        output_path: Path to autogenerated_study
        hospitalrisk_demo_path: Path to labeled_hospitalrisk_demo.csv
        """
        json_paths = path.join(current_path, "./paths.json")
        with open(json_paths) as paths_fp:
            paths = json.load(paths_fp)

        path_container = PathContainer()

        layout = [[sg.T("")], [sg.Text("Choose the output path folder within SEMR - ex. autogenerated_study"), sg.Input(default_text=paths["output_path"]),
                               sg.FolderBrowse(key="-OutputFolder-")],
                  [sg.T("")], [sg.Text("Choose the excel data file - ex. hospitalrisk_ecart_wpercentilescoring.xlsx"), sg.Input(default_text=paths["hospitalrisk_path"]),
                               sg.FileBrowse(key="-ExcelFile-")],
                  [sg.T("")], [sg.Text("Choose labeled hospitalrisk_demo - ex. labeled_hospitalrisk_demo.csv"), sg.Input(default_text=paths["hospitalrisk_demo_path"]),
                               sg.FileBrowse(key="-HospitalriskDemo-")],
                  [sg.Button("Submit")]]
        window = sg.Window('Locate File', layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED or event == "Exit":
                break
            elif event == "Submit":
                # TODO: Need to add checks to determine file validity

                # Using indexes because the keys don't take into account pre-entered file paths
                path_container.add_output_path(values[0])
                path_container.add_hospitalrisk_path(values[1])
                path_container.add_hospitalrisk_demo(values[2])

                paths["output_path"] = path_container.get_output_path()
                paths["hospitalrisk_path"] = path_container.get_hospitalrisk_path()
                paths["hospitalrisk_demo_path"] = path_container.get_hospitalrisk_demo()

                with open(json_paths, "w") as paths_fp:
                    json.dump(obj=paths, fp=paths_fp, indent=4)

                window.close()

        return path_container

    def __get_hospitalrisk_df(self, excel_path: str):
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

    def __create_case_details(self, hospitalrisk_df: DataFrame, case_ids: set, min_time: float = 1352687400000.0, max_time: float = 1352946600000.0) -> Dict:
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
            "risk_score_and_vitals": ["EWS", "HR", "RR", "BP", "SaO2", "Temperature"],
            "neurology": ["AVPU"],
            "blood_gas_cbc_lactate": ["CO2", "HgB", "WBC", "Platelets", "Lactate"],
            "chemistry": ["Sodium", "Potassium", "Chloride", "Anion_Gap", "Glucose", "BUN", "Creatinine", "BUN-Creatinine_ratio", "Calcium"],
            "notes": ["note section 1", "note section 2", "note section 3"]
        }

    def __add_to_start_time(self, hours: float):
        minimum_time = 1352687400000
        # Convert hours to milliseconds, 3600000 milliseconds being 1 hour
        ms = hours * 3600000
        # add to start milliseconds
        total_ms = ms + minimum_time
        # Return
        return total_ms

    def __get_new_data(self, hospitalrisk_key: str, one_patient: DataFrame):
        # TODO : Make this method work correctly time wise.
        hours_and_other = one_patient[[
            "hours_since_first_vitals", hospitalrisk_key]]

        hours_and_other_no_nan = hours_and_other.dropna(
            subset=[hospitalrisk_key]).reset_index(drop=True)

        # Converts js to unix time
        hours_and_other_no_nan["hours_since_first_vitals"] = list(map(
            lambda hours: self.__add_to_start_time(
                hours), hours_and_other_no_nan["hours_since_first_vitals"]
        ))

        new_data = hours_and_other_no_nan.values.tolist()

        return new_data


    def create_study(self):
        '''
        Creates a study
        '''
        print("Fetching data")
        current_path = path.dirname(__file__)
        data_paths = self.__get_data_paths(current_path=current_path)
        hospitalrisk_path = data_paths.get_hospitalrisk_path()
        output_folder_path = data_paths.get_output_path()

        df = self.__get_hospitalrisk_df(excel_path=hospitalrisk_path)

        df.dropna(subset=["patient_id"], inplace=True)

        numeric_ids = pd.to_numeric(
            arg=df["patient_id"], errors='raise', downcast='integer')

        case_ids = set(numeric_ids)

        case_ids_str_list = list(map(lambda elem: str(elem), case_ids))

        users = ["testuser1"]
        user_details = self.__create_user_details(
            user_names=users, patients=case_ids_str_list)
        with open(f"{output_folder_path}/user_details.json", "w+") as fp:
            json.dump(obj=user_details, fp=fp, indent=4)

        case_ids = set(df["patient_id"])
        case_details = self.__create_case_details(hospitalrisk_df=df, case_ids=case_ids_str_list)
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

        try:
            cases_path = Path(f"{output_folder_path}/cases_all")
            cases_path.mkdir(parents=False, exist_ok=False)
        except:
            pass

        hospitalrisk_path = data_paths.get_hospitalrisk_demo()
        hospitalrisk_df = pd.read_csv(hospitalrisk_path)

        keys = set(hospitalrisk_df["patient_id"])
        translation = self.__get_translation(current_path=current_path)

        # Need to grab all of the potential user id's, those will be the keys
        for key in keys:
            print(f"Creating case: {key}")
            # Create id folder
            try:
                patient_path = cases_path / str(key)
                patient_path.mkdir(parents=False, exist_ok=False)
            except:
                pass

            # Will need to create demographics for each user
            demographics_info = hospitalrisk_df[hospitalrisk_df["patient_id"] == key]
            # TODO: Need - Weight, Height, and BMI
            # Getting iloc[0] as not doing so returns a series with the index and value
            demographics_dict = {
                "weight": 0,
                "age": int(demographics_info["age"].iloc[0]),
                "bmi": 0,
                "sex": demographics_info["sex"].iloc[0],
                "race": demographics_info["race"].iloc[0],
                "height": 0,
                "id": key
            }

            try:
                demographics_path = patient_path / "demographics.json"
                demographics_path.touch(exist_ok=True)
            except PermissionError:
                raise PermissionError(
                    "Permission denied when creating demograhpics file")

            with open(demographics_path, "w+") as fp:
                json.dump(obj=demographics_dict, fp=fp, indent=4)

            # TODO: Need to create a note panel

            # note_headers = data_layout["notes"]
            all_notes_dict = {}

            note_date = "11/11"
            note_text = "This is text for a note"
            note_time = 1352687800000.0
            note_headers = data_layout["notes"]

            for note_header in note_headers:
                all_notes_dict[note_header] = []

            note_dict = {
                "date": note_date,
                "text": note_text,
                "js_time": note_time,
                "upk": 0,
                "type": note_headers[0]
            }

            all_notes_dict[note_dict["type"]].append(note_dict)

            try:
                note_panel_path = patient_path / "note_panel_data.json"
                note_panel_path.touch(exist_ok=True)
            except PermissionError:
                raise PermissionError(
                    "Permission denied when creating notes file")

            with open(note_panel_path, "w+") as fp:
                json.dump(obj=all_notes_dict, fp=fp, indent=4)

            # Creating an observations file by modifying the observations.json template created

            hospitalrisk_keys = translation.keys()
            one_patient = df[df["patient_id"] == key]

            with open(f"{current_path}/observations.json", "r") as fp:
                observations_template = json.load(fp)

            for hospitalrisk_key in hospitalrisk_keys:
                observation_key = translation[hospitalrisk_key]["internal_name"]

                if observation_key == "VTDIAV":
                    observations_template[observation_key]["numeric_lab_data"][0]["data"] = self.__get_new_data(
                        "dbp", one_patient)
                    observations_template[observation_key]["numeric_lab_data"][1]["data"] = self.__get_new_data(
                        "sbp", one_patient)
                else:
                    observations_template[observation_key]["numeric_lab_data"][0]["data"] = self.__get_new_data(
                        hospitalrisk_key, one_patient)

            with open(f"{patient_path}/observations.json", "w") as fp:
                json.dump(observations_template, fp, indent=4)


creator = StudyCreator()
creator.create_study()
