from aiohttp.web_app import Application


def setup_routes(app: Application):
    from kts_backend.users.admin.routes import (
        setup_routes as admin_setup_routes,
    )
    from kts_backend.users.quiz.routes import setup_routes as quiz_setup_routes
    from kts_backend.users.game.routes import setup_routes as game_setup_routes

    admin_setup_routes(app)
    quiz_setup_routes(app)
    game_setup_routes(app)
