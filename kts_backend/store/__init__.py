import typing

from kts_backend.store.database.database import Database

if typing.TYPE_CHECKING:
    from kts_backend.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from kts_backend.store.bot.manager import BotManager
        from kts_backend.store.admin.accessor import AdminAccessor
        from kts_backend.store.quiz.accessor import QuizAccessor
        from kts_backend.store.game.accessor import GameAccessor
        from kts_backend.store.tg_api.accessor import TgApiAccessor

        self.quizzes = QuizAccessor(app)
        self.admins = AdminAccessor(app)
        self.tg_api=TgApiAccessor(app)
        self.game=GameAccessor(app)
        self.bots_manager = BotManager(app)


def setup_store(app: "Application"):
    app.database = Database(app)
    app.on_startup.append(app.database.connect)
    app.on_cleanup.append(app.database.disconnect)
    app.store = Store(app)
