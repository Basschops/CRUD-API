from marshmallow import Schema, fields, EXCLUDE


class ItemSchema(Schema):
    id = fields.Integer(
        dump_only=True,
    )
    file_name = fields.String(required=True)
    media_type = fields.String(required=True)
    updated_at = fields.DateTime(dump_only=True)
    created_at = fields.DateTime(dump_only=True)

    class Meta:
        unknown = EXCLUDE
