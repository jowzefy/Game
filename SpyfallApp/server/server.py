import asyncio
import websockets
import json
from rooms import RoomManager
from game_logic import GameError
from os import system
system("cls")
room_manager = RoomManager()

async def handler(websocket):
    player_id = None
    room_code = None
    try:
        async for message in websocket:
            data = json.loads(message)
            print(f"🟢 SERVER RECEIVED: {data}")
            action = data.get("action")
            payload = data.get("payload", {})

            if action == "create_room":
                player_id = payload["player_id"]
                room_code = room_manager.create_room(player_id, websocket)
                await websocket.send(json.dumps({
                    "type": "room_created",
                    "room_code": room_code
                }))

            elif action == "join_room":
                player_id = payload["player_id"]
                room_code = payload["room_code"]
                room = room_manager.join_room(room_code, player_id, websocket)
                await room.broadcast({
                    "type": "player_joined",
                    "player_id": player_id,
                    "players": list(room.players.keys())
                })

            elif action == "start_game":
                room = room_manager.get_room_by_player(player_id, room_code)
                if room:
                    try:
                        await room.start_game()
                    except GameError as e:
                        await websocket.send(json.dumps({"type": "error", "message": str(e)}))

            elif action == "ask_question":
                room = room_manager.get_room_by_player(player_id, room_code)
                if room:
                    question = payload["question"]
                    await room.broadcast({
                        "type": "question_asked",
                        "from": player_id,
                        "question": question
                    })

            elif action == "answer_question":
                room = room_manager.get_room_by_player(player_id, room_code)
                if room:
                    answer = payload["answer"]
                    await room.broadcast({
                        "type": "answer_given",
                        "from": player_id,
                        "answer": answer
                    })

            elif action == "cast_vote":
                room = room_manager.get_room_by_player(player_id, room_code)
                if room:
                    target = payload["target"]
                    await room.cast_vote(player_id, target)

            elif action == "restart_game":
                room = room_manager.get_room_by_player(player_id, room_code)
                if room:
                    await room.restart_game()

            # more actions can be added

    except websockets.exceptions.ConnectionClosed:
        pass
    finally:
        if player_id and room_code:
            room_manager.leave_room(room_code, player_id)

async def main():
    async with websockets.serve(handler, "0.0.0.0", 8765, ping_interval=None):
        print("Spyfall server running on ws://0.0.0.0:8765")
        await asyncio.Future() # run forever

if __name__ == "__main__":
    asyncio.run(main())
