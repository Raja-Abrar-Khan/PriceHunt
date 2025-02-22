import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Search from "./pages/Search";
import ProtectedRoute from "./components/ProtectedRoute";

function App() {
    const [token, setToken] = useState(localStorage.getItem("token") || "");

    return (
        <Router>
            <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login setToken={setToken} />} />
                <Route path="/register" element={<Register setToken={setToken} />} />
                <Route element={<ProtectedRoute />}>
                    <Route path="/search" element={<Search />} />
                </Route>
            </Routes>
        </Router>
    );
}

export default App;