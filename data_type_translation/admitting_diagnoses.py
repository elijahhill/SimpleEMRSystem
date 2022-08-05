import json


class AdmittingDiagnoses():

    def __init__(self, output_folder_path: str, current_path: str):
        self.output_folder_path = output_folder_path
        self.current_path = current_path

    def write_admitting_diagnoses(self):
        print("Creating variable details")
        with open(f"{self.current_path}/data_translation_files/admitting_diagnoses.json") as fp:
            variable_details = json.load(fp=fp)

        with open(f"{self.output_folder_path}/admitting_diagnoses.json", "w+") as fp:
            json.dump(obj=variable_details, fp=fp, indent=4)
