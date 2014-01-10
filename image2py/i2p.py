#!/usr/bin/env python
#-*- coding:utf-8 -*-

import os
import base64


class BasicTemplate(object):

    def __init__(self):
        self._part_files = []
        self._part_imports = []
        self._part_func = []

    def part_files(self, files):
        self._part_files.append("data = {}")
        for name, data in files.items():
            output = ["data['{!s}'] = \"\" ".format(name)]
            while data:
                part = data[:70]
                data = data[70:]
                output.append('    "{!s}" '.format(part.decode()))
            self._part_files.append("\\\n".join(output))

    def part_imports(self):
        self._part_imports.append("import base64")

    def part_functions(self):
        self._part_func = [
            "def get_data(name):\n    return data[name]",
            "def get_decoded(name):\n    return base64.b64decode(data[name])",
            "def list_files():\n    return list(data.keys())"
            ]

    def render(self, files):
        self.part_imports()
        self.part_functions()
        self.part_files(files)
        header = "# created with image2py\n" \
                 "template = '{!s}'".format(self.__class__.__name__)
        blocks = [header,
                  "\n".join(self._part_imports),
                  "\n\n".join(self._part_files),
                  "\n\n".join(self._part_func)]
        return "\n\n\n".join(blocks)


class Converter(object):

    def __init__(self, input_file=None):
        self.files = {}
        self.template = BasicTemplate()
        if input_file is not None and os.path.isfile(input_file):
            self.load_file(input_file)

    def load_file(self, input_file):
        # TODO
        pass

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
