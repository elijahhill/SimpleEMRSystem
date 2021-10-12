from numpy.core.numeric import NaN
import pandas as pd
import json
from pathlib import Path

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


df = pd.read_excel(
    r"C:\Users\Elijah\Box\1_Contextual interviews\eCART data to select cases\hospitalrisk_ecart.xlsx", engine="openpyxl")

one_patient = df[df["patient_id"] == 610044]

hours_and_hr = one_patient[["hours_since_first_vitals", "hr"]]

hours_and_hr_no_nan = hours_and_hr.dropna(subset=["hr"]).reset_index(drop=True)

hours_and_hr_no_nan["hours_since_first_vitals"] = hours_and_hr_no_nan["hours_since_first_vitals"].map(add_to_start_time)

new_data = hours_and_hr_no_nan.values.tolist()

# Open the observations file 

path = Path(r"C:\Users\Elijah\simpleemr\SimpleEMRSystem\resources\manual_data_entry_study\cases_all\10000101\observations.json")

observations = None
with open(path, "r") as fp:
    observations = json.load(fp)

observations["VTHR"]["numeric_lab_data"][0]["data"] = new_data

with open(path, "w") as fp:
    json.dump(observations, fp)
