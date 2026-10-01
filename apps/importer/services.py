from .parsers.parser_99acres import Parser99Acres


class ImportService:

    def __init__(self, record):
        self.record = record

    def run(self):

        url = self.record.url.lower()

        if "99acres.com" in url:
            Parser99Acres(self.record).run()
            return

        raise Exception("Unsupported Website")