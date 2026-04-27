# This file defines the message formats used between client and server.
# (Optional, not imported directly by code, just for reference)

CREATE_ROOM = {
    "action": "create_room",
    "payload": {
        "player_id": str
    }
}

JOIN_ROOM = {
    "action": "join_room",
    "payload": {
        "player_id": str,
        "room_code": str
    }
}

START_GAME = {
    "action": "start_game"
}

# Server responses:
ROOM_CREATED = {
    "type": "room_created",
    "room_code": str
}

PLAYER_JOINED = {
    "type": "player_joined",
    "player_id": str,
    "players": [str]
}

YOUR_ROLE = {
    "type": "your_role",
    "role": str,       # e.g., "Pilot" or "Spy"
    "location": str | None  # null for spy
}

GAME_STARTED = {
    "type": "game_started",
    "players": [str]
}

QUESTION_ASKED = {
    "type": "question_asked",
    "from": str,
    "question": str
}

ANSWER_GIVEN = {
    "type": "answer_given",
    "from": str,
    "answer": str
}

VOTE_CAST = {
    "type": "vote_cast",
    "voter": str,
    "target": str
}

VOTE_RESULT = {
    "type": "vote_result",
    "suspect": str,  # player_id or "tie"
    "votes": dict   # player_id -> count
}

GAME_OVER = {
    "type": "game_over",
    "winner": str   # "civilians" or "spy"
}
