from requests import (
    request,
    Request,
    Response
)
from .text_handler import textHandler, TextHandler


class BlastForum:

    def __init__(self):
        self.base_url = 'https://blast.hk'
        self._text_handler: TextHandler = textHandler

    def _request(self, url: str = None) -> Response:
        try:
            return request(
                url =self.base_url + url,
                method = "GET"
            )
        except Exception as e:
            raise e

    def go_to(self, url: str = '/'):
        return self._request(url)

    def extract_text(self, contents: Response) -> str:
        return contents.text;

    def _get_groups(self, pattern: str, page_html: str):
        try:
            return self._text_handler.search_pattern(pattern, page_html)
        except Exception as e:
            return []

    def _remove_pattern(self, pattern: str, page_html: str):
        try:
            return self._text_handler.replace_pattern(pattern, page_html);
        except Exception as e:
            raise e

    def get_heading_link(self, heading:str, page_html: str):
        pattern = fr'<a [\s\w\W\"]*href=\"(.*?)\"[\"\s\W\w]+>{heading}</a>'
        return self._get_groups(pattern, page_html);

    def get_topic_links(self, page_html: str ):
        pattern = r'<a href=\"(/threads/\d+/)\" class='
        return self._get_groups(pattern, page_html)[0:5];

    def get_last_page_link(self, thread_link: str, page_html: str):
        pattern = fr'(?<=pageNav-page \"><a href=\"){thread_link}page-\d+(?=\">\d+</a>)'
        return self._get_groups(pattern, page_html);

    # def get_messages_with_quotes(self, page_html: str):
    #     pattern = r'<div class=\"bbWrapper\">[</\w\s\W\">\n]*?te>(.*?)</div>\n'
    #     return self._get_groups(pattern, page_html);

    def remove_quotes(self, page_html: str):
        pattern = r'<blockquote[\"\w\W\s<>]*?</blockquote>'
        return self._remove_pattern(pattern, page_html);

    def get_messages_with_no_quotes(self, page_html: str):
        pattern = r'<div class=\"bbWrapper\">(.*?)</div>\n'
        return self._get_groups(pattern, page_html);

    def get_articles(self, page_html: str):
        pattern = r'<div [\w\s\W\"=]*?>[\n\s]+(<article[\s\w\W\"-<>]*?</article>)\n+\s+</div>'
        return self._get_groups(pattern, page_html);

    def get_author_and_time(self, page_html: str):
        pattern = r'data-lb-caption-desc=\"(.*?)\">'
        return self._get_groups(pattern, page_html);

    def get_article_title(self, page_html: str):
        pattern = r'<a href=\"/threads/\d+/\"[\w\s\W\"<>\n/]*?>(.*?)</a>\n\t\t\t</div>'
        return self._get_groups(pattern, page_html);

    def get_words(self, text: str):
        pattern = r'\b(?!и|с|ли|или|в|ну|не|по|уже\b)\w+\b'
        return self._get_groups(pattern, text);