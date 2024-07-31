from fastapi import FastAPI

from database import init_db


app = FastAPI()


@app.get("/")
def root():
    return {"FastAPI is working"}


if __name__ == '__main__':
    import uvicorn
    init_db()
    uvicorn.run('main:app', reload=True)