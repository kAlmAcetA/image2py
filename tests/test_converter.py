#-*- coding:utf-8 -*-
import unittest
from mock import patch, Mock, MagicMock

from file2py import Converter, templates


class ConverterTest(unittest.TestCase):

    filename = '_fake_FILE'
    content = Mock()
    content.template = 'Basic'
    content.data = {'dummy': 'dummy'}
    dummybase64 = 'ZHVtbXk='

    def setUp(self):
        self.conv = Converter()

    def tearDown(self):
        del self.conv

    def test_bare_create(self):
        self.assertEqual(self.conv.files, {})
        self.assertIsInstance(self.conv.template, templates.BasicTemplate)

    def test_create_with_nonexisting_file(self):
        conv = Converter(self.filename)
        self.assertEqual(conv.files, {})
        self.assertIsInstance(conv.template, templates.BasicTemplate)

    def test_create_with_existing_file(self):
        mock = MagicMock(return_value=True)
        with patch('os.path.isfile', mock):
            mock_load = MagicMock()
            patcher = patch('file2py.Converter.load_file', new=mock_load)
            patcher.start()
            Converter(self.filename)
            mock_load.assert_called_with(self.filename)
            patcher.stop()

    def test_load_nonexisting__file(self):
        self.assertRaises(IOError,
                          self.conv.load_file, self.filename)

    def test_load_existing_not_proper_file2py_file(self):
        mock = MagicMock(return_value={})
        with patch('imp.load_source', mock):
            self.assertRaises(AttributeError,
                              self.conv.load_file, self.filename)

    def test_load_existing_proper_file2py_file_with_bad_template(self):
        mock = MagicMock(return_value=Mock())
        with patch('imp.load_source', mock):
            self.assertRaises(Exception, self.conv.load_file, self.filename)

    def test_load_existing_proper_file2py_file_with_proper_data(self):
        mock = MagicMock(return_value=self.content)
        with patch('imp.load_source', mock):
            self.conv.load_file(self.filename)
        self.assertEqual(self.conv.files, self.content.data)
        self.assertIsInstance(self.conv.template, templates.BasicTemplate)

    def test_set_template_with_wrong_param(self):
        self.assertRaises(TypeError, self.conv.set_template)
        self.assertRaises(TypeError, self.conv.set_template, 'WronTemplate')

    def test_set_template_with_good_param(self):
        self.conv.set_template(templates.BasicTemplate())
        self.assertIsInstance(self.conv.template, templates.BasicTemplate)
        self.conv.set_template(templates.QtTemplate())
        self.assertIsInstance(self.conv.template, templates.BasicTemplate)
        self.assertIsInstance(self.conv.template, templates.QtTemplate)

    def test_add_inon_existing_file(self):
        self.assertRaises(IOError, self.conv.add_file, self.filename)

    def test_add_existing_file(self):
        mock_open = MagicMock()
        with patch('__builtin__.open', mock_open):
            manager = mock_open.return_value.__enter__.return_value
            manager.read.return_value = 'dummy'
            self.conv.add_file(self.filename)
            self.assertEqual(len(self.conv.files), 1)
            self.assertEqual(self.conv.files[self.filename], self.dummybase64)

    def test_remove_non_existing_file(self):
        self.assertRaises(KeyError, self.conv.remove_file, self.filename)

    def test_remove_existing_file(self):
        self.conv.files = self.content.data
        self.assertEqual(len(self.conv.files), 1)
        self.conv.remove_file('dummy')
        self.assertEqual(len(self.conv.files), 0)

    def test_output_bare(self):
        self.assertRaises(Exception, self.conv.output)
