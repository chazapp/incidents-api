import logging
import re

wsgi_app = 'incidents.wsgi'
bind = '0.0.0.0:8000'
workers = 5
accesslog = '-'
errorlog = '-'

class RequestPathFilter(logging.Filter):
    def __init__(self, *args, path_re, **kwargs):
        super().__init__(*args, **kwargs)
        self.path_filter = re.compile(path_re)

    def filter(self, record):
        req_path = record.args['U']
        if not self.path_filter.match(req_path):
            return True  
        return False

def on_starting(server):
    server.log.access_log.addFilter(RequestPathFilter(path_re=r'^/health/$'))
    server.log.access_log.addFilter(RequestPathFilter(path_re=r'^/metrics/$'))
