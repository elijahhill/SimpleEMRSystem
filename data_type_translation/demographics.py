import json

class Demographics:
    
    def __init__(self):
        # Heights are tuples: feet, inches
        self.heights = {
            1065120: (6, 1),
            741698: (5, 6),
            68584: (5, 6),
            104203: (5, 6),
            2259947: (5, 11),
            2799629: (5, 10),
            182065: (5, 6),
            864861: (5, 9)

        }
        # Weights are in pounds
        self.weights = {
            1065120: 186,
            741698: 155,
            68584: 195,
            104203: 139,
            2259947: 245,
            2799629: 363,
            182065: 145,
            864861: 146              
        }

    def __calculate_bmi(self, case_id):
        kg = self.weights[case_id] * 0.45359237
        feet_and_inches = self.heights[case_id]
        inches = (feet_and_inches[0] * 12) + feet_and_inches[1]
        m = (inches * 2.54) / 100
        bmi = kg / (m * m)
        return round(bmi, 2)

    def create_demographics(self, case_id, patient_path, hospitalrisk_demo_df):
        print(f"Creating case: {case_id}")

        demographics_info = hospitalrisk_demo_df[hospitalrisk_demo_df["patient_id"] == case_id]

        weight_exists = True if case_id in self.heights.keys() else False
        height_exists = True if case_id in self.weights.keys() else False

        if height_exists:
            height = self.heights[case_id]
        else:
            height = 0
        
        if weight_exists:
            weight = self.weights[case_id]
        else:
            weight = 0

        if height_exists and weight_exists:
            bmi = self.__calculate_bmi(case_id)
        else:
            bmi = 0

        demographics_dict = {
            "weight": weight,
            "age": int(demographics_info["age"].iloc[0]),
            "bmi": bmi,
            "sex": demographics_info["sex"].iloc[0],
            "race": demographics_info["race"].iloc[0],
            "height": height,
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
