import re
from flask import render_template, request
from app import app
from extractor.extractor_f import Extractor


@app.route('/', methods=['POST', 'GET'])
def index():

    if request.method == 'POST':

        term = request.form['term']

        infos = Extractor(term)

        if infos.term.exist != False:

            context = {
                'id': infos.term.id,
                'term': infos.term.r_term,
                'defs': infos.term.definition,
                'pos': infos.term.r_pos,
                'rels': infos.rels,
                'not_exist': infos.not_exists,
            }
        else:
            context = {
                'exist': False,
                'term': term,
            }

        return render_template('index.html', **context)

    else:

        return render_template('index.html')
