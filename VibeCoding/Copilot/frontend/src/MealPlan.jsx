// MealPlan.jsx
import React, { useState, useEffect } from "react";

function MealPlan() {
    const [mealPlan, setMealPlan] = useState([]);

    useEffect(() => {
        fetch("http://localhost:3000/api/meal-plan")
            .then((res) => res.json())
            .then((data) => setMealPlan(data))
            .catch((err) => console.error(err));
    }, []);

    return (
        <div>
            <h2>Pianificazione Settimanale</h2>
            {mealPlan.map((day, index) => (
                <div key={index} style={{ borderBottom: "1px solid #ddd", padding: "10px 0" }}>
                    <h3>{day.day}</h3>
                    <p>
                        <strong>Colazione:</strong> {day.breakfast.recipe}
                    </p>
                    <p>
                        <strong>Pranzo:</strong> {day.lunch.recipe}
                    </p>
                    <p>
                        <strong>Cena:</strong> {day.dinner.recipe}
                    </p>
                </div>
            ))}
        </div>
    );
}

export default MealPlan;
