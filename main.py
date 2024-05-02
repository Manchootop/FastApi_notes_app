from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def get_routes():
    return ['/notes', '/notes/<pk>/']