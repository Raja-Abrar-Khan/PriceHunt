import bcrypt from "bcryptjs";
import jwt from "jsonwebtoken";
import prisma from "../config/prisma.js";
import dotenv from "dotenv";

dotenv.config();
const JWT_SECRET=process.env.JWT_SECRET;

//USer is regestering here
export const registerUser=async (req,res) =>{
    try {
        const {email,password}=req.body;
        const existingUser=await prisma.user.findUnique({where:{email}});
        if(existingUser){
            return res.status(400).json({message:"user already exists"});
        }

        // create hash password
        const hashedPassword=await bcrypt.hash(password,10);

        // new user
        const newUser= await prisma.user.create({
            data:{
                email,
                password:hashedPassword,
            },
        });
        res.status(201).json({message: "User registered successfully",userId:newUser.id});
    } catch (error) {
        res.status(500).json({message: "Server error",error});
    }
}