import React from "react";
import { Navigate, Outlet } from "react-router-dom";

const ProtectedRoute = () => {
    const token = localStorage.getItem("token");

    // If token exists, allow access; otherwise, redirect to login
    return token ? <Outlet /> : <Navigate to="/login" />;
};

export default ProtectedRoute;