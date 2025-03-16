from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
from core import get_savings, get_plot as get_img

app = Flask(__name__)

# Включаем поддержку CORS
CORS(app)


@app.route('/api/savings', methods=['GET'])
def savings():
    # Получаем параметры из запроса
    start_energy = int(request.args.get('start_energy'))
    time = int(request.args.get('time'))
    energy_low_coeff = float(request.args.get('energy_low_coeff'))
    start_price = float(request.args.get('start_price'))
    price_up_coeff = float(request.args.get('price_up_coeff'))

    savings = get_savings(start_energy, time, energy_low_coeff, start_price, price_up_coeff)

    return jsonify({'savings': savings})


@app.route('/api/plot', methods=['GET'])
def plot():
    # Получаем параметры из запроса
    start_energy = int(request.args.get('start_energy'))
    time = int(request.args.get('time'))
    energy_low_coeff = float(request.args.get('energy_low_coeff'))

    # Получаем путь к изображению
    path = get_img(start_energy, time, energy_low_coeff)

    # Отправляем изображение как файл
    return send_file(path, mimetype='image/png')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
