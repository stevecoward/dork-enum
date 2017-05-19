import re
import requests
from dorkenum import user_actions


class RegexMatch():
    result = u''

    def __init__(self, pattern, haystack, match_group):
        try:
            pat = re.compile(pattern)
            if pat.search(haystack):
                search_result = pat.search(haystack)
                self.result = search_result.group(match_group)
        except Exception as e:
            print e


class GetRemoteFile():
    def __init__(self, url, endpoint, **kwargs):
        test_urls = []
        user_actions['file'] = ''
        if endpoint.startswith('/'):
            test_url = u'%s%s%s' % (
                '//'.join(url.split('/')[:2]), url.split('/')[2], endpoint)
            test_urls.append(test_url)
        else:
            url_split = url.split('/')[2:]
            for i in xrange(((len(url_split) - 1) * -1), 0, 1):
                url_segment = '/'.join(url_split[:i])
                test_url = u'%s//%s/%s' % (url.split('//')
                                           [0], url_segment, endpoint)
                test_urls.append(test_url)
        for url in test_urls:
            with requests.Session() as session:
                request = session.get(url, **kwargs)
                if request.ok:
                    user_actions['file'] = request.text
                    break
