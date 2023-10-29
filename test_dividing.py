import unittest

from splitting import split_html
from exceptions import SplittingException


class TestDividing(unittest.TestCase):

    def test_emty(self):
        check = ''
        correct = ['']
        self.assertEqual(list(split_html(check, 250)), correct)

    def test_simple(self):
        check = '''<p>
            <a href="https://www.google.com/">Google search1</a>
            <b>
                <a href="https://www.google.com/">Google search</a>
                <ul>
                    <li>Lorem ipsum dolor sit amet, consectetur adipiscing.</li>
                </ul>
            </b>
        </p>'''
        self.assertEqual(list(split_html(check, 500)), [check])

    def test_wrong_html(self):
        check = '''<p>
            <a href="https://www.google.com/">Google search1</a>
            <b>
                <a href="https://www.google.com/">Google search</a>
                <ul>
                    <li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li>
                    <li>Ut enim ad minim veniam, quis nostrud exercitation ullamc.</li>
                    <li>Duis aute irure dolor in reprehenderit in voluptate.'''
        correct = ['<p><a href="https://www.google.com/">Google search1</a><b><a href="https://www.google.com/">Google search</a><ul><li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li></ul></b></p>',
                   '<p><b><ul><li>Ut enim ad minim veniam, quis nostrud exercitation ullamc.</li><li>Duis aute irure dolor in reprehenderit in voluptate.</li></ul></b></p>']
        self.assertEqual(list(split_html(check, 250)), correct)

    def test_two_elements_with_attr(self):
        check = '''<p class="css3nav">
            <a href="https://www.google.com/">Google search1</a>
            <b>
                <a href="https://www.google.com/">Google search</a>
                <ul>
                    <li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li>
                    <li>Ut enim ad minim veniam, quis nostrud exercitation ullamc.</li>
                    <li>Duis aute irure dolor in reprehenderit in voluptate.</li>
                </ul>
            </b>
        </p>'''
        correct = ['<p class="css3nav"><a href="https://www.google.com/">Google search1</a><b><a href="https://www.google.com/">Google search</a><ul><li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li></ul></b></p>',
                   '<p class="css3nav"><b><ul><li>Ut enim ad minim veniam, quis nostrud exercitation ullamc.</li><li>Duis aute irure dolor in reprehenderit in voluptate.</li></ul></b></p>']
        self.assertEqual(list(split_html(check, 250)), correct)

    def test_different_levels(self):
        check = '''<p>
            <a href="https://www.google.com/">Google search1</a>
            <b>
                <a href="https://www.google.com/">Google search</a>
                <ul>
                    <li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li>
                    <li>Ut enim ad minim veniam, quis nostrud exercitation ullamc.</li>
                    <li>Duis aute irure dolor in reprehenderit in voluptate.</li>
                </ul>
            </b>
            <b>
                <a href="https://www.google.com/">Google search</a>
                <ul>
                    <li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li>
                    <li>Ut enim ad minim veniam, quis nostrud exercitation ullamc.</li>
                    <li>Duis aute irure dolor in reprehenderit in voluptate.</li>
                </ul>
            </b>
        </p>'''
        correct = ['<p><a href="https://www.google.com/">Google search1</a><b><a href="https://www.google.com/">Google search</a><ul><li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li></ul></b></p>',
                   '<p><b><ul><li>Ut enim ad minim veniam, quis nostrud exercitation ullamc.</li><li>Duis aute irure dolor in reprehenderit in voluptate.</li></ul></b><b><a href="https://www.google.com/">Google search</a></b></p>',
                   '<p><b><ul><li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li><li>Ut enim ad minim veniam, quis nostrud exercitation ullamc.</li><li>Duis aute irure dolor in reprehenderit in voluptate.</li></ul></b></p>']
        self.assertEqual(list(split_html(check, 250)), correct)

    def test_split_in_tag(self):
        check = '''<p>
            <a>Google search1</a>
            <strong>
                <a>Goo</a>
            </strong>
        </p>'''
        correct = ['<p><a>Google search1</a></p>',
                   '<p><strong><a>Goo</a></strong></p>']
        self.assertEqual(list(split_html(check, 35)), correct)

    def test_Exception(self):
        check = '''
        <p>
            <a href="https://www.google.com/">Google search1</a>
            <b>
                <a href="https://www.google.com/">Google search</a>
                <ul>
                    <li>Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit.Lorem ipsum dolor sit amet, consectetur adipiscing elit.</li>
                    <li>Ut enim ad minim veniam, quis nostrud exercitation ullamc.</li>
                    <li>Duis aute irure dolor in reprehenderit in voluptate.</li>
                </ul>
            </b>
        </p>'''
        with self.assertRaises(SplittingException):
            list(split_html(check, 250))


if __name__ == '__main__':
    unittest.main()
