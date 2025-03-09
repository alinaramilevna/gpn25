"use client"; // ← Это обязательно!

import { useState } from "react";
import { Line } from "react-chartjs-2";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import "chart.js/auto";

export default function EnergyCalculator() {
  const [initialConsumption, setInitialConsumption] = useState(10000); // МДж
  const [years, setYears] = useState(10);
  const [tariff, setTariff] = useState(5); // руб/кВт*ч
  const [rateIncrease, setRateIncrease] = useState(15); // %
  const [efficiency, setEfficiency] = useState(0.05); // коэффициент ежегодного снижения (например, 5% или 0.05)
  const [energyPrice, setEnergyPrice] = useState(3); // начальная цена на электроэнергию (руб/кВт*ч)

  // Вычисляем данные для графика и совокупной экономии
  const data = Array.from({ length: years }, (_, t) => {
    const consumption = initialConsumption * Math.pow(1 - efficiency, t);
    return {
      year: t + 1,
      consumption,
    };
  });

  // Формула для расчета совокупной экономии в МДж
  const calculateSavings = () => {
    let totalSavings = 0;
    for (let t = 1; t < years; t++) {
      const previousConsumption = initialConsumption * Math.pow(1 - efficiency, t - 1);
      const currentConsumption = initialConsumption * Math.pow(1 - efficiency, t);
      totalSavings += previousConsumption - currentConsumption;
    }
    return totalSavings.toFixed(2); // Совокупная экономия в МДж
  };

  // Формула для расчета совокупной экономии в деньгах (с учетом роста тарифа)
  const calculateMonetarySavings = () => {
    let totalMonetarySavings = 0;
    let currentTariff = energyPrice; // Начальная цена на электроэнергию

    for (let t = 1; t < years; t++) {
      const previousConsumption = initialConsumption * Math.pow(1 - efficiency, t - 1);
      const currentConsumption = initialConsumption * Math.pow(1 - efficiency, t);

      // Вычисляем экономию в деньгах за год с учетом тарифа
      const yearlySavings = (previousConsumption - currentConsumption) * currentTariff;
      totalMonetarySavings += yearlySavings;

      // Каждый год цена на электроэнергию растет на rateIncrease %
      currentTariff *= (1 + rateIncrease / 100);
    }
    return totalMonetarySavings.toFixed(2); // Совокупная экономия в деньгах
  };

  // Конфигурация графика
  const chartData = {
    labels: data.map((d) => `Год ${d.year}`),
    datasets: [
      {
        label: "Энергопотребление (МДж)",
        data: data.map((d) => d.consumption),
        borderColor: "#ff3b30",
        backgroundColor: "rgba(255, 59, 48, 0.2)",
        tension: 0.3,
      },
    ],
  };

  return (
    <div className="min-h-screen bg-white text-black flex flex-col items-center p-6">
      <h1 className="text-2xl font-semibold mb-4">🔋 Калькулятор энергопотребления</h1>

      <div className="grid grid-cols-2 gap-4 w-full max-w-xl">
        <Card>
          <CardContent className="flex flex-col gap-2">
            <label>Начальное потребление (МДж)</label>
            <Input
              type="number"
              value={initialConsumption}
              onChange={(e) => setInitialConsumption(Number(e.target.value))}
            />
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex flex-col gap-2">
            <label>Время прогнозирования (лет)</label>
            <Input
              type="number"
              value={years}
              onChange={(e) => setYears(Number(e.target.value))}
            />
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex flex-col gap-2">
            <label>Коэффициент снижения энергопотребления (%)</label>
            <Input
              type="number"
              value={efficiency * 100} // отобразить процент
              onChange={(e) => setEfficiency(Number(e.target.value) / 100)}
            />
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex flex-col gap-2">
            <label>Повышение тарифа ежегодно (%)</label>
            <Input
              type="number"
              value={rateIncrease}
              onChange={(e) => setRateIncrease(Number(e.target.value))}
            />
          </CardContent>
        </Card>

        <Card>
          <CardContent className="flex flex-col gap-2">
            <label>Стоимость электроэнергии в первый год (руб/кВт*ч)</label>
            <Input
              type="number"
              value={energyPrice}
              onChange={(e) => setEnergyPrice(Number(e.target.value))}
            />
          </CardContent>
        </Card>
      </div>

      <div className="w-full max-w-2xl mt-6">
        <Line data={chartData} />
      </div>

      <div className="mt-6">
        <h2 className="text-xl font-semibold">Совокупная экономия в МДж</h2>
        <p className="text-lg">Суммарная экономия за {years} лет: {calculateSavings()} МДж</p>
      </div>

      <div className="mt-6">
        <h2 className="text-xl font-semibold">Совокупная экономия в деньгах</h2>
        <p className="text-lg">Суммарная экономия за {years} лет: {calculateMonetarySavings()} руб</p>
      </div>

      <Button className="mt-6 bg-black text-white px-4 py-2 rounded-lg shadow-md">
        Рассчитать экономию
      </Button>
    </div>
  );
}
