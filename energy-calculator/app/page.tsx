"use client";

import { useState, useEffect } from "react";
import dynamic from "next/dynamic";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

// Регистрируем модули Chart.js
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
  const [chartData, setChartData] = useState(null);

  useEffect(() => {
    const data = Array.from({ length: years }, (_, t) => {
      const consumption = initialConsumption * Math.pow(1 - efficiency, t);
      return {
        year: t + 1,
        consumption: isNaN(consumption) || consumption < 0 ? 0 : consumption,
      };
    });

    // Логируем данные для графика
    console.log("📊 Проверка данных для графика:", data);

    // Проверим, есть ли некорректные данные
    const invalidData = data.some((d) => d.consumption === 0);
    if (invalidData) {
      console.error("Ошибка: Есть некорректные данные в графике (0 или NaN)");
    }

    setChartData({
      labels: data.map((d) => `Год ${d.year}`),
      datasets: [
        {
          label: "Энергопотребление (МДж)",
          data: data.map((d) => d.consumption),
          borderColor: "#ff3b30",
          backgroundColor: "rgba(255, 59, 48, 0.2)",
          pointRadius: 3, // Делаем точки видимыми
          pointBackgroundColor: "#ff3b30",
          pointBorderColor: "#fff",
          fill: false,
        },
      ],
    });
  }, [initialConsumption, years, efficiency]);

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    scales: {
      x: {
        title: {
          display: true,
          text: "Годы",
        },
      },
      y: {
        beginAtZero: false,
        title: {
          display: true,
          text: "Энергопотребление (МДж)",
        },
      },
    },
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
        {chartData ? (
          <>
            {console.log("Финальные данные для графика:", chartData)}
            <Line data={chartData} options={chartOptions} />
          </>
        ) : (
          <p className="text-center">⏳ Загрузка графика...</p>
        )}
      </div>

      <Button className="mt-6 bg-black text-white px-4 py-2 rounded-lg shadow-md">
        Рассчитать экономию
      </Button>
    </div>
  );
}
