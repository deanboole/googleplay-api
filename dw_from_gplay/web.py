#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging

logging.basicConfig(level=logging.DEBUG)


if __name__ == '__main__':

    from flask import Flask
    from ui.view import ui

    portal = Flask(__name__)
    portal.config.from_object('config')

    portal.register_blueprint(ui)

    portal.run(host='0.0.0.0', port=8000, )
