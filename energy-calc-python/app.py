import uvicorn
from fastapi import FastAPI

app = FastAPI(debug=True)


@app.get('/')
def main():
    return 'Hello!'


if __name__ == '__main__':
    uvicorn.run(reload=True,
                app='app:app')
