from marshmallow import Schema, fields


class AdminSchema(Schema):
    id = fields.Int(required=False)
    email = fields.Str(required=True)
    password = fields.Str(required=True, load_only=True)


class AdminLoginSchema(Schema):
    email = fields.Str(required=True)
    password = fields.Str(required=False)


class AdminLoginResponseSchema(Schema):
    id = fields.Int(required=True)
    email = fields.Str(required=True)
