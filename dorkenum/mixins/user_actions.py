import simplejson as json


class UserActions():
    directives = {}

    def __init__(self, file):
        try:
            self.directives = json.loads(file)
        except Exception as e:
            print e
