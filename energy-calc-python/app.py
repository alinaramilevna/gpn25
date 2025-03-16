import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from core import get_savings, get_plot as get_img

app = FastAPI(debug=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/api/savings')
def main(start_energy: int,
         time: int,
         energy_low_coeff: float,
         start_price: float,
         price_up_coeff: float) -> dict:
    # curl "http://127.0.0.1:8000/api/savings?start_energy=10000000&time=10&energy_low_coeff=0.07&start_price=5&price_up_coeff=0.09"
    return {'savings': get_savings(start_energy, time, energy_low_coeff, start_price, price_up_coeff)}


@app.get('/api/plot')
def get_plot(start_energy: int,
             time: int,
             energy_low_coeff: float):
    path = get_img(start_energy, time, energy_low_coeff)
    return FileResponse(path, media_type="image/png")


if __name__ == '__main__':
    uvicorn.run(reload=True,
                host='0.0.0.0',
                app='app:app')
