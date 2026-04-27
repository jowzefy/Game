import asyncio
import random
import json
from game_logic import GameState, LOCATIONS, assign_roles
from game_logic import GameError

class Room:
    def __init__(self, code, host_id, host_ws):
        self.code = code
        self.players = {host_id: host_ws}
        self.host = host_id
        self.game = None

    async def broadcast(self, message, exclude=None):
        if not isinstance(message, str):
            import json
            message = json.dumps(message)
        tasks = []
        for pid, ws in self.players.items():
            if pid != exclude:
                tasks.append(asyncio.create_task(ws.send(message)))
        if tasks:
            await asyncio.gather(*tasks)

    async def start_game(self):
        if len(self.players) < 3:
            raise GameError("Need at least 3 players")
        location = random.choice(LOCATIONS)
        roles = assign_roles(list(self.players.keys()), location)
        self.game = GameState(location, roles)
        # Send roles privately
        for pid, ws in self.players.items():
            role = self.game.roles[pid]
            await ws.send(json.dumps({
                "type": "your_role",
                "role": role,
                "location": location if role != "Spy" else None
            }))
        await self.broadcast({
            "type": "game_started",
            "players": list(self.players.keys())
        })

    async def cast_vote(self, voter, target):
        if not self.game:
            return
        self.game.votes[voter] = target
        await self.broadcast({
            "type": "vote_cast",
            "voter": voter,
            "target": target
        })
        # Check if all voted
        if len(self.game.votes) == len(self.players):
            # Tally votes
            tally = {}
            for v in self.game.votes.values():
                tally[v] = tally.get(v, 0) + 1
            max_votes = max(tally.values())
            suspects = [pid for pid, count in tally.items() if count == max_votes]
            # Simplest case: one suspect
            result = suspects[0] if len(suspects) == 1 else "tie"
            await self.broadcast({
                "type": "vote_result",
                "suspect": result,
                "votes": tally
            })
            # Determine win
            if result == "tie":
                await self.broadcast({"type": "game_over", "winner": "spy"})
            else:
                if self.game.roles[result] == "Spy":
                    # Spy caught - civilians win unless spy guesses location correctly
                    await self.broadcast({
                        "type": "spy_caught",
                        "spy": result,
                        "location": self.game.location
                    })
                    # TODO: Ask spy to guess location - simplified: civilians win
                    winner = "civilians"
                    await self.broadcast({"type": "game_over", "winner": winner})
                else:
                    # Wrong guess, spy wins
                    await self.broadcast({
                        "type": "game_over",
                        "winner": "spy",
                        "spy": [pid for pid, r in self.game.roles.items() if r == "Spy"][0]
                    })

    async def restart_game(self):
        self.game = None
        await self.broadcast({"type": "game_restarting"})
        await self.start_game()

class RoomManager:
    def __init__(self):
        self.rooms = {}

    def create_room(self, player_id, ws):
        code = self._generate_code()
        room = Room(code, player_id, ws)
        self.rooms[code] = room
        return code

    def join_room(self, code, player_id, ws):
        room = self.rooms.get(code)
        if not room:
            raise GameError("Room not found")
        if player_id in room.players:
            raise GameError("Name already taken")
        room.players[player_id] = ws
        return room

    def leave_room(self, code, player_id):
        room = self.rooms.get(code)
        if room:
            if player_id in room.players:
                del room.players[player_id]
            if not room.players:
                del self.rooms[code]

    def get_room_by_player(self, player_id, code):
        return self.rooms.get(code)

    def _generate_code(self):
        import string, random
        return ''.join(random.choices(string.ascii_uppercase, k=4))
