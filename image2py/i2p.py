#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import base64

try:
    from ConfigParser import ConfigParser
except:
    from configparser import ConfigParser


class Bare():

    def get_encode(self):
        return base64.b64encode


class Img2Py():

    def __init__(self, files, indent=True, toolkit=None, encode=None,
                 continue_on_errors=False):
        self.files = files
        self.indent = indent
        if toolkit is None:
            toolkit = Bare()
        self.toolkit = toolkit
        self.coe = continue_on_errors
        self.encode = encode if encode else toolkit.get_encode()

    def generate(self):
        self.errors = []
        self.raw_data = {}
        for f in self.files:
            self.process_file(f)
        return self

    def output(self, filename=None):
        output = "hihi"
        if len(self.raw_data) < 1:
            raise Exception('No data')
        if filename is None:
            return output

    def process_file(self, fname):
        if not os.path.isfile(fname):
            self.errors.append("File %s does not exists" % (fname))
            if self.coe:
                return
        with (open(fname, 'rb')) as f:
            data = f.read()
        # below won't handle the same name files
        # in different paths
        filename = os.path.basename(fname)
        self.raw_data[filename] = self.encode(data)


def main():
    #    config = ConfigParser()
    try:
        o = Img2Py([])
        print(o.generate().output())
    except Exception as e:
        print("Error: %s" % e)
        return

if __name__ == "__main__":
    main()
