from typing import Optional
from aiohttp.web_exceptions import HTTPNotFound, HTTPConflict, HTTPBadRequest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

from app.base.base_accessor import BaseAccessor
from app.quiz.models import (
    Answer,
    Question,
    Theme, ThemeModel, QuestionModel, AnswerModel,
)
from app.store.database.database import Database
from sqlalchemy import select, text, exc, delete


class QuizAccessor(BaseAccessor):
    async def create_theme(self, title: str) -> Theme:
        # if await self.get_theme_by_title(title) is not None:
        #     raise HTTPConflict(reason=f"Тема под названием '{title}' уже существует.")
        async with self.app.database.session() as session:
            new_theme = ThemeModel(title=str(title))
            session.add(new_theme)
            await session.commit()

            # try:
            #     session.add(new_theme)
            #     await session.commit()
            #
            # except IntegrityError as e:
            #     print('!ERROR!', e.__dict__['orig'])
            #     print('?ERROR?', e.orig.pgcode)
            #     print('.ERROR.', e.detail)
            #     await session.rollback()
            #     if e.orig.pgcode == "23505":
            #         raise HTTPConflict(reason=f"Тема под названием '{title}' уже существует.")
            #     raise HTTPConflict(reason=e.__dict__['orig'])

            return Theme(id=new_theme.id, title=new_theme.title)

    async def get_theme_by_title(self, title: str) -> Optional[Theme]:
        async with self.app.database.session() as session:
            result_raw = await session.execute(select(ThemeModel).filter_by(title=title))
            result = [res._mapping['ThemeModel'] for res in result_raw]
            return Theme(id=result[0].id, title=result[0].title) if len(result) > 0 else None

    async def get_theme_by_id(self, id_: int) -> Optional[Theme]:
        async with self.app.database.session() as session:
            result_raw = await session.execute(select(ThemeModel).filter_by(id=int(id_)))
            result = [res._mapping['ThemeModel'] for res in result_raw]
            return Theme(id=result[0].id, title=result[0].title) if len(result) > 0 else None

    async def list_themes(self) -> list[Theme]:
        async with self.app.database.session() as session:
            result_raw = await session.execute(select(ThemeModel))
            result = [res._mapping['ThemeModel'] for res in result_raw]
            return result

    async def create_answers(
            self, question_id: int, answers: list[Answer]
    ) -> list[Answer]:
        async with self.app.database.session() as session:
            session.add_all([AnswerModel(title=answer.title, question_id=question_id, is_correct=answer.is_correct) for answer in answers])
            await session.commit()
        return [Answer(title=answer.title, is_correct=answer.is_correct) for answer in answers]

    async def create_question(
            self, title: str, theme_id: int, answers: list[Answer]
    ) -> Question:
        # if await self.get_theme_by_id(theme_id) is None:
        #     raise HTTPNotFound(reason=f'Не существует темы №{theme_id}')
        # if await self.get_question_by_title(title) is not None:
        #     raise HTTPConflict(reason=f"Вопрос под названием '{title}' уже существует.")
        print('NONE?', theme_id)
        if len(answers) < 2:
            raise HTTPBadRequest(reason=f"Слишком мало ответов")
        if len([answer for answer in answers if answer.is_correct]) == 0 \
                or len([answer for answer in answers if answer.is_correct]) > 1:
            raise HTTPBadRequest(reason=f"Должен быть 1 правильный ответ.")
        async with self.app.database.session() as session:
            new_question = QuestionModel(title=str(title), theme_id=theme_id)
            session.add(new_question)


            await session.commit()

            _answers = await self.create_answers(question_id=new_question.id,
                                               answers=[Answer(title=answer.title,
                                                               is_correct=answer.is_correct)
                                                        for answer in answers])

            # try:
            #     await session.commit()
            # except IntegrityError as e:
            #     await session.rollback()
            #     if e.orig.pgcode == "23505":
            #         raise HTTPConflict(reason=f"Вопрос под названием '{title}' уже существует.")
            #     if e.orig.pgcode == "23502":
            #         raise HTTPNotFound(reason=f'Не указана тема вопроса.')
            #     if e.orig.pgcode == "23503":
            #         raise HTTPNotFound(reason=f'Указанная тема отсутствует в списке.')
            #     raise HTTPConflict(reason=e.__dict__['orig'])
            return Question(id=int(new_question.id), title=new_question.title, theme_id=new_question.theme_id,
                            answers=[Answer(title=answer.title, is_correct=answer.is_correct) for answer in answers]
                            )

    async def get_question_by_title(self, title: str) -> Optional[Question]:
        async with self.app.database.session() as session:
            # result_raw = await session.execute(select(QuestionModel).filter_by(title=title))
            # result = [res._mapping['QuestionModel'] for res in result_raw]
            res = await session.execute(select(QuestionModel).join(
                AnswerModel, QuestionModel.id == AnswerModel.question_id
            ).where(QuestionModel.title == title))
            question = res.scalars().first()

            # result = await session.query()

            # return Question(id=int(result[0].id), title=result[0].title, theme_id=result[0].theme_id,
            #                 answers=[]) if len(result) > 0 else None

            return Question(id=int(question.id), title=question.title, theme_id=question.theme_id,
                            answers=[Answer(title=answer.title, is_correct=answer.is_correct)
                                      for answer in question.answers])

    async def list_questions(self, theme_id: Optional[int] = None) -> list[Question]:
        async with self.app.database.session() as session:
            if theme_id is not None:
                result_raw = await session.execute(
                    select(QuestionModel).filter_by(theme_id=int(theme_id)))
            else:
                result_raw = await session.execute(select(QuestionModel))
            result = [res._mapping['QuestionModel'] for res in result_raw]
            return [Question(id=int(question.id), title=question.title, theme_id=question.theme_id,
                             answers=[Answer(title=answer.title, is_correct=answer.is_correct)
                                      for answer in question.answers])
                    for question in result]


    async def test(self):

        question = await self.create_question(
            title='Какие гуси жили у бабуси?', theme_id=151, answers=[
                AnswerModel(
                    title="Белый и серый",
                    is_correct=True,
                ),
                AnswerModel(
                    title="Чёрный и белый",
                    is_correct=False,
                ),
            ]
        )

        async with self.app.database.session() as session:
            res = await session.execute(select(QuestionModel))
            questions = res.scalars().all()

            res = await session.execute(select(AnswerModel))
            db_answers = res.scalars().all()

            print('T1', questions)
            print('T2', db_answers)
        print('T3', len(db_answers))

        # async with self.app.database.session() as session:
        #
        #     res = await session.execute(select(AnswerModel))
        #     db_answers = res.scalars().all()
        #     return [Answer(title=answer.title, is_correct=answer.is_correct) for answer in db_answers]
