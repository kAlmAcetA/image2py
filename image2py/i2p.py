#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import base64

try:
    from ConfigParser import ConfigParser
except:
    from configparser import ConfigParser


class Bare():

    def __init__(self):
        self._part_files = ""
        self._part_headers = ""
        self._part_functions = ""

    def encode(self, data):
        return base64.b64encode(data)

    def part_files(self, files):
        output = "data = {}\n\n"
        for name, data in files.items():
            output += "data['{!s}'] = "" \\\n".format(name)
            while data:
                part = data[:70]
                data = data[70:]
                output += '    "{!s}" \\\n'.format(part)
        self._part_files = output

    def part_header(self):
        self.part_headers = "import base64"

    def part_functions(self):
        self._part_functions = "def get_data(name):\n    return d[name]"
        self._part_functions += "def get_decoded(name):\n    " \
                                "return base64.b64decode(d[name])"


class Converter(object):

    def __inoit__(self, filename=None):
        self.output = ""
        self.files = {}
        self.filename = filename
        self.toolkit = Bare()
        if os.path.isfile(filename) and filename is not None:
            pass

    def set_toolkit(self, toolkit):
        self.toolkit = toolkit

    def save(self, to_file=None):
        if to_file is None and self.filename is not None:
            to_file = self.filename

    def add_file(self, fname):
        with (open(fname, 'rb')) as f:
            data = f.read()
        # below won't handle the same name files
        # in different paths
        filename = os.path.basename(fname)
        self.files[filename] = self.toolkit.encode(data)

    def remove_file(self, fname):
        del self.files[fname]

    def output(self):
        if len(self.files) < 1:
            raise Exception('No data')
        return self.output


def main():
    #    config = ConfigParser()
    try:
        o = type()
        print(o.generate().output())
    except Exception as e:
        print("Error: %s" % e)
        return

if __name__ == "__main__":
    main()
