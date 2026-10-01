from bs4 import BeautifulSoup

from .base import BaseParser
from ..utils import download_html


class Parser99Acres(BaseParser):

    def run(self):

        self.record.status = "Running"
        self.record.save(update_fields=["status"])

        html = download_html(self.record.url)

        soup = BeautifulSoup(
            html,
            "lxml",
        )

        self.parse(soup)

    def parse(self, soup):

        data = {}

        data["title"] = self.get_title(soup)
        data["description"] = self.get_description(soup)
        data["keywords"] = self.get_keywords(soup)

        self.record.log = str(data)

        self.record.status = "Completed"

        self.record.save(
            update_fields=[
                "log",
                "status",
            ]
        )

    def get_title(self, soup):

        if soup.title:
            return soup.title.text.strip()

        return ""

    def get_description(self, soup):

        tag = soup.find(
            "meta",
            attrs={
                "name": "description"
            },
        )

        if tag:
            return tag.get(
                "content",
                ""
            )

        return ""

    def get_keywords(self, soup):

        tag = soup.find(
            "meta",
            attrs={
                "name": "keywords"
            },
        )

        if tag:
            return tag.get(
                "content",
                ""
            )

        return ""