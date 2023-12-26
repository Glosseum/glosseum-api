from fastapi import FastAPI

from endpoint.user.route import router as user_router
from endpoint.board.route import router as board_router


app = FastAPI()


app.include_router(user_router)
app.include_router(board_router)
