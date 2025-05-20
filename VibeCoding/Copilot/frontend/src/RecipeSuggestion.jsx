// RecipeSuggestion.jsx
import React, { useState } from "react";

function RecipeSuggestion() {
    const [ingredients, setIngredients] = useState("");
    const [suggestions, setSuggestions] = useState([]);

    const handleSubmit = (e) => {
        e.preventDefault();
        // Trasformare in array, eliminando eventuali spazi extra
        const ingredientArray = ingredients.split(",").map((i) => i.trim());
        fetch("http://localhost:3000/api/suggestions", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ ingredients: ingredientArray })
        })
            .then((res) => res.json())
            .then((data) => setSuggestions(data))
            .catch((err) => console.error(err));
    };

    return (
        <div>
            <h2>Suggerimenti Ricette in Base alla Dispensa</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    Ingredienti disponibili (separati da virgola):
                    <input
                        type="text"
                        value={ingredients}
                        onChange={(e) => setIngredients(e.target.value)}
                    />
                </label>
                <button type="submit">Cerca</button>
            </form>
            <ul>
                {suggestions.map((recipe) => (
                    <li key={recipe.id}>
                        <strong>{recipe.name}</strong> - Ingredienti: {recipe.ingredients.join(", ")}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default RecipeSuggestion;
