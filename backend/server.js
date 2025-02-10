import express from "express";
import colors from "colors";
import { PrismaClient } from "@prisma/client";
import { config } from "dotenv";
import cors from "cors";
import authRoutes from "./route/authRoutes.js";

config();

const prisma =new PrismaClient();
const app=express();
const PORT=process.env.PORT;

app.use(cors());
app.use(express.json());
app.use("/auth",authRoutes);

app.get("/",(req,res)=>{
    res.send("hieeee");
})
const connectPostgress=async()=>{
try {
    const result=await prisma.$queryRaw`SELECT current_database()`;
    console.log(`connected to the database: ${result[0].current_database}`.bgWhite.black);
} catch (error) {
    console.error("Error connection to the datatbase".bgRed.white,error.message);
}
}

app.listen(PORT,()=>{
    console.log(`Server is running on ${PORT}`.bgGreen.bgBlack);
    connectPostgress();
})
