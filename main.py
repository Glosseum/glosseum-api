from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from endpoint.user.route import router as user_router
from endpoint.board.route import router as board_router
from endpoint.article.route import router as article_router
from endpoint.comment.route import router as comment_router


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router)
app.include_router(board_router)
app.include_router(article_router)
app.include_router(comment_router)


@app.on_event("startup")
async def startup():
    print("APP STARTUP")


@app.on_event("shutdown")
async def shutdown():
    print("APP SHUTDOWN")
