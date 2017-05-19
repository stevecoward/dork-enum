import sys
import requests
from bs4 import BeautifulSoup
from logger import Logger
from search import GoogleSearchResponse, ResultLinks
from sigint_handler import SIGINT_handler
from dorkenum import user_options


def get_next_link(response_content, selector='a.fl'):
    html = BeautifulSoup(response_content, 'html.parser')
    paginated_links = html.select(selector)
    return paginated_links[-1] if len(paginated_links) else False


def get_page_or_die(url, params={}, indent=1, **kwargs):
    query_request = requests.get(url, params=params, **kwargs)
    if not query_request.ok:
        user_options['logger'].log(
            (u'search failed somehow, could be google captcha... (HTTP %d)' % query_request.status_code, 'fail', indent))
        sys.exit(2)
    return query_request.text
