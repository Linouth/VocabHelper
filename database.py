from peewee import (
        SqliteDatabase, Model, TextField, DateTimeField
)
import datetime
import json


db = SqliteDatabase('results.db')


class Entry(Model):
    searchstring = TextField()
    phrase = TextField(unique=True, index=True)
    meaning = TextField(null=True)
    lasttested = DateTimeField(null=True)

    timestamp = DateTimeField(default=datetime.datetime.now())

    class Meta:
        database = db

    @classmethod
    def export(cls, style):
        q = cls.select()
        out = []
        for e in q:
            out.append({
                'string': e.searchstring,
                'phrase': e.phrase,
                'meaning': e.meaning})
        if style == 'json':
            return json.dumps(out)


def create_tables():
    db.connect()
    db.create_tables([Entry])


if __name__ == '__main__':
    print('Preparing database')
    create_tables()
