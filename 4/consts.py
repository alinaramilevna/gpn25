debit_in_barrel = 10_000  # баррелей в день
k = 0.1364  # литров в 1 барреле
density = 850  # кг/м3 - плотность 0.85 т/м3

debit_in_ton = debit_in_barrel * density * k / 1000  # дебит в день из баррелей в тонны
discounting = 0.28  # 28 % = 21 % (ключевая ставка ЦБ РФ) + 7% (отраслевая премия за риск)

energy_per_barrel = 50 * 10 ** 6 / 3_600_000  # кВт * ч

economy_in_usd_75 = {
    0.05: 2_000_000,
    0.1: 3_800_000,
    0.2: 7_000_000
}

modern_cost = {
    0.05: 10_000_000,
    0.1: 20_000_000,
    0.2: 40_000_000
}

# это за кВт*ч
energy_prices_kVt = [4.134, 4.258, 4.356, 4.439, 4.496, 4.546]
# это за Мдж
energy_prices_MDz = [i / 3.6 for i in energy_prices_kVt]

percent_5_cost = 10 ** 7 * 82
percent_10_cost = 2 * 10 ** 7 * 82
percent_20_cost = 4 * 10 ** 7 * 82
