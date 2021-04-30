
from bs4 import BeautifulSoup
import requests
import re
from term import Term


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

        self.__scrap()
        self.__regles_construction()
        print(self.term.r_pos)
        self.termes_const()

        print(self.new_terms)

    def __regles_construction(self):

        with open("regles_test.txt", 'r') as f:
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
            # print(len(regle))
            if len(regle) > 1:
                count = 0

                for i in regle:
                    if count == 0:
                        print(regle)
                        print(i)
                        if i in self.term.r_pos:
                            continue
                        else:
                            break

                    print(i, "2")
                    new_term = re.sub(f'{i[0]}$', i[1], self.term.r_term)
                    count += 1

            else:
                new_term = re.sub(f'{regle[0][0]}$',
                                  regle[0][1], self.term.r_term)

            if new_term != None:
                self.new_terms.append(new_term)

    def __scrap(self):

        self.term_data["n_entries"] = []

        try:

            page_req = requests.get(self.url)

        except Exception as e:
            print(e)

        page_soup = BeautifulSoup(page_req.text, self.parser_engine)

        code_text = page_soup.find('code').text.split("\n")

        for ligne in code_text:

            if self.term.id == None:
                id_info = re.search('eid=(.*)\)', ligne)
                if id_info != None:
                    self.term.id = id_info.group(1)

            if re.match('e', ligne):
                pos_info = re.search(".*;\'(.*)\';4;.*", ligne)
                if pos_info != None:
                    self.term.r_pos.append(pos_info.group(1))


Extractor("dîner")
