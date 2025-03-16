"use client";

import { useState, useEffect } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

export default function EnergyCalculator() {
  const [startEnergy, setStartEnergy] = useState(10000000);
  const [time, setTime] = useState(10);
  const [energyLowCoeff, setEnergyLowCoeff] = useState(0.07);
  const [startPrice, setStartPrice] = useState(5);
  const [priceUpCoeff, setPriceUpCoeff] = useState(0.09);
  const [savings, setSavings] = useState(null);
  const [plotUrl, setPlotUrl] = useState("");

  const fetchSavings = async () => {
    const res = await fetch(
      `http://127.0.0.1:8000/savings?start_energy=${startEnergy}&time=${time}&energy_low_coeff=${energyLowCoeff}&start_price=${startPrice}&price_up_coeff=${priceUpCoeff}`
    );
    const data = await res.json();
    setSavings(data.savings);
  };

  const fetchPlot = async () => {
    const imgUrl = `http://127.0.0.1:8000/plot?start_energy=${startEnergy}&time=${time}&energy_low_coeff=${energyLowCoeff}`;
    setPlotUrl(imgUrl);
  };

  useEffect(() => {
    fetchSavings();
    fetchPlot();
  }, [startEnergy, time, energyLowCoeff, startPrice, priceUpCoeff]);

  // Округление значений до нужной точности
  const roundToFixed = (num: number, decimals: number) => {
    return Number(num.toFixed(decimals));
  };

  return (
    <div className="min-h-screen bg-white text-black flex flex-col items-center p-6">
      <h1 className="text-2xl font-semibold mb-4">🔋 Калькулятор энергопотребления</h1>

      <div className="grid grid-cols-2 gap-4 w-full max-w-xl">
        <Card>
          <CardContent>
            <label>Начальное потребление (МДж)</label>
            <Input
              type="number"
              value={startEnergy}
              onChange={(e) => setStartEnergy(Number(e.target.value))}
            />
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <label>Время прогнозирования (лет)</label>
            <Input
              type="number"
              value={time}
              onChange={(e) => setTime(Number(e.target.value))}
            />
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <label>Коэффициент снижения энергопотребления (%)</label>
            <Input
              type="number"
              value={roundToFixed(energyLowCoeff * 100, 2)} // Отображаем с 2 знаками после запятой
              onChange={(e) => setEnergyLowCoeff(Number(e.target.value) / 100)}
            />
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <label>Начальная стоимость электроэнергии (руб/кВт*ч)</label>
            <Input
              type="number"
              value={roundToFixed(startPrice, 2)} // Отображаем с 2 знаками после запятой
              onChange={(e) => setStartPrice(Number(e.target.value))}
            />
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <label>Годовое увеличение тарифа (%)</label>
            <Input
              type="number"
              value={roundToFixed(priceUpCoeff * 100, 2)} // Отображаем с 2 знаками после запятой
              onChange={(e) => setPriceUpCoeff(Number(e.target.value) / 100)}
            />
          </CardContent>
        </Card>
      </div>

      <div className="mt-6">
        <h2 className="text-xl font-semibold">Экономия</h2>
        {savings !== null && Array.isArray(savings) ? (
          <div className="text-lg">
            <p>🔹 Энергия: {roundToFixed(savings[0], 2)} МДж</p> {/* Округляем и отображаем */}
            <p>💰 Деньги: {roundToFixed(savings[1], 2)} руб</p> {/* Округляем и отображаем */}
          </div>
        ) : (
          <p>Загрузка...</p>
        )}
      </div>

      <div className="mt-6">
        <h2 className="text-xl font-semibold">График энергопотребления</h2>
        {plotUrl && <img src={plotUrl} alt="График" className="mt-4 w-full max-w-2xl" />}
      </div>

      <Button className="mt-6 bg-black text-white px-4 py-2 rounded-lg shadow-md" onClick={() => {
        fetchSavings();
        fetchPlot();
      }}>
        Обновить данные
      </Button>
    </div>
  );
}
