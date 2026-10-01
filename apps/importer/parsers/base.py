class BaseParser:

    def __init__(self, record):

        self.record = record

    def run(self):

        raise NotImplementedError