import re
import socket
import tldextract
import geoip2.webservice
from bs4 import BeautifulSoup
from dorkenum.helpers import Logger
from dorkenum import user_options, geo_creds

class ResultLinks():
    count = 0
    progress_pager = 10
    limit_reached = False
    links = []
    link_regex = re.compile(r'url\?q=(.+)')

    def __init__(self, links):
        for link in links:
            self.links.append(link)
        self.progress_pager = (user_options['limit'] / 4)

    def _scrape(self):
        logger = user_options['logger']
        for link in self.links:
            self.limit_reached = True if len(user_options['visited']) >= user_options['limit'] else False
            if not self.limit_reached and link not in user_options['visited']:
                # STUB FOR MODULES HERE
                extracted_link = self._extract_link(link.get('href'))
                target_domain = u''
                if extracted_link:
                    tld = tldextract.extract(extracted_link)
                    target_domain = tld.registered_domain
                else:
                    if user_options['verbose']:
                        logger.log((u'something funky getting the target url, skipping!', 'warn', 2))
                    continue
                try:
                    if re.search(r'(\d+\.)+\d+', link.get('href')):
                        ip_addr = re.search(r'(\d+\.)+\d+', link.get('href')).group()
                    else:
                        ip_addr = socket.gethostbyname(target_domain)
                    geo = geoip2.webservice.Client(geo_creds['userid'], geo_creds['password'])
                    try:
                        target_geo = geo.country(ip_addr)
                        country_iso = target_geo.country.iso_code
                    except:
                        # maxmind limit reached
                        pass
                    logger.log([
                        (u'', 'success', 2),
                        (u'[', 'white', -1),
                        (u'%s' % country_iso, 'warn', -1),
                        (u'][', 'white', -1),
                        (u'%s' % ip_addr, 'warn', -1),
                        (u'][', 'white', -1),
                        (u'%s' % target_domain, 'warn', -1),
                        # (u'][', 'white', -1),
                        # (u'%s' % uri, 'warn', -1),
                        (u']%s ' % ':' if user_options['action'] != 'list-results' else ']', 'white', -1),
                    ])
                except:
                    if user_options['verbose']:
                        logger.log([(u'trouble resolving ip and geo info for: ', 'warn', 2), (u'%s' % link.get('href'), 'warn', -1)])
                if len(user_options['visited']) > 0 and len(user_options['visited']) % self.progress_pager == 0:
                    logger.log((u'processed %d total search results (%d%% complete)' % (len(user_options['visited']), (float(len(user_options['visited']))/float(user_options['limit']))*100), 'info', 2))
                if len(user_options['visited']) >= user_options['limit']:
                    return
                user_options['visited'].append(link)
        return len(user_options['visited'])

    def _extract_link(self, link):
        return u'' if not len(self.link_regex.findall(link)) else self.link_regex.findall(link)[0]

class GoogleSearchResponse():
    pageresult_selector = 'ol > div.g > h3.r > a'

    def __init__(self, query_response, parser='html.parser'):
        self.content = BeautifulSoup(query_response, parser)
        result_links = self.content.select(self.pageresult_selector)
        logger = user_options['logger']
        links = ResultLinks(result_links)
        visited_count = links._scrape()
        if visited_count >= user_options['limit']:
            return
            