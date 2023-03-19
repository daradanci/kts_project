import json

from aiohttp.web_exceptions import HTTPNotFound, HTTPUnauthorized, HTTPForbidden, HTTPConflict, HTTPBadRequest
from aiohttp_apispec import response_schema, docs, request_schema
from sqlalchemy.orm import class_mapper

from app.quiz.models import Answer
from app.quiz.schemes import (
    ThemeSchema, ThemeListSchema, ThemeListResponseSchema, QuestionSchema,
)
from app.web.app import View
from app.web.schemes import OkResponseSchema
from app.web.utils import json_response
from app.web.mixins import AuthRequiredMixin


class ThemeAddView(AuthRequiredMixin,View):
    @docs(tags=["web"], summary="Add theme", description="Insert a new theme")
    @request_schema(ThemeSchema)
    @response_schema(OkResponseSchema)
    async def post(self):
        if "title" in self.data:
            title = self.data["title"]
        else:
            raise HTTPBadRequest
        # if await self.store.quizzes.get_theme_by_title(title) is not None:
        #     raise HTTPConflict(reason=f"Тема под названием '{title}' уже существует.")
        #
        theme = await self.store.quizzes.create_theme(title=title)
        return json_response(data=ThemeSchema().dump(theme))


class ThemeListView(AuthRequiredMixin,View):
    @docs(tags=["web"], summary="List themes", description="List themes")
    @response_schema(ThemeListResponseSchema)
    async def get(self):
        themes = await self.store.quizzes.list_themes()
        raw_themes = [{"title": theme.title, "id": theme.id} for theme in themes]
        return json_response(data={"themes": raw_themes})


class QuestionAddView(AuthRequiredMixin,View):
    @docs(tags=["web"], summary="Add question", description="Insert questions for the theme")
    @request_schema(QuestionSchema)
    @response_schema(OkResponseSchema)
    async def post(self):
        _question = await self.store.quizzes.create_question(title=self.data['title'], theme_id=
        self.data['theme_id'],
                                                             answers=[Answer(title=answer['title'],
                                                                             is_correct=answer['is_correct'])
                                                                      for answer in self.data['answers']])
        # _answers=await self.store.quizzes.create_answers(question_id=_question.id,
        #                                                  answers=[Answer(title=answer['title'],
        #                                                                  is_correct=answer['is_correct'])
        #                                                           for answer in self.data['answers']])
        return json_response(data= {
            'id': _question.id,
            'title': _question.title,
            'theme_id': _question.theme_id,
            'answers': [{'title': _answer.title, 'is_correct': _answer.is_correct} for _answer in _question.answers]
        })


class QuestionListView(AuthRequiredMixin,View):
    @docs(tags=["web"], summary="All questions", description="View all questions (thematic filtration implemented)")
    @response_schema(OkResponseSchema)
    async def get(self):
        questions = await self.store.quizzes.list_questions(
            theme_id=self.request.rel_url.query['theme_id'] if 'theme_id' in self.request.rel_url.query else None)

        raw_questions = [{
            'id': question.id,
            'title': question.title,
            'theme_id': question.theme_id,
            'answers': [{'title': _answer.title, 'is_correct': _answer.is_correct} for _answer in question.answers]
        } for question in questions]
        return json_response(data={"questions": raw_questions})


class TestView(View):
    @docs(tags=["web"], summary="test", description="test")
    @response_schema(OkResponseSchema)
    async def post(self):
        await self.store.quizzes.test()
        return json_response(data='ok')