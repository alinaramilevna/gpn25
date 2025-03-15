"use client";

import { useState } from "react";
import dynamic from "next/dynamic";
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend } from "chart.js";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

// Регистрируем нужные модули для Chart.js
ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, Title, Tooltip, Legend);

// Динамический импорт графика с отключенным SSR
const Line = dynamic(() => import("react-chartjs-2").then((mod) => mod.Line), {
  ssr: false,
});

export default function EnergyCalculator() {
  const [initialConsumption, setInitialConsumption] = useState(10000);
  const [years, setYears] = useState(10);
  const [rateIncrease, setRateIncrease] = useState(15);
  const [efficiency, setEfficiency] = useState(0.05);
  const [energyPrice, setEnergyPrice] = useState(3);

  const data = Array.from({ length: years }, (_, t) => ({
    year: t + 1,
    consumption: initialConsumption * Math.pow(1 - efficiency, t),
  }));

  const calculateSavings = () => {
    let totalSavings = 0;
    for (let t = 1; t < years; t++) {
      totalSavings +=
        initialConsumption * Math.pow(1 - efficiency, t - 1) -
        initialConsumption * Math.pow(1 - efficiency, t);
    }
    return totalSavings.toFixed(2);
  };

  const calculateMonetarySavings = () => {
    let totalMonetarySavings = 0;
    let currentTariff = energyPrice;

    for (let t = 1; t < years; t++) {
      const yearlySavings =
        (initialConsumption * Math.pow(1 - efficiency, t - 1) -
          initialConsumption * Math.pow(1 - efficiency, t)) *
        currentTariff;
      totalMonetarySavings += yearlySavings;
      currentTariff *= 1 + rateIncrease / 100;
    }
    return totalMonetarySavings.toFixed(2);
  };

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
              value={efficiency * 100}
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
        {Line && <Line data={chartData} />}
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
