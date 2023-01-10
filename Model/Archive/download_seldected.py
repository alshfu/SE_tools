from Model.Archive.Verification import Verification


class Verification_to_download(Verification):
    def __init__(self, data, index, f_data):
        super().__init__(data, index, f_data)
        self.selected = data.getlist('selected')[index]
    def get_selected(self):
        if self.selected == 'true':
            print(f"""id of verification: {self.id_from_file} and selected: {self.selected}""")