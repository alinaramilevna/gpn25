import matplotlib.pyplot as plt
import numpy as np


def get_plot(start_energy: int, time: int, energy_low_coeff: float):
    '''

        :param start_energy: Energy costs at the beginning of the production (МДж)
        :param time: Term to prediction in years
        :param energy_low_coeff: Coefficient (for example 0.05 if annual reducing is 5%) of reducing energy consumption
        :return: None (saves file with plot in ../tmp
        '''

    plt.style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(8, 4))

    a = (1 - energy_low_coeff)
    x_min = 1
    x_max = time
    num_points = 120

    x = np.linspace(x_min, x_max, num_points)
    y = start_energy * a ** x

    ax.plot(x, y, label=f"Снижение {energy_low_coeff * 100:.1f}%", linewidth=2)

    ax.set_title("Экспоненциальное падение затрат электроэнергии", fontsize=14, fontweight='bold')
    ax.set_xlabel("Год", fontsize=12)
    ax.set_ylabel("Затраты, МДж", fontsize=12)
    ax.legend(title="Ежегодное снижение", fontsize=10)
    ax.grid(True, linestyle="--", alpha=0.7)

    plt.savefig(f'tmp/{start_energy}-{time}-{energy_low_coeff}.png')
    # DEBUG
    # plt.show()

# DEBUG
# get_plot(10_000_000, 10, 0.05)
