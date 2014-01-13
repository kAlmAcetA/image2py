#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import base64
from . import templates


class Converter(object):

    def __init__(self, input_file=None):
        self.files = {}
        self.template = templates.BasicTemplate()
        if input_file is not None and os.path.isfile(input_file):
            self.load_file(input_file)

    def load_file(self, input_file):
        """
        import importlib.machinery
        loader = importlib.machinery.SourceFileLoader("image2py_taf",
                                                      input_file)
        pyimg = loader.load_module("image2py_taf")
        """
        import imp
        pyimg = imp.load_source('image2py_taf', input_file)
        self.files = pyimg.data
        self.set_template(templates.templateByName(pyimg.template))

    def set_template(self, template):
        self.template = template

    def save(self, filename=None):
        if filename is None:
            raise Exception('Converter#save: Undefined filename')
        with (open(filename, 'wb')) as f:
            f.write(self.output())

    def add_file(self, fname):
        with (open(fname, 'rb')) as f:
            data = f.read()
        # below won't handle the same name files
        # in different paths
        filename = os.path.basename(fname)
        self.files[filename] = base64.b64encode(data)

    def remove_file(self, fname):
        del self.files[fname]

    def output(self):
        if len(self.files) < 1:
            raise Exception('Converter#output: No files to convert')
        return self.template.render(self.files)
