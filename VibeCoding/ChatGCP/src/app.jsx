import { useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Calendar } from "@/components/ui/calendar";
import { LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer } from "recharts";

const sampleRecipes = [
    { name: "Pasta al Pomodoro", ingredients: ["pasta", "pomodori", "olio"], id: 1 },
    { name: "Insalata di Riso", ingredients: ["riso", "tonno", "piselli"], id: 2 },
    { name: "Frittata di Zucchine", ingredients: ["uova", "zucchine"], id: 3 },
];

const pantry = ["pasta", "olio", "uova", "zucchine"];

const budgetData = [
    { month: "Gen", spesa: 120 },
    { month: "Feb", spesa: 95 },
    { month: "Mar", spesa: 130 },
    { month: "Apr", spesa: 110 },
];

export default function MealPlannerApp() {
    const [meals, setMeals] = useState({});
    const [shoppingList, setShoppingList] = useState([]);
    const [budget, setBudget] = useState(150);
    const [expenses, setExpenses] = useState(0);

    function planMeal(day, mealType, recipe) {
        setMeals((prev) => ({
            ...prev,
            [day]: { ...prev[day], [mealType]: recipe },
        }));
        generateShoppingList();
    }

    function generateShoppingList() {
        const ingredients = new Set();
        Object.values(meals).forEach((dayMeals) => {
            Object.values(dayMeals).forEach((meal) => {
                meal?.ingredients?.forEach((i) => !pantry.includes(i) && ingredients.add(i));
            });
        });
        setShoppingList([...ingredients]);
    }

    function suggestRecipes() {
        return sampleRecipes.filter((r) => r.ingredients.every((i) => pantry.includes(i)));
    }

    return (
        <div className="p-4 space-y-4">
            <h1 className="text-2xl font-bold">Pianificazione Settimanale dei Pasti</h1>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {/* Calendario visuale */}
                <Card>
                    <CardContent className="p-4">
                        <h2 className="text-xl font-semibold mb-2">Pasti della Settimana</h2>
                        {["Lunedì", "Martedì", "Mercoledì", "Giovedì", "Venerdì", "Sabato", "Domenica"].map((day) => (
                            <div key={day} className="mb-2">
                                <strong>{day}</strong>
                                <div className="grid grid-cols-3 gap-2 text-sm">
                                    {["Colazione", "Pranzo", "Cena"].map((mealType) => (
                                        <Button
                                            variant="outline"
                                            onClick={() => planMeal(day, mealType, sampleRecipes[Math.floor(Math.random() * sampleRecipes.length)])}
                                            key={mealType}
                                        >
                                            {meals[day]?.[mealType]?.name || mealType}
                                        </Button>
                                    ))}
                                </div>
                            </div>
                        ))}
                    </CardContent>
                </Card>

                {/* Lista della spesa */}
                <Card>
                    <CardContent className="p-4">
                        <h2 className="text-xl font-semibold mb-2">Lista della Spesa</h2>
                        {shoppingList.length === 0 ? (
                            <p>Nessun ingrediente necessario.</p>
                        ) : (
                            <ul className="list-disc pl-4">
                                {shoppingList.map((item) => (
                                    <li key={item}>{item}</li>
                                ))}
                            </ul>
                        )}
                    </CardContent>
                </Card>

                {/* Budget e Spese */}
                <Card className="col-span-1 md:col-span-2">
                    <CardContent className="p-4">
                        <h2 className="text-xl font-semibold mb-2">Budget Alimentare</h2>
                        <Input
                            type="number"
                            placeholder="Imposta budget mensile"
                            value={budget}
                            onChange={(e) => setBudget(Number(e.target.value))}
                        />
                        <p className="mt-2">Totale spese: €{expenses}</p>
                        <p>Budget rimanente: €{budget - expenses}</p>
                        <ResponsiveContainer width="100%" height={200}>
                            <LineChart data={budgetData}>
                                <XAxis dataKey="month" />
                                <YAxis />
                                <Tooltip />
                                <Line type="monotone" dataKey="spesa" stroke="#82ca9d" />
                            </LineChart>
                        </ResponsiveContainer>
                    </CardContent>
                </Card>

                {/* Suggerimenti in base alla dispensa */}
                <Card>
                    <CardContent className="p-4">
                        <h2 className="text-xl font-semibold mb-2">Ricette dalla Dispensa</h2>
                        <ul className="list-disc pl-4">
                            {suggestRecipes().map((r) => (
                                <li key={r.id}>{r.name}</li>
                            ))}
                        </ul>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
