def get_energy(e0: int, t: int, r: float) -> float:
    return e0 * (1 - r) ** t


def get_savings(start_energy: int,
                time: int,
                energy_low_coeff: float,
                start_price: float,
                price_up_coef: float) -> tuple[float, float]:
    '''

    :param start_energy: Energy costs at the beginning of the production (МДж)
    :param time: Term to prediction in years
    :param energy_low_coeff: Coefficient (for example 0.05 if annual reducing is 5%) of reducing energy consumption
    :param start_price: Energy costs at the beginning of the production
    :param price_up_coeff: Coefficient (for example 0.05 if annual increasing is 5%) of increasing costs of the energy
    :return: first value is energy savings, second is monetary savings
    '''
    # 1 кВт * ч - 5 руб
    # 1 кВт * ч = 3,6 МДж
    # 3,6 МДж - 5 руб
    # 1 МДж - 5 / 3,6 руб
    start_price /= 3.6

    # Рассчитаем затраты на t лет
    energy_expenses = [start_energy]

    for i in range(1, time):
        energy = start_energy * (1 - energy_low_coeff) ** i
        energy_expenses.append(energy)

    # Рассчитаем совокупную экономию
    money = 0
    energy = 0
    for i in range(1, len(energy_expenses)):
        current_savings = (energy_expenses[i - 1] - energy_expenses[i])
        energy += current_savings
        print((1 + price_up_coef) ** (i - 1))
        money += current_savings * (start_price * (1 + price_up_coef) ** (i - 1))

    return energy, money
