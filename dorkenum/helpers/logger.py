import click
from datetime import datetime

class Logger():
    path = u''
    spacer = u'   '
    message_types = {
        'success': {
            'fg': u'green',
            'header': u'%s[+]',
        },
        'fail': {
            'fg': u'red',
            'header': u'%s[-]',
        },
        'warn': {
            'fg': u'yellow',
            'header': u'%s[!]',
        },
        'info': {
            'fg': u'blue',
            'header': u'%s[*]',
        },
        'white': {
            'fg': u'white',
            'header': u'',
        },
        'magenta': {
            'fg': u'magenta',
            'header': u'',
        },
    }

    def __init__(self, path=''):
        self.path = path

    def log(self, entries, *args, **kwargs):
        now = datetime.now().strftime('%Y%m%d-%H:%M:%S')
        entries = [entries] if isinstance(entries, tuple) else entries

        index_message_type = entries[0][1] if len(entries) else 'success'
        index_spacing = entries[0][2] if len(entries) else 0
        
        full_message = [click.style(u'%s ' % self.message_types[index_message_type]['header'] % (self.spacer*index_spacing), fg=self.message_types[index_message_type]['fg'])]
        for entry in entries:
            message, message_type, spacing = entry
            full_message.append(click.style(message, fg=self.message_types[message_type]['fg']))
        if self.path:
            with open(self.path, 'ab') as fh:
                fh.write(u'%s %s %s\n' % (now, self.message_types[index_message_type]['header'] % (self.spacer*index_spacing), ''.join([entry[0] for entry in entries])))
        click.echo(''.join(full_message))