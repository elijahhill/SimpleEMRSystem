from pandas.core.frame import DataFrame
from typing import Dict, List
import json

class CaseDetails:

    def __init__(self, output_folder_path: str, case_id_str_list: List[str]):
        self.output_folder_path = output_folder_path
        self.case_ids = case_id_str_list

    def __add_to_start_time(self, hours: float, minimum_time: int = 1352687400000):
        # Convert hours to milliseconds, 3600000 milliseconds being 1 hour
        ms = hours * 3600000
        # add to start milliseconds
        total_ms = ms + minimum_time
        # Return
        return total_ms

    def __create_case_details(self, case_times: DataFrame, min_time: float = 1352687400000.0, max_time: float = 1352946600000.0) -> Dict:
        print("Creating case details")
        all_case_details = {}
        for case_id in self.case_ids:
            patient_case_times = case_times[case_times["patient_id"] == int(
                case_id)]
            hours_list = patient_case_times["hours_since_first_vitals"].reset_index(
                drop=True)
            min_time = self.__add_to_start_time(float(hours_list[0]))
            max_time = self.__add_to_start_time(
                float(hours_list[len(hours_list) - 1]))
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

    def write_case_details(self, hospitalrisk_df: DataFrame):
        case_details = self.__create_case_details(case_times=hospitalrisk_df[["patient_id", "hours_since_first_vitals"]])
        with open(f"{self.output_folder_path}/case_details.json", "w+") as fp:
            json.dump(obj=case_details, fp=fp, indent=4)
