import json
import re
from pathlib import Path

from os import listdir as os_listdir
from os.path import isdir as os_isdir


class Notes:

    def __init__(self, progress_notes_path):
        self.patient_folder_paths = {}
        self.__init_patient_folder_paths__(progress_notes_path=progress_notes_path)

    def __init_patient_folder_paths__(self, progress_notes_path: str):
        overall_note_folder = os_listdir(progress_notes_path)
        id_matcher = re.compile("\d{4,}")
        for case_note_folder in overall_note_folder:
            potential_case_folder = Path(
                progress_notes_path) / case_note_folder
            if os_isdir(potential_case_folder):
                patient_id_match = id_matcher.search(
                    potential_case_folder.stem)
                if patient_id_match != None:
                    patient_id = int(patient_id_match.group(0))
                    self.patient_folder_paths[patient_id] = potential_case_folder


    def create_notes(self, data_layout, patient_path):
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
