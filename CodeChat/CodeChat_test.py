# -*- coding: utf-8 -*-

# Testing
# -------
# This test bench exercises the FindLongestMatchingString module.

import pytest
from FindLongestMatchingString import find_approx_text_in_target as f

# A diagnostic function to match then print the returned match.
def p(search_text, search_anchor, target_text):
    index = f(search_text, search_anchor, target_text)
    print('\nFinal match:\n' + search_text[search_anchor:] + '\n' + target_text[index:])
    return index


# Find a location in a source file based on a given location in the resulting
# html.
class TestFindLongestMatchingString(object):
    # Show that we can match identical text
    def test_1(self):
        index = f(search_anchor = 2,
                  search_text = 'test',
                  target_text = 'test')
        assert index == 2

    # Show that we can match with a initial Python comment
    def test_2(self):
        index = f(search_anchor = 4,
                  search_text = '# test',
                  target_text = 'test')
        assert index == 2

    # Show that we can match with a initial C/C++ comment
    def test_3(self):
        index = f(search_anchor = 5,
                  search_text = '// test',
                  target_text = 'test')
        assert index == 2

    # Show that we can match at the end of a line
    def test_4(self):
        index = f(search_anchor = 4,
                  search_text = 'test\ntest',
                  target_text = 'test\ntest')
        assert index == 4

    # Show that we can match at the end of a line with a Python comment
    def test_5(self):
        index = f(search_anchor = 6,
                  search_text = '# test\n# test',
                  target_text = 'test\ntest')
        assert index == 4

    def test_6(self):
        index = f(search_anchor = 73-34,
                  search_text = '# The :doc:`README` user manual gives a broad overview of this system. In contrast, this document discusses the implementation specifics of the CodeChat system.',
                  target_text = 'The CodeChat user manual gives a broad overview of this system. In contrast, this document discusses the implementation specifics of the CodeChat system.')
        assert index == 66-34
        
# Test the fixup code which removed junk lines used only to produce a desired indent.
from CodeToRest import sphinx_html_page_context
class TestHtmlCleanup(object):
    # Given a string, return it after sphinx_html_page_context processes it.
    def s(self, string):
        context = {'body' : string}
        sphinx_html_page_context(None, None, None, context, None)
        return context['body']
        
    # Show that normal text isn't changed
    def test_1(self):
        string = 'testing'
        ret = self.s(string)
        assert ret == string
        
    def test_2(self):
        string = 'testing'
        ret = self.s(string)
        assert ret == string

from cStringIO import StringIO        
from CodeToRest import code_to_rest
from LanguageSpecificOptions import LanguageSpecificOptions
from pygments.lexers.compiled import CLexer, CppLexer
from pygments.lexers.agile import PythonLexer
class TestHtmlCleanup(object):
    # Given a string and a language, run it through code_to_rest and return the resulting string.
    def t(self, in_string, language = CLexer()):
        # Use a StringIO object to act like file IO which code_to_rest expects.
        lso = LanguageSpecificOptions()
        lso.set_language(language)
        in_stringIO = StringIO(in_string)
        out_stringIO = StringIO()
        code_to_rest(lso, in_stringIO, out_stringIO)
        # For convenience, create the removal string for the chosen language
        unique_remove_comment = lso.comment_string + lso.unique_remove_str + '\n'
        return out_stringIO.getvalue(), unique_remove_comment
        
    # A single line of code, without an ending \n
    def test_1(self):
        ret, comment = self.t('testing')
        assert ret ==  ' ::\n\n ' + comment + ' testing\n'

    # A single line of code, with an ending \n.
    def test_2(self):
        ret, comment = self.t('testing\n')
        assert ret == ' ::\n\n ' + comment + ' testing\n'

    # Several lines of code, with arbitrary indents
    def test_3(self):
        ret, comment = self.t('testing\n  test 1\n test 2\n   test 3')
        assert ret == ' ::\n\n ' + comment + ' testing\n   test 1\n  test 2\n    test 3\n'

    # A single line comment, no trailing \n
    def test_4(self):
        ret, comment = self.t('// testing')
        assert ret == '\ntesting\n'

    # A single line comment, trailing \n
    def test_5(self):
        ret, comment = self.t('// testing\n')
        assert ret == '\ntesting\n'

    # A multi line comment
    def test_5a(self):
        ret, comment = self.t('// testing\n// more testing')
        assert ret == '\ntesting\nmore testing\n'

    # A single line comment with no space after the comment should be treated like code
    def test_6(self):
        ret, comment = self.t('//testing')
        assert ret == ' ::\n\n ' + comment + ' //testing\n'

    # A singly indented single-line comment
    def test_7(self):
        ret, comment = self.t(' // testing')
        assert ret == '\n\n' + comment + '\n testing\n'

    # A doubly indented single-line comment
    def test_8(self):
        ret, comment = self.t('  // testing')
        assert ret == '\n\n' + comment + '\n ' + comment + '\n  testing\n'

    # A doubly indented multi-line comment
    def test_9(self):
        ret, comment = self.t('  // testing\n  // more testing')
        assert ret == '\n\n' + comment + '\n ' + comment + '\n  testing\n  more testing\n'

def main():
    pytest.main()

if __name__ == '__main__':
    main()
