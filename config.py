TESTING = True
DEBUG = True
FLASK_ENV = "development"
SECRET_KEY = "83278af38b3c630e8774e023bb7d9b77"

TEMPLATES_FOLDER = "templates"
UPLOAD_FOLDER = "uploads"
UPLOAD_FOLDER_FOR_TRANSACTIONS_FILES = f"""{UPLOAD_FOLDER}/transactions_files"""
ALLOWED_EXTENSIONS = {"xlsx", "csv", "SE", "se", "sie", "pdf", "jpg"}

# Database
SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"

WORD_OF_EXCEPTIONS = ["en", "TJÄNST", "en", "den", "och", "eller", "men", "för", "eller", "så", "ännu", "vid", "av", "för", "från", "in", "in", "nära", "av",
                      "på", "till", "med", "utan", "om", "ovan", " tvärs över", "efter", "mot", "längs", "i mitten", "bland", "runt", "som", "vid", "före",
                      "under", "under", "bredvid", "utöver", "mellan", "bortom", "men", "av", "beträffande", "överväger", "trots", "ner", "under", "utom",
                      " förutom", "exklusive", "följer", "för", "från", "in", "inuti", "in", "gilla", "minus", "nära", "av", "av", "på", "på", "motsatt",
                      "utanför", "över", "förbi", "per", "plus", "angående", "runda", "spara", "sedan", " än", "genom", "till", "mot", "mot", "under", "under",
                      "till skillnad från", "tills", "upp", "på", "mot", "via", "med", "inom", "utan", "a", "an", "the", "and", "or", "but", "for", "nor", "so",
                      "yet", "at", "by", "for", "from", "in", "into", "near", "of", "on", "to", "with", "without", "about", "above", "across", "after",
                      "against", "along", "amid", "among", "around", "as", "at", "before", "behind", "below", "beneath", "beside", "besides", "between",
                      "beyond", "but", "by", "concerning", "considering", "despite", "down", "during", "except", "excepting", "excluding", "following", "for",
                      "from", "in", "inside", "into", "like", "minus", "near", "of", "off", "on", "onto", "opposite", "outside", "over", "past", "per", "plus",
                      "regarding", "round", "save", "since", "than", "through", "to", "toward", "towards", "under", "underneath", "unlike", "until", "up",
                      "upon", "versus", "via", "with", "KOSTNAD", "KOSTNADER", "within", "without","bakom","AVGIFT","MNADSAVGIFT","MÅNADSAVGIFT"]


def get_list_of_stop_words():
    return list(map(lambda x: x.upper(), WORD_OF_EXCEPTIONS))
