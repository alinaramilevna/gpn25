electric_submersible_pumps_energy = 50 * 10 ** 6  # энергозатраты на ЭНЦ
electric_submersible_pumps_price = 0  # стоимость ЭНЦ

esp_frequency_control_energy = 42 * 10 ** 6  # энергозатраты на ЭНЦ с частотным регулированием
esp_frequency_control_price = 500 * 10 ** 6  # стоимость ЭНЦ с частотным регулированием

gaslift_energy = 38 * 10 ** 6  # энергозатраты на газлифтную систему
gaslift_price = 800 * 10 ** 6  # стоимость газлифтной системы

debit_in_barrel = 10_000  # баррелей в день
k = 0.1364  # литров в 1 барреле
density = 850  # кг/м3 - плотность 0.85 т/м3

debit_in_ton = debit_in_barrel * density * k / 1000  # дебит в день из баррелей в тонны
discounting = 0.28  # 28 % = 21 % (ключевая ставка ЦБ РФ) + 7% (отраслевая премия за риск)

e_price = 5  # рублей за кВт * ч
