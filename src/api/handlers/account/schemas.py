from marshmallow import fields

from api.schemas import Schema


class GetAccountRequestSchema(Schema):
    id = fields.Integer(required=True)


class GetAccountResponseSchema(Schema):
    id = fields.Integer(required=True)
    name = fields.String(required=True)
