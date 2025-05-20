// BudgetChart.jsx
import React, { useState, useEffect } from "react";
import { Bar } from "react-chartjs-2";
import { Chart, BarElement, CategoryScale, LinearScale } from "chart.js";

Chart.register(BarElement, CategoryScale, LinearScale);

function BudgetChart() {
    const [budgetData, setBudgetData] = useState({ monthlyBudget: 0, expenses: [] });

    useEffect(() => {
        fetch("http://localhost:3000/api/budget")
            .then((res) => res.json())
            .then((data) => setBudgetData(data))
            .catch((err) => console.error(err));
    }, []);

    const totalSpent = budgetData.expenses.reduce(
        (sum, expense) => sum + expense.amount,
        0
    );

    const data = {
        labels: ["Budget", "Spese"],
        datasets: [
            {
                label: "Euro",
                data: [budgetData.monthlyBudget, totalSpent],
                backgroundColor: [
                    "rgba(75, 192, 192, 0.6)",
                    "rgba(255, 99, 132, 0.6)"
                ]
            }
        ]
    };

    return (
        <div style={{ width: "100%", height: 300 }}>
            <h2>Monitoraggio Budget Mensile</h2>
            <Bar data={data} options={{ responsive: true, maintainAspectRatio: false }} />
        </div>
    );
}

export default BudgetChart;
