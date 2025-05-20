// server.js
const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
app.use(express.json());

// Dati di esempio per il piano settimanale
const mealPlan = [
    {
        day: "Lunedì",
        breakfast: { recipe: "Porridge", ingredients: ["avena", "latte", "miele", "frutta"] },
        lunch: { recipe: "Insalata di pollo", ingredients: ["pollo", "insalata", "pomodori", "olio"] },
        dinner: { recipe: "Spaghetti al pomodoro", ingredients: ["spaghetti", "pomodoro", "basilico", "olio", "formaggio"] }
    },
    {
        day: "Martedì",
        breakfast: { recipe: "Smoothie alla frutta", ingredients: ["banana", "fragole", "yogurt", "miele"] },
        lunch: { recipe: "Risotto ai funghi", ingredients: ["riso", "funghi", "brodo", "formaggio", "vino bianco"] },
        dinner: { recipe: "Zuppa di verdure", ingredients: ["carota", "patata", "sedano", "cipolla", "pomodoro"] }
    }
    // Prosegui per il resto della settimana...
];

// Endpoint per ottenere il piano dei pasti
app.get("/api/meal-plan", (req, res) => {
    res.json(mealPlan);
});

// Endpoint per generare la lista della spesa (senza duplicati)
app.get("/api/shopping-list", (req, res) => {
    const ingredientsSet = new Set();
    mealPlan.forEach(day => {
        ["breakfast", "lunch", "dinner"].forEach(mealType => {
            day[mealType].ingredients.forEach(ingredient => ingredientsSet.add(ingredient));
        });
    });
    const shoppingList = Array.from(ingredientsSet);
    res.json(shoppingList);
});

// Dati di esempio per il monitoraggio del budget
const budgetData = {
    monthlyBudget: 300, // euro
    expenses: [
        { date: "2025-05-01", amount: 25 },
        { date: "2025-05-05", amount: 40 },
        { date: "2025-05-10", amount: 30 }
    ]
};

app.get("/api/budget", (req, res) => {
    res.json(budgetData);
});

// Ricette preferite salvate dall'utente
const favoriteRecipes = [
    { id: 1, name: "Pesto Genovese", ingredients: ["basilico", "pinoli", "parmigiano", "olio d'oliva", "aglio"] },
    { id: 2, name: "Lasagne", ingredients: ["pasta", "carne macinata", "besciamella", "pomodoro", "formaggio"] }
];

app.get("/api/favorite-recipes", (req, res) => {
    res.json(favoriteRecipes);
});

// Suggerimenti ricette in base agli ingredienti disponibili in dispensa
const allRecipes = [
    { id: 3, name: "Frittata di verdure", ingredients: ["uova", "spinaci", "pomodorini"] },
    { id: 4, name: "Panino con tonno", ingredients: ["pane", "tonno", "maionese", "insalata"] },
    { id: 5, name: "Minestrone", ingredients: ["carota", "patata", "fagioli", "pomodoro", "sedano"] }
];

app.post("/api/suggestions", (req, res) => {
    const availableIngredients = req.body.ingredients; // Array di ingredienti
    const suggestions = allRecipes.filter(recipe => {
        return recipe.ingredients.some(ing => availableIngredients.includes(ing));
    });
    res.json(suggestions);
});

// Avvio del server
app.listen(3000, () =>
    console.log("Server in esecuzione su http://localhost:3000")
);
