
from kts_backend.users.game.models import GameDC, GameScoreDC, PlayerDC


def score2dict(score: GameScoreDC):
    return {
        "points": int(score.points),
    }


def game2dict(game: GameDC):
    return {
        "id": int(game.id),
        "created_at": game.created_at,
        "chat_id": int(game.chat_id),
        "players": [player2dict(player) for player in game.players],
    }


def player2dict(player: PlayerDC):
    return {
        "tg_id": int(player.tg_id),
        "name": str(player.name),
        "last_name": str(player.last_name),
        "score": [score2dict(score) for score in player.score]
    }
