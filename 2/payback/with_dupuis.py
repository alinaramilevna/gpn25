from math import ceil

from consts import electric_submersible_pumps_energy, e_price, esp_frequency_control_energy, \
    esp_frequency_control_price, gaslift_energy, gaslift_price, discounting
from tools import get_daily_by_dupuis


def get_barrels_per_year(year: int = 1) -> float:
    # Учитываем падение дебита для всего года, начиная с первого года
    return sum([get_daily_by_dupuis(t, di=0.1 * year) for t in range(1, 366)])


def get_barrels_per_period(t: int, year: int = 1) -> float:
    # Учитываем падение дебита для каждого периода (по дням), с накоплением за годы
    return sum([get_daily_by_dupuis(i, di=0.1 * year, days=t) for i in range(1, t + 1)])


# ------------------------------------------------------

def get_electric_submersible_pumps_cost(years: int = 1) -> int:
    # 1. Переводим Дж в кВт·ч (1 кВт·ч = 3 600 000 Дж)
    # 2. Умножаем на стоимость электроэнергии с учетом падения дебита за все годы
    return ceil(
        (electric_submersible_pumps_energy / 3_600_000) * e_price * get_barrels_per_period(int(365 * years), years))


def get_electric_submersible_pumps_PBP() -> float:
    # т к затраты на внедрение нулевые
    return 0


# ------------------------------------------------------

def get_esp_frequency_control_cost(years: int = 1) -> int:
    return ceil((esp_frequency_control_energy / 3_600_000) * e_price * get_barrels_per_period(365 * years, years))


def get_esp_frequency_control_PBP() -> float:
    savings = get_electric_submersible_pumps_cost() - get_esp_frequency_control_cost()
    return esp_frequency_control_price / savings


def get_gaslift_cost(years: int = 1) -> int:
    return ceil((gaslift_energy / 3_600_000) * e_price * get_barrels_per_period(365 * years, years))


def get_gaslift_PBP() -> float:
    savings = get_electric_submersible_pumps_cost() - get_gaslift_cost()
    return gaslift_price / savings


# ------------------------------------------------------

def get_gaslift_DPBP() -> float:
    discounting_savings = (get_electric_submersible_pumps_cost() - get_gaslift_cost()) / (1 + discounting)
    return gaslift_price / discounting_savings


def get_esp_frequency_control_DPBP() -> float:
    discounting_savings = (get_electric_submersible_pumps_cost() - get_esp_frequency_control_cost()) / (1 + discounting)
    return esp_frequency_control_price / discounting_savings


# ------------------------------------------------------

'''
РАССЧИТАЕМ ДИСКОНТИРОВАННЫЙ ДЕНЕЖНЫЙ ПОТОК
'''


def get_gaslift_NPV(t: int = 1) -> float:
    npv = 0
    for year in range(1, t + 1):
        npv += (get_electric_submersible_pumps_cost(year) - get_gaslift_cost(year)) / (1 + discounting) ** year
    return npv


def get_esp_frequency_control_NPV(t: int = 1) -> float:
    npv = 0
    for year in range(1, t + 1):
        npv += (get_electric_submersible_pumps_cost(year) - get_esp_frequency_control_cost(year)) / (
                1 + discounting) ** year
    return npv


# ------------------------------------------------------

'''
РАССЧИТАЕМ ИНДЕКС РЕНТАБЕЛЬНОСТИ ПРОЕКТА ДЛЯ КАЖДОЙ МОДЕРНИЗАЦИИ
'''


def get_gaslift_PI(t: int = 1) -> float:
    return 1 + get_gaslift_NPV(t) / gaslift_price


def get_esp_frequency_control_PI(t: int = 1) -> float:
    return 1 + get_esp_frequency_control_NPV(t) / esp_frequency_control_price


print('С УЧЕТОМ ПАДЕНИЯ ДЕБИТА')
print('PBP ЭЦН с частотным регулированием:', get_esp_frequency_control_PBP())
print('DPBP ЭЦН с частотным регулированием:', get_esp_frequency_control_DPBP())
print('NPV ЭЦН с частотным регулированием:', get_esp_frequency_control_NPV(16))
print('PI ЭЦН с частотным регулированием:', get_esp_frequency_control_PI(16))
print('----------------------------------------------------------------------------')
print('PBP Газлифтной системы:', get_gaslift_PBP())
print('DPBP Газлифтной системы:', get_gaslift_DPBP())
print('NPV Газлифтной системы:', get_gaslift_NPV(16))
print('PI Газлифтной системы:', get_gaslift_PI(16))
print('Дебит ДО/ПОСЛЕ перерасчета по формуле ДЮПЮИ')
print(get_barrels_per_period(16 * 365, 16))  # Падение дебита за 16 лет
print(10_000 * 365 * 16)  # Проверка для сравнения
