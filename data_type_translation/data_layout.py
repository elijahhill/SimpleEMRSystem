import json
from typing import Dict, List

class DataLayout:

    def __init__(self, output_folder_path: str):
        self.output_folder_path = output_folder_path
        self.data_layout = {
            "title_bar": ["id", "age", "sex", "height", "weight", "bmi", "race"],
            "risk_score_and_vitals": ["EWS", "VTHR", "VTDIAV", "VTRR", "VTSO2A", "VTTEMA"],
            "neurology": ["AVPU", "LACT", "CA"],
            "chemistry": ["NA", "K", "CL", "CO2", "AGAP", "BUN", "CREAT", "BCR", "GLU"],
            "blood_gas_cbc_lactate": ["HGB", "WBC", "PLT"],
            "notes": ["note section 1", "note section 2", "note section 3"]
        }

    def __create_data_layout(self):
        print("Creating data layout")
        return self.data_layout

    def write_data_layout(self):
        print("Creating data layout")
        data_layout = self.__create_data_layout()
        with open(f"{self.output_folder_path}/data_layout.json", "w+") as fp:
            json.dump(obj=data_layout, fp=fp, indent=4)
