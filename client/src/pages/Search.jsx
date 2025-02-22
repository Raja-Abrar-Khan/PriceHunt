import React, { useState } from "react";
import axios from "axios";

const Search = () => {
    const [query, setQuery] = useState("");
    const [products, setProducts] = useState([]);
    const [error, setError] = useState("");

    const handleSearch = async () => {
        try {
            const token = localStorage.getItem("token");
            const response = await axios.post("http://localhost:5001/price/product", { query }, {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            });
            setProducts(response.data);
        } catch (error) {
            setError("You must be logged in to search for products.");
        }
    };

    return (
        <div className="p-4">
            <h1 className="text-2xl font-bold mb-4">Search Products</h1>
            <input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Search for a product"
                className="p-2 border rounded"
            />
            <button
                onClick={handleSearch}
                className="p-2 bg-blue-500 text-white rounded ml-2"
            >
                Search
            </button>
            {error && <p className="text-red-500 mt-4">{error}</p>}
            <div className="mt-4">
                {products.map((product) => (
                    <div key={product.id} className="p-4 border rounded mb-2">
                        <h2 className="text-xl font-bold">{product.title}</h2>
                        <p>Price: {product.currentPrice}</p>
                        <img src={product.image} alt={product.title} className="w-32 h-32" />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default Search;