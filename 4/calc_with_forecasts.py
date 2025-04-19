# Учитываются три основных фактора
# Падение дебита (по формуле Дюпюи если что считаем дебит)
# Цены на электроэнергию спрогнозированные МинФином РФ
# Ну и понятно ставка дисконтирования 28 %

# from pprint import pprint as print

from consts import energy_prices_MDz, energy_per_barrel, percent_10_cost, percent_5_cost, percent_20_cost
from tools import get_every_year_by_arps as get_every_year_by_arps


def get_PBP(annual_savings: list[int], investment: int) -> float:
    # Обратно переводим в рубли
    investment /= 82
    cnt = 0
    i = 0
    while investment > 0:
        try:
            investment -= annual_savings[i]
            i += 1
            cnt += 1
        except IndexError:
            investment -= annual_savings[-1]
            cnt += 1
    return cnt


def get_DBPB(annual_savings: list[int], investment: int, discounting: float) -> float:
    # Обратно переводим в рубли
    investment /= 82
    cnt = 0
    i = 0
    while investment > 0:
        try:
            investment -= (annual_savings[i] / (1 + discounting) ** i)
            i += 1
            cnt += 1
        except IndexError:
            investment -= (annual_savings[-1] / (1 + discounting) ** i)
            cnt += 1
            i += 1
    return cnt


def get_NPV(savings_for_years: list, discounting: float, t: int) -> float:
    npv = 0
    for year in range(1, t + 1):
        npv += savings_for_years[year - 1] / (1 + discounting) ** year
    return npv


def get_PI(savings: int, investment: int, discounting: float, t: int) -> float:
    return 1 + get_NPV(savings, discounting, t) / investment


def get_money() -> dict:
    debits = get_every_year_by_arps(6)
    expenses_per_years = [debits[i] * energy_per_barrel * energy_prices_MDz[i] for i in range(6)]

    percent_5 = [debits[0] * energy_per_barrel * energy_prices_MDz[0]]
    energy_5 = energy_per_barrel
    for i in range(5):
        energy_5 = energy_5 - energy_5 * 0.05
        percent_5.append(debits[i + 1] * energy_5 * energy_prices_MDz[i + 1])

    percent_10 = [debits[0] * energy_per_barrel * energy_prices_MDz[0]]
    energy_10 = energy_per_barrel
    for i in range(5):
        energy_10 = energy_10 - energy_10 * 0.1
        percent_10.append(debits[i + 1] * energy_10 * energy_prices_MDz[i + 1])

    percent_20 = [debits[0] * energy_per_barrel * energy_prices_MDz[0]]
    energy_20 = energy_per_barrel
    for i in range(5):
        energy_20 = energy_20 - energy_20 * 0.2
        percent_20.append(debits[i + 1] * energy_20 * energy_prices_MDz[i + 1])

    # return expenses_per_years, percent_5, percent_10, percent_20
    return {
        'start': expenses_per_years,
        '5_percent': percent_5,
        '10_percent': percent_10,
        '20_percent': percent_20
    }


data = get_money()
start, percent_5, percent_10, percent_20 = data['start'], data['5_percent'], data['10_percent'], data['20_percent']
percent_5_savings = [start[i] - percent_5[i] for i in range(len(start))]
percent_10_savings = [start[i] - percent_10[i] for i in range(len(start))]
percent_20_savings = [start[i] - percent_20[i] for i in range(len(start))]

percent_5_data = {
    'PI': get_PI(percent_5_savings, percent_5_cost, 0.28, len(percent_5_savings)),
    'NPV': get_NPV(percent_5_savings, 0.28, len(percent_5_savings)),
    'PBP': get_PBP(percent_5_savings, percent_5_cost),
    'DPBP': get_DBPB(percent_5_savings, percent_5_cost, 0.28)
}
percent_10_data = {
    'PI': get_PI(percent_10_savings, percent_10_cost, 0.28, len(percent_10_savings)),
    'NPV': get_NPV(percent_10_savings, 0.28, len(percent_10_savings)),
    'PBP': get_PBP(percent_10_savings, percent_10_cost),
    'DPBP': get_DBPB(percent_10_savings, percent_10_cost, 0.28)
}
percent_20_data = {
    'PI': get_PI(percent_20_savings, percent_20_cost, 0.28, len(percent_20_savings)),
    'NPV': get_NPV(percent_20_savings, 0.28, len(percent_20_savings)),
    'PBP': get_PBP(percent_20_savings, percent_20_cost),
    'DPBP': get_DBPB(percent_20_savings, percent_20_cost, 0.28)
}

print(percent_5_data, percent_10_data, percent_20_data, sep='\n')
