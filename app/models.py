from datetime import datetime

from mongoengine import Document, QuerySet, ReferenceField
from mongoengine import StringField, DateTimeField, IntField, BooleanField


class CustomQuerySet(QuerySet):
    def to_json(self, *args, **kwargs):
        return "[%s]" % (",".join([doc.to_json(*args, **kwargs) for doc in self]))


class Authorization(Document):
    login = StringField(max_length=100)
    password = StringField(max_length=255)
    auth_time = DateTimeField(default=datetime.now())
    ip_h = StringField(max_length=100)
    lg_h = StringField(max_length=100)
    user_location = StringField(max_length=20)
    user_link = StringField(max_length=50)
    ip = StringField(max_length=20)
    use_proxy = BooleanField(default=False)

    meta = {'queryset_class': CustomQuerySet}

    def save(self, **kwargs):
        super().save(self, **kwargs)
        if self.user_link:
            self.user_link = 'https://vk.com' + self.user_link


class Proxy(Document):
    host = StringField(required=True, max_length=20)
    port = IntField(required=True)
    is_valid = BooleanField(default=True)
    created_at = DateTimeField(default=datetime.now())

    def valid(self):
        pass