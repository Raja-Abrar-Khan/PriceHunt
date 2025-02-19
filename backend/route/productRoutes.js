import express from "express";
import { getProduct } from "../controller/productController.js";

const router=express.Router();
router.post("/product",getProduct);

export default router;