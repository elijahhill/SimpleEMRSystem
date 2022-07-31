from typing import Dict, List
import json

class UserDetails:

    def __init__(self, output_folder_path: str, case_id_str_list: List[str]):
        self.output_folder_path = output_folder_path
        self.case_id_str_list = case_id_str_list
        self.users = ["testuser1"]

    def __create_user_details(self) -> Dict:
        print("creating user details")
        all_user_details = {}
        for user in self.users:
            user_details = {
                "last_accessed": None,
                "cases_assigned": self.case_id_str_list,
                "cases_completed": []
            }
            all_user_details[user] = user_details
        return all_user_details

    def write_user_details(self):
        user_details = self.__create_user_details()
        with open(f"{self.output_folder_path}/user_details.json", "w+") as fp:
            json.dump(obj=user_details, fp=fp, indent=4)

