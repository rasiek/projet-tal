
from typing import Pattern
from bs4 import BeautifulSoup
import requests
import re
from extractor.term import Term
import os


class Extractor:

    def __init__(self, criteria):

        self.parser_engine = "lxml"
        self.criteria = criteria
        self.url = f'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={self.criteria}&rel='
        self.term_data = {}
        self.term = Term()
        self.term.r_term = criteria
        self.regles = []
        self.new_terms = []
        self.not_exists = []
        self.rel_types = {}
        self.rels = {}

        self.__scrap()
        if self.term.exist != False:
            self.__regles_construction()
            self.termes_const()
            self.__terms_rels()
            print(self.rels)
        else:
            print("term not exist")

    def __regles_construction(self):

        with open("extractor/regles.txt", 'r') as f:
            for ligne in f:
                regle_info = re.search("(.*)⇒(.*\*[a-z]*)", ligne)
                prop_1 = None
                prop_2 = None
                if regle_info:
                    props_info = re.search(
                        "(.*)&(.*)==(.*)", regle_info.group(1))
                    if props_info != None:
                        prop_1 = props_info.group(1).strip().replace('*', '')
                        prop_2 = props_info.group(2).strip()
                        prop_2_val = props_info.group(3).strip()

                    else:
                        prop_1 = regle_info.group(1).strip().replace('*', '')

                    trans = regle_info.group(2).strip().replace('*', '')

                    if prop_2 != None:

                        self.regles.append([
                            prop_2_val,
                            [prop_1, trans]
                        ])
                    else:
                        self.regles.append(
                            [[prop_1, trans]]
                        )
                else:
                    pass

    def termes_const(self):

        for regle in self.regles:
            new_term = None
            if len(regle) > 1:

                count = 0
                for i in regle:

                    if count == 0:
                        if i in self.term.r_pos:
                            count += 1
                            continue
                        else:
                            break

                    new_term = re.sub(f'{i[0]}$', i[1], self.term.r_term)
                    new_term = None if new_term == self.term.r_term else new_term
                    count += 1

            else:
                new_term = re.sub(f'{regle[0][0]}$',
                                  regle[0][1], self.term.r_term)
                new_term = None if new_term == self.term.r_term else new_term

            if new_term != None:
                self.new_terms.append(new_term)

    def __req_and_parse(self, term=None):

        if term == None and os.path.exists(f'extractor/cache/{self.term.r_term}.txt'):

            code_text = []
            with open(f'extractor/cache/{self.term.r_term}.txt', 'r') as f:

                for ligne in f:
                    code_text.append(ligne)

            return code_text

        elif term and os.path.exists(f'extractor/cache/{term}.txt'):
            code_text = []
            with open(f'extractor/cache/{term}.txt', 'r') as f:

                for ligne in f:
                    code_text.append(ligne)

            return code_text

        try:
            url = f'http://www.jeuxdemots.org/rezo-dump.php?gotermsubmit=Chercher&gotermrel={term}&rel='
            page_req = requests.get(self.url if term == None else url)

        except Exception as e:
            print(e)

        if page_req.status_code == 200:

            if term:

                try:
                    page_soup = BeautifulSoup(
                        page_req.text, self.parser_engine)
                    code_text = page_soup.find('code').text.split("\n")

                    with open(f"extractor/cache/{term}.txt", 'w') as f:
                        f.writelines(code_text)

                    return code_text
                except:
                    return None

            else:

                page_soup = BeautifulSoup(page_req.text, self.parser_engine)
                if page_soup.find('code'):
                    code_text = page_soup.find('code').text.split("\n")
                else:
                    return None

                with open(f"extractor/cache/{self.term.r_term}.txt", 'w') as f:
                    f.writelines(code_text)

                return code_text

        else:
            return 'Conn Error'

    def __scrap(self):

        code_text = self.__req_and_parse()

        if code_text == None:

            self.term.exist = False
            return

        for ligne in code_text:

            if self.term.id == None:
                id_info = re.search('eid=(.*)\)', ligne)
                if id_info != None:
                    self.term.id = id_info.group(1)

            if re.match('[1-9]', ligne):
                self.term.definition.append(ligne)

            if re.match('e', ligne):
                pos_info = re.search(".*;\'(.*)\';4;.*", ligne)
                if pos_info != None:
                    self.term.r_pos.append(pos_info.group(1))

            if re.match('rt', ligne):
                key_info = re.search('rt;([0-9]*);(.*)', ligne)

                if key_info != None:
                    self.rel_types[key_info.group(1)] = key_info.group(2)

    def __scrap_new_terms(self, code_text):

        term_id = None
        pos = []
        rels = []
        defs = []

        for ligne in code_text:

            if term_id == None:
                id_info = re.search('eid=(.*)\)', ligne)
                if id_info != None:
                    term_id = id_info.group(1)

            if re.match('[1-9]', ligne):
                defs.append(ligne)

            elif re.match('e', ligne):
                pos_info = re.search(".*;\'(.*)\';4;.*", ligne)
                if pos_info != None:
                    pos.append(pos_info.group(1))

            elif re.match('r', ligne):
                pattern = f"{term_id};{self.term.id};(.*);"
                rel = re.search(pattern, ligne)

                if rel != None:
                    rels.append(self.rel_types[rel.group(1)])

        return pos, rels, defs

    def __terms_rels(self):

        for term in self.new_terms:

            req = self.__req_and_parse(term)

            if req != None:
                pos, rels, defs = self.__scrap_new_terms(req)
                self.rels[term] = [pos, rels, defs]

            else:
                self.not_exists.append(term)
