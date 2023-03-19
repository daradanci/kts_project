from marshmallow import Schema, fields
from app.web.schemes import OkResponseSchema


class ThemeSchema(Schema):
    id = fields.Int(attribute="id")
    title = fields.Str(attribute="title", required=True)


class AnswerSchema(Schema):
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)


class QuestionSchema(Schema):
    id = fields.Int(required=False)
    title = fields.Str(required=True)
    theme_id = fields.Int(required=True)
    answers = fields.Nested(AnswerSchema, many=True, required=True)

#
# class QuestionSchema(Schema):
#     id = fields.Int(required=False)
#     title = fields.Str(required=True)
#     answers=fields.Nested(AnswerSchema, many=True)
#     theme_id = fields.Int(required=True)


class ThemeListSchema(Schema):
    data = fields.Nested(ThemeSchema, many=True)


class ThemeIdSchema(Schema):
    theme_id = fields.Int(required=False)



class ListQuestionSchema(Schema):
    questions = fields.Nested(QuestionSchema, many=True)




class ThemeAddSchema(Schema):
    title = fields.Str(required=True)



class ThemeListResponseSchema(OkResponseSchema):
    data = fields.Nested(ThemeListSchema)



