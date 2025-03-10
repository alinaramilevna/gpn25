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
