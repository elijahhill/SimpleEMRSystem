import pandas as pd
from pathlib import Path
from os import path

from case_details import CaseDetails
from data_layout import DataLayout
from admitting_diagnoses import AdmittingDiagnoses
from gui import Gui
from variable_details import VariableDetails
from user_details import UserDetails
from observations import Observations
from notes import Notes
from demographics import Demographics


class StudyCreator:
    

    def __get_hospitalrisk_df(self, excel_path: str):
        # df = pd.read_excel(excel_path, engine="openpyxl",
        #                    sheet_name='color_test')
        df = pd.read_excel(excel_path, engine="openpyxl",
                           sheet_name='10_of_10_cases')
        df["EWS percentile"] = df["ecart percentile"].round(1)
        return df


    def create_study(self):
        '''
        Creates a study
        '''
        print("Fill out the file path window to continue")
        # current_path = path.dirname(__file__)
        current_path = Path().absolute() / "data_type_translation"
        psg = Gui()
        data_paths = psg.get_data_paths(current_path=current_path)
        hospitalrisk_path = data_paths.get_hospitalrisk_path()
        output_folder_path = data_paths.get_output_path()
        progress_notes_path = data_paths.get_progress_note_cases()

        hospitalrisk_df = self.__get_hospitalrisk_df(
            excel_path=hospitalrisk_path)

        hospitalrisk_df.dropna(subset=["patient_id"], inplace=True)

        case_ids = set([
            1065120,
            864861,
            68584,
            104203,
            2259947,
            182065,
            741698,
            2799629,
            1802864,
            2821216
        ])

        # case_ids = set([
        #     610044
        # ])

        case_ids_str_list = list(map(lambda elem: str(elem), case_ids))

        user_details = UserDetails(output_folder_path=output_folder_path, case_id_str_list=case_ids_str_list)
        user_details.write_user_details()

        case_details = CaseDetails(output_folder_path=output_folder_path, case_id_str_list=case_ids_str_list)
        case_details.write_case_details(hospitalrisk_df=hospitalrisk_df)

        data_layout = DataLayout(output_folder_path=output_folder_path)
        data_layout.write_data_layout()

        variable_details = VariableDetails(output_folder_path=output_folder_path, current_path=current_path)
        variable_details.write_variable_details()

        admitting_diagnoses = AdmittingDiagnoses(
            output_folder_path=output_folder_path, current_path=current_path)
        admitting_diagnoses.write_admitting_diagnoses()

        try:
            cases_path = Path(f"{output_folder_path}/cases_all")
            cases_path.mkdir(parents=False, exist_ok=False)
        except:
            pass

        hospitalrisk_demo_path = data_paths.get_hospitalrisk_demo()
        hospitalrisk_demo_df = pd.read_csv(hospitalrisk_demo_path)

        demographics_creator = Demographics()
        note_creator = Notes(progress_notes_path=progress_notes_path)
        observation_creator = Observations(current_path=current_path)

        for case_id in case_ids:
            patient_path = cases_path / str(case_id)
            patient_path.mkdir(parents=False, exist_ok=True)

            demographics_creator.create_demographics(
                case_id=case_id, patient_path=patient_path, hospitalrisk_demo_df=hospitalrisk_demo_df)
            note_creator.create_notes(
                patient_path=patient_path, case_id=case_id)
            observation_creator.create_observations(
                patient_path=patient_path, hospitalrisk_df=hospitalrisk_df, case_id=case_id)


creator = StudyCreator()
creator.create_study()
