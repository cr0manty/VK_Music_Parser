from mongoengine import connect


class Database:
    def __init__(self, host='localhost', port=27017):
        self.host = host
        self.port = port
        connect('vk_music', host=self.host, port=self.port)

    def __str__(self):
        return 'Host: {}, Port: {}'.format(self.host, self.port)

    def __repr__(self):
        return '{}:{}'.format(self.host, self.port)
