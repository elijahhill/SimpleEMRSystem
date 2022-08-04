import json
from pandas.core.frame import DataFrame

class Observations:

    def __init__(self, current_path: str):
        self.current_path = current_path
        self.translation = self.__get_translation()

    def __get_translation(self) -> dict:
        translation = None
        with open(f"{self.current_path}/data_translation_paths/stat_lookup.json") as f:
            translation = json.load(f)

        if(translation != None):
            return translation
        else:
            raise Exception("Translation file is empty")
    
    def __add_to_start_time(self, hours: float, minimum_time: int = 1352687400000):
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

    def create_observations(self, patient_path, hospitalrisk_df, case_id):
        hospitalrisk_keys = self.translation.keys()
        one_patient = hospitalrisk_df[hospitalrisk_df["patient_id"] == case_id]

        with open(f"{self.current_path}/data_translation_files/observations.json", "r") as fp:
            observations_template = json.load(fp)

        for hospitalrisk_key in hospitalrisk_keys:
            observation_key = self.translation[hospitalrisk_key]["internal_name"]

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

    

    