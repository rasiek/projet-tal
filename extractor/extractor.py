
from bs4 import BeautifulSoup
import requests
import re


class Extractor:

    def __init__(self, criteria):

        self.parser_engine = "lxml"
        self.criteria = criteria
        self.url = f'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={self.criteria}&rel='

        self.__scrap()

    def __scrap(self):

        rel_types = []
        terms = []
        rels = []

        try:

            page_req = requests.get(self.url)

        except Exception as e:
            print(e)

        page_soup = BeautifulSoup(page_req.text, self.parser_engine)

        code_text = page_soup.find('code').text.split("\n")

        for ligne in code_text:

            if re.match('rt', ligne):
                rel_types.append(ligne)
            elif re.match('e', ligne):
                terms.append(ligne)
            elif re.match('r', ligne):
                rels.append(ligne)

        print(rel_types)
        print(terms)
        print(rels)


Extractor("lavage")
