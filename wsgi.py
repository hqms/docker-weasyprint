#!/usr/bin/env python

import json
import logging

from flask import Flask, request, make_response, jsonify, render_template
from flask_cors import CORS

import weasyprint
from weasyprint import HTML

app = Flask('pdf')
CORS(app)

@app.route('/health')
def index():
    return 'ok'

@app.route('/version')
def version_index():
    return weasyprint.__version__


@app.before_first_request
def setup_logging():
    logging.addLevelName(logging.DEBUG, "\033[1;36m%s\033[1;0m" % logging.getLevelName(logging.DEBUG))
    logging.addLevelName(logging.INFO, "\033[1;32m%s\033[1;0m" % logging.getLevelName(logging.INFO))
    logging.addLevelName(logging.WARNING, "\033[1;33m%s\033[1;0m" % logging.getLevelName(logging.WARNING))
    logging.addLevelName(logging.ERROR, "\033[1;31m%s\033[1;0m" % logging.getLevelName(logging.ERROR))

    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.DEBUG)


@app.route('/')
def home():
    return '''
        OK
    '''


@app.route('/a', methods=['POST'])
def generate():
    name = request.args.get('filename', 'unnamed.pdf')
    app.logger.info('POST  /pdf?filename=%s' % name)
    data = json.loads(request.data)
    app.logger.info(data)

    rendered = render_template('label.html', data=data, barang=data.items)

    html = HTML(string=rendered)
    pdf = html.write_pdf()
    response = make_response(pdf)
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = 'inline;filename=%s' % name
    app.logger.info(' ==> POST  /pdf?filename=%s  ok' % name)
    return response


if __name__ == '__main__':
    app.run()
