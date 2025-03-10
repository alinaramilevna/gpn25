def get_daily_by_dupuis(t: int, qi: float = 10_000, di: float = 0.1, days: int = 365) -> float:
    """
    :param t: Номер дня (от 1 и далее)
    :param qi: Начальный дебит (баррелей в день)
    :param di: Номинальный темп падения добычи в год (10% = 0.1)
    :return: Дебит за день (баррелей в день)
    """
    di_daily = di / days
    # формула Дюпюи для линейного падения
    qt = qi * (1 - di_daily * t)
    return max(qt, 0)


def get_sum_by_year_by_dupuis(t: int, qi: float = 10_000, di: float = 0.1) -> float:
    s = 0
    curr_debit = qi * 365
    for year in range(1, t + 1):
        qt = curr_debit * (1 - di)
        s += qt
        curr_debit = qt

    return s


def get_curr_debit_by_dupuis(t: int, qi: float = 10_000, di: float = 0.1) -> float:
    curr_debit = qi * 365
    for year in range(1, t + 1):
        qt = curr_debit * (1 - di)
        curr_debit = qt

    return curr_debit
