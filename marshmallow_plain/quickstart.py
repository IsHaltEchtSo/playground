from datetime import date
from pprint import pprint

from marshmallow import Schema, fields


class ArtistSchema(Schema):
    name = fields.Str()

class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
    artist = fields.Nested(nested=ArtistSchema())

class Artist:
    def __init__(self, name) -> None:
        self.name = name

bowie = Artist(name='David Bowie')
album = dict(title='Hunky Dory', artist=bowie, release_data=date(year=1971, month=12, day=17))

schema = AlbumSchema()
result = schema.dump(obj=[album, album], many=True)
pprint(result, indent=2)
pprint(album, indent=2)