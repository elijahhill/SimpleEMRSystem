class PathContainer:
    def __init__(self):
        pass

    def add_hospitalrisk_path(self, hospitalrisk_path: str):
        self.hospitalrisk_path = hospitalrisk_path

    def get_hospitalrisk_path(self):
        return self.hospitalrisk_path

    def add_output_path(self, output_path: str):
        self.output_path = output_path

    def get_output_path(self):
        return self.output_path

    def add_hospitalrisk_demo(self, hospitalrisk_demo: str):
        self.hospitalrisk_demo = hospitalrisk_demo

    def get_hospitalrisk_demo(self):
        return self.hospitalrisk_demo

    def add_progress_note_cases(self, progress_note_cases: str):
        self.progress_note_cases = progress_note_cases

    def get_progress_note_cases(self):
        return self.progress_note_cases
