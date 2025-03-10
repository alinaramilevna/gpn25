'''
В файле приведен расчет без учета падения дебита
'''
from math import ceil

from consts import debit_in_barrel, electric_submersible_pumps_energy, e_price, esp_frequency_control_energy, \
    esp_frequency_control_price, gaslift_energy, gaslift_price, discounting


def get_barrels_per_year() -> int:
    # возьмем 365 дней в году
    return debit_in_barrel * 365


def get_barrels_per_month() -> int:
    # возьмем 30 дней в месяце
    return debit_in_barrel * 30


# ------------------------------------------------------


def get_electric_submersible_pumps_cost() -> int:
    # 1. Переводим Дж в кВт·ч (1 кВт·ч = 3 600 000 Дж)
    # 2. Умножаем на стоимость электроэнергии
    return ceil((electric_submersible_pumps_energy / 3_600_000) * e_price * get_barrels_per_year())


def get_electric_submersible_pumps_PBP() -> float:
    # т к затраты на внедрение нулевые
    return 0


# ------------------------------------------------------

def get_esp_frequency_control_cost() -> int:
    return ceil((esp_frequency_control_energy / 3_600_000) * e_price * get_barrels_per_year())


def get_esp_frequency_control_PBP() -> float:
    savings = get_electric_submersible_pumps_cost() - get_esp_frequency_control_cost()
    return esp_frequency_control_price / savings


def get_gaslift_cost() -> int:
    return ceil((gaslift_energy / 3_600_000) * e_price * get_barrels_per_year())


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
        npv += (get_electric_submersible_pumps_cost() - get_gaslift_cost()) / (1 + discounting) ** year
    return npv


def get_esp_frequency_control_NPV(t: int = 1) -> float:
    npv = 0
    for year in range(1, t + 1):
        npv += (get_electric_submersible_pumps_cost() - get_esp_frequency_control_cost()) / (1 + discounting) ** year
    return npv


# ------------------------------------------------------

'''
РАССЧИТАЕМ ИНДЕКС РЕНТАБЕЛЬНОСТИ ПРОЕКТА ДЛЯ КАЖДОЙ МОДЕРНИЗАЦИИ
'''


def get_gaslift_PI(t: int = 1) -> float:
    return 1 + get_gaslift_NPV(t) / gaslift_price


def get_esp_frequency_control_PI(t: int = 1) -> float:
    return 1 + get_esp_frequency_control_NPV(t) / esp_frequency_control_price


print('БЕЗ УЧЕТА ПАДЕНИЯ ДЕБИТА')
print('PBP ЭЦН с частотным регулированием:', get_esp_frequency_control_PBP())
print('DPBP ЭЦН с частотным регулированием:', get_esp_frequency_control_DPBP())
print('NPV ЭЦН с частотным регулированием:', get_esp_frequency_control_NPV())
print('PI ЭЦН с частотным регулированием:', get_esp_frequency_control_PI(16))
print('----------------------------------------------------------------------------')
print('PBP Газлифтной системы:', get_gaslift_PBP())
print('DPBP Газлифтной системы:', get_gaslift_DPBP())
print('NPV Газлифтной системы:', get_gaslift_NPV())
print('PI Газлифтной системы:', get_gaslift_PI(16))
