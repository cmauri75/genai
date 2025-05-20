// ShoppingList.jsx
import React, { useState, useEffect } from "react";

function ShoppingList() {
    const [shoppingList, setShoppingList] = useState([]);
    const [checkedItems, setCheckedItems] = useState([]);

    useEffect(() => {
        fetch("http://localhost:3000/api/shopping-list")
            .then((res) => res.json())
            .then((data) => setShoppingList(data))
            .catch((err) => console.error(err));
    }, []);

    const toggleItem = (item) => {
        setCheckedItems((prev) =>
            prev.includes(item) ? prev.filter((i) => i !== item) : [...prev, item]
        );
    };

    return (
        <div>
            <h2>Lista della Spesa</h2>
            <ul>
                {shoppingList.map((item, index) => (
                    <li key={index}>
                        <input
                            type="checkbox"
                            checked={checkedItems.includes(item)}
                            onChange={() => toggleItem(item)}
                        />{" "}
                        {item}
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default ShoppingList;
