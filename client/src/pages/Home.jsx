import React from "react";
import { useNavigate } from "react-router-dom";

const Home = () => {
    const navigate = useNavigate();

    return (
        <div className="flex flex-col items-center justify-center h-screen bg-gray-100">
            <h1 className="text-4xl font-bold mb-4">Welcome to Price Tracker</h1>
            <p className="text-lg text-gray-700 mb-8">
                Track prices of your favorite products and get alerts when prices drop!
            </p>
            <button
                onClick={() => navigate("/login")}
                className="bg-blue-500 text-white px-6 py-2 rounded-lg hover:bg-blue-600"
            >
                Try It
            </button>
        </div>
    );
};

export default Home;