from numpy.core.numeric import NaN
import pandas as pd
import json
from pathlib import Path

from pandas.core.frame import DataFrame

# ..\resources\manual_data_entry_study\case_details.json
# Minimum time: 1352687400000 - Gotten from case_details.json



minimum_time = 1352687400000

def add_to_start_time(hours: float):
    # Convert hours to milliseconds
    ms = hours * 3600000
    # add to start milliseconds
    total_ms = ms + minimum_time
    # Return
    return total_ms

def get_new_data(key: str, one_patient: DataFrame):
    hours_and_hr = one_patient[["hours_since_first_vitals", key]]

    hours_and_hr_no_nan = hours_and_hr.dropna(
        subset=[key]).reset_index(drop=True)

    hours_and_hr_no_nan["hours_since_first_vitals"] = hours_and_hr_no_nan["hours_since_first_vitals"].map(
        add_to_start_time)

    new_data = hours_and_hr_no_nan.values.tolist()

    return new_data


thing = Path().absolute()
df = pd.read_excel(
    r"C:\Users\Elijah\Box\1_Contextual interviews\eCART data to select cases\hospitalrisk_ecart_wpercentilescoring.xlsx", engine="openpyxl")

df["ecart percentile"] = df["ecart percentile"].round(1)

translation = None
with open("./data_type_translation/stat_lookup.json") as f:
    translation = json.load(f)

if(translation != None):
    keys = translation.keys()
else:
    raise Exception()

one_patient = df[df["patient_id"] == 610044]

for key in keys:

    path = Path(r"C:\Users\Elijah\simpleemr\SimpleEMRSystem\resources\manual_data_entry_study\cases_all\10000101\observations.json")

    observations = None
    with open(path, "r") as fp:
        observations = json.load(fp)

    observation_key = translation[key]["internal_name"]

    if observation_key == "VTDIAV":
        observations[observation_key]["numeric_lab_data"][0]["data"] = get_new_data(
            "dbp", one_patient)
        observations[observation_key]["numeric_lab_data"][1]["data"] = get_new_data(
            "sbp", one_patient)
    else:
        observations[observation_key]["numeric_lab_data"][0]["data"] = get_new_data(key, one_patient)

    with open(path, "w") as fp:
        json.dump(observations, fp)
