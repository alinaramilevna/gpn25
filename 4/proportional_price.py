import csv

from consts import discounting, economy_in_usd_75, modern_cost


def get_energy_cost_from_oil_price(oil_price: float, base_oil_price=75, base_energy_cost=0.05) -> float:
    return base_energy_cost * (oil_price / base_oil_price)


def get_PBP(annual_savings: int, investment: int) -> float:
    return investment / annual_savings


def get_DBPB(annual_savings: int, investment: int, discounting: float) -> float:
    return investment / (annual_savings / (1 + discounting))


def get_NPV(annual_savings: int, discounting: float, t: int) -> float:
    npv = 0
    for year in range(1, t + 1):
        npv += annual_savings / (1 + discounting) ** year
    return npv


def get_PI(annual_savings: int, investment: int, discounting: float, t: int) -> float:
    return 1 + get_NPV(annual_savings, discounting, t) / investment


def get_annual_savings(percent: int, energy_cost_usd: int,
                       energy_per_barrel: float) -> float:
    # Сколько тратим в год на энергию
    energy_per_year = 10_000 * 365 * energy_per_barrel * energy_cost_usd
    # Экономия при сокращении
    energy_per_year = energy_per_year * percent
    return energy_per_year


years = 5
oil_prices = list(range(60, 91))  # 60–90 USD/баррель
efficiency_levels = [0.05, 0.1, 0.2]  # 5%, 10%, 20% снижения

# по вертикали - цена на нефть, по горизонтали - эффективность
matrix_pbp = []
matrix_dpbp = []
matrix_npv = []
matrix_pi = []

for price in oil_prices:
    row_pbp = []
    row_dpbp = []
    row_npv = []
    row_pi = []

    for eff in efficiency_levels:
        savings_75 = economy_in_usd_75[eff]
        savings_scaled = savings_75 * (price / 75)  # пропорциональная корректировка под цену

        investment = modern_cost[eff]

        row_pbp.append(get_PBP(savings_scaled, investment))
        row_dpbp.append(get_DBPB(savings_scaled, investment, discounting))
        row_npv.append(get_NPV(savings_scaled, discounting, years))
        row_pi.append(get_PI(savings_scaled, investment, discounting, years))

    matrix_pbp.append(row_pbp)
    matrix_dpbp.append(row_dpbp)
    matrix_npv.append(row_npv)
    matrix_pi.append(row_pi)

# print('PBP matrix:')
# print(matrix_pbp)
# print('DPBP matrix:')
# print(matrix_dpbp)
# print('NPV matrix:')
# print(matrix_npv)
# print('PI matrix:')
# print(matrix_pi)


headers = ['Oil Price'] + [f'{int(eff * 100)}%' for eff in efficiency_levels]


def save_matrix_to_csv(matrix, filename):
    with open(filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for i, row in enumerate(matrix):
            writer.writerow([oil_prices[i]] + row)


save_matrix_to_csv(matrix_pbp, 'pbp_matrix.csv')
save_matrix_to_csv(matrix_dpbp, 'dpbp_matrix.csv')
save_matrix_to_csv(matrix_npv, 'npv_matrix.csv')
save_matrix_to_csv(matrix_pi, 'pi_matrix.csv')
