// App.jsx
import React from "react";
import "./App.css"; // importa il file CSS
import MealPlan from "./MealPlan";
import ShoppingList from "./ShoppingList";
import BudgetChart from "./BudgetChart";
import RecipeSuggestion from "./RecipeSuggestion";

function App() {
    return (
        <div className="container">
            <h1>Planner dei Pasti & Gestione Budget Alimentare</h1>
            <MealPlan />
            <hr />
            <ShoppingList />
            <hr />
            <BudgetChart />
            <hr />
            <RecipeSuggestion />
        </div>
    );
}

export default App;
