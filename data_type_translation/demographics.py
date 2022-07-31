import json

class Demographics:
    
    def __init__(self):
        pass

    def create_demographics(self, case_id, patient_path, hospitalrisk_demo_df):
        print(f"Creating case: {case_id}")

        # Will need to create demographics for each user
        demographics_info = hospitalrisk_demo_df[hospitalrisk_demo_df["patient_id"] == case_id]
        # TODO: Need - Weight, Height, and BMI
        # Getting iloc[0] as not doing so returns a series with the index and value
        demographics_dict = {
            "weight": 0,
            "age": int(demographics_info["age"].iloc[0]),
            "bmi": 0,
            "sex": demographics_info["sex"].iloc[0],
            "race": demographics_info["race"].iloc[0],
            "height": 0,
            "id": case_id
        }

        try:
            demographics_path = patient_path / "demographics.json"
            demographics_path.touch(exist_ok=True)
        except PermissionError:
            raise PermissionError(
                "Permission denied when creating demograhpics file")

        with open(demographics_path, "w+") as fp:
            json.dump(obj=demographics_dict, fp=fp, indent=4)
