#!flask/bin/python
# -*- coding: utf-8 -*-
from app import app
import config
app.run(debug=False, host=config.host, port=config.port)
