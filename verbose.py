'''
File: verbose.py
Author: Tristan van Vaalen

Prefixed printing using ANSI escape code
Can chain debug output:
    debug('test').indent().info('indented').unindent()
'''

import sys
_indent_level = 0


class Verbose:

    _debug_color = "\x1b[32mDEBG\x1b[0m "
    _info_color = "\x1b[34mINFO\x1b[0m "
    _warn_color = "\x1b[33mWARN\x1b[0m "
    _error_color = "\x1b[31mERR!\x1b[0m "
    _critical_color = "\x1b[31mCRIT\x1b[0m "

    def indent(self):
        global _indent_level
        _indent_level += 1

        return self

    def unindent(self):
        global _indent_level
        assert _indent_level > 0
        _indent_level -= 1

        return self

    def _get_indent(self):
        global _indent_level
        return _indent_level

    def _write_std(self, prefix, string, postfix='\n'):
        indent_level = self._get_indent()

        if indent_level > 0:
            prefix = ''
            indent = '     ' + '  ' * (indent_level - 1)
        else:
            indent = ''

        sys.stdout.write(indent + prefix + str(string) + postfix)

    def rewrite(self, string):
        self._write_std('\r', string, postfix='')
        return self

    def write(self, string):
        self._write_std('', string)
        return self

    def debug(self, string):
        self._write_std(self._debug_color, string)
        return self

    def info(self, string):
        self._write_std(self._info_color, string)
        return self

    def warning(self, string):
        self._write_std(self._warn_color, string)
        return self

    def error(self, string):
        self._write_std(self._error_color, string)
        return self

    def critical(self, string):
        self._write_std(self._critical_color, string)
        return self
