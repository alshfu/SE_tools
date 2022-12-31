from Model.Archive.Verifications_from_archive import Verification


class Vat(Verification):
    def __init__(self, data, index):
        super().__init__(data, index)
        self.list_of_transactions_vat = self.data.getlist(f"""vat_of_transaction_for_verifications_{self.index + 1}""")