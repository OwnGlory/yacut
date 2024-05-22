from datetime import datetime

from . import db


class URLMap(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original = db.Column(db.String(256), nullable=False)
    short = db.Column(db.String(16), unique=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.now)

    def to_dict(self):
        return dict(
            url=self.original,
            custom_id=self.short
        )

    def from_dict(self, data):
        field_map = {
            'url': 'original',
            'custom_id': 'short'
        }
        for field in field_map:
            if field in data:
                setattr(self, field_map[field], data[field])
