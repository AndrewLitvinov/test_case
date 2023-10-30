from collections.abc import Generator

from bs4 import BeautifulSoup
from bs4.element import Tag

from exceptions import SplittingException

BLOCK_TAGS = ('p', 'b', 'ul', 'strong', 'i', 'ul', 'ol', 'div', 'span')
SPLITTER = ''


class HtmlParams:
    '''All data for calculations.'''
    def __init__(self, max_len):
        self.max_len = max_len
        self.text = ''
        self.curr_block_tags = []
        self.end_block_tags = []
        self.block_ends_tags_len = 0
        self.result = []


def create_html_by_tags(tags: list[str]) -> str:
    '''Create start or end tags by list.'''
    return SPLITTER.join(tags)


def check_possibility(html: HtmlParams) -> None:
    '''Checking the possibility of splitting.'''
    if len(html.text) + html.block_ends_tags_len > html.max_len:
        raise SplittingException('Impossible to split: ' + html.text)


def get_tag_view(tag: Tag, tag_text: str) -> str:
    '''Get the name of the block tag with their attributes.'''
    if len(tag.attrs) > 0:
        return tag_text[:tag_text.find('>') + 1]
    return f'<{tag.name}>'


def exclude_empty_tags(html: HtmlParams) -> str:
    '''Remove block tags that may remain at the end of the message
    because of splitting.'''
    text = html.text
    i = len(html.curr_block_tags) - 1
    while (text[len(text)-len(html.curr_block_tags[i]):] ==
           html.curr_block_tags[i]):
        text = text[:len(text)-len(html.curr_block_tags[i])]
        i -= 1
    end_tags = html.end_block_tags[len(html.curr_block_tags) - 1 - i:]
    return text + create_html_by_tags(end_tags)


def split_tags(parent_tag: Tag, html_params: HtmlParams) -> None:
    '''Recursive function for splitting.'''
    for tag in parent_tag.contents:
        if tag == '\n':
            continue

        tag_text = str(tag)
        curr_len = (len(html_params.text + tag_text) +
                    html_params.block_ends_tags_len)
        if curr_len <= html_params.max_len:
            html_params.text += SPLITTER + tag_text
            continue
        elif tag.name in BLOCK_TAGS:
            tag_view = get_tag_view(tag, tag_text)
            end_element = f'</{tag.name}>'
            curr_len = (len(html_params.text + tag_view + end_element) +
                        html_params.block_ends_tags_len)
            if curr_len > html_params.max_len:
                html_params.result.append(exclude_empty_tags(html_params))
                html_params.text = (
                    create_html_by_tags(html_params.curr_block_tags)
                    + SPLITTER + tag_view)
            else:
                html_params.text += SPLITTER + tag_view

            html_params.curr_block_tags.append(tag_view)
            html_params.end_block_tags.insert(0, end_element)
            html_params.block_ends_tags_len += len(end_element)
            split_tags(tag, html_params)

        else:
            curr_len = (len(html_params.text + tag_text) +
                        html_params.block_ends_tags_len)
            if curr_len > html_params.max_len:
                html_params.result.append(exclude_empty_tags(html_params))
                html_params.text = (
                    create_html_by_tags(html_params.curr_block_tags)
                    + SPLITTER + tag_text)
            else:
                html_params.text += SPLITTER + tag_text

        check_possibility(html_params)

    if parent_tag.name != 'body':
        tag_view = get_tag_view(parent_tag, parent_tag.prettify())
        html_params.curr_block_tags.pop(len(html_params.curr_block_tags) - 1)
        end_element = f'</{parent_tag.name}>'
        endtag = html_params.end_block_tags.pop(0)
        html_params.text = html_params.text + endtag
        html_params.block_ends_tags_len -= len(end_element)
    else:
        mess = (html_params.text +
                create_html_by_tags(html_params.end_block_tags))
        html_params.result.append(mess)


def split_html(source: str, max_len: int) -> Generator[str]:
    '''Splits the original message (`source`) into fragments of the specified
    length (`max_len`).'''

    if len(source) <= max_len:
        yield source
    else:
        html_params = HtmlParams(max_len=max_len)
        soup = BeautifulSoup(source, 'lxml')
        split_tags(soup.html.body, html_params)

        for part in html_params.result:
            yield part
