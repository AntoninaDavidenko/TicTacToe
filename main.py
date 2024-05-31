import json

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from typing import List

app = FastAPI()

templates = Jinja2Templates(directory="templates")


# Підключення до файлу client.html
@app.get("/", response_class=HTMLResponse)
def read_index(request: Request):
    # Відображаємо HTML шаблон
    return templates.TemplateResponse("client.html", {"request": request})


def init_board():
    # створюємо пусту дошку
    return [
        None, None, None,
        None, None, None,
        None, None, None,
    ]


board = init_board()


# перевірка на нічию
def is_draw():
    global board
    # якщо на дошці все ще є вільна клітинка, то нічия не підтверджується та гра продовжується
    # Use list comprehension to check for empty cells in the board
    if any(cell is None for cell in board):
        return False
    # якщо вільних клітинок немає, підтверджуємо нічию та очищуємо дошку
    board = init_board()
    return True


# перевірка на перемогу
def if_won():
    global board
    winning_combinations = [
        [0, 1, 2],
        [3, 4, 5],
        [6, 7, 8],
        [0, 3, 6],
        [1, 4, 7],
        [2, 5, 8],
        [0, 4, 8],
        [6, 4, 2]
    ]
    # якщо є виграшна комбінація, то очищуємо дошку та підтверджуємо перемогу
    for combination in winning_combinations:
        if board[combination[0]] == board[combination[1]] == board[combination[2]] is not None:
            board = init_board()
            return True
    return False


# асинхронная функция
async def update_board(manager, data):
    # зменшуємо id на 1, щоб id клітинок були такими однаковими
    ind = int(data['cell']) - 1
    # завершення підготовки та перехід у гру
    data['init'] = False
    # перевіряємо чи пуста клітинка
    if board[ind] is None:
        # додаємо у клітинку символ за який грає гравець
        board[ind] = data['player']
        if if_won():
            data['message'] = "won"
        elif is_draw():
            data['message'] = "draw"
        else:
            data['message'] = "move"
    else:
        data['message'] = "choose another one"
    await manager.broadcast(data)
    # якщо в повідомленні є перемога чи нічия - розриваємо з'єднання
    game_over = data['message'] in ['draw', 'won']
    if game_over:
        manager.connections = []


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # якщо вже існує 2 підключення, закриваємо всі наступні та повертаємо код помилки
        if len(self.connections) >= 2:
            await websocket.accept()
            await websocket.close(4000)
        else:
            await websocket.accept()
            # додаємо підключення у список
            self.connections.append(websocket)
            if len(self.connections) == 1:
                # визначаємо першого гравця та повідомляємо про очікування опонента
                await websocket.send_json({
                    # відправляємо підготовчі дані перед початком гри
                    'init': True,
                    'player': 'X',
                    'message': 'Waiting for another player',
                    'opponent': 'O',
                })
            else:
                # визначаємо, що другий гравець грає з "О"
                await websocket.send_json({
                    'init': True,
                    'player': 'O',
                    'message': '',
                    'opponent': 'X',
                })
                await self.connections[0].send_json({
                    # повідомляємо гравця про його хід
                    'init': True,
                    'player': 'X',
                    'message': 'Your turn',
                    'opponent': 'O',
                })

    # відключення від сервера
    def disconnect(self, websocket: WebSocket):  # (может быть async)
        self.connections.remove(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            await connection.send_json(data)


manager = ConnectionManager()


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data = json.loads(data)
            await update_board(manager, data)
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except:
        pass


