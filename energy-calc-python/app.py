import uvicorn
from fastapi import FastAPI

from core import get_savings

app = FastAPI(debug=True)


@app.get('/')
def main(start_energy: int,
         time: int,
         energy_low_coeff: float,
         start_price: float,
         price_up_coeff: float) -> dict:
    # curl http://127.0.0.1:8000/?start_energy=10000000&time=10&energy_low_coeff=0.07&start_price=5&price_up_coeff=0.09
    return {'savings': get_savings(start_energy, time, energy_low_coeff, start_price, price_up_coeff)}


if __name__ == '__main__':
    uvicorn.run(reload=True,
                app='app:app')
