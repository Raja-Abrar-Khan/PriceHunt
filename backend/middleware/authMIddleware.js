import jwt from "jsonwebtoken";
import dotenv from "dotenv";

dotenv.config();
const JWT_SECRET=process.env.JWT_SECRET;

// middle ware to verify the token
export const verifyToken=(req,res,next)=>{
    const authHeader=req.headers.authorization;

    if(!authHeader|| !authHeader.startsWith("Bearer ")){
        return res.status(401).json({message:"Unauthorized: No token provided"});
    }

    const token=authHeader.split(" ")[1]; //Extract token

    try {
        const decoded=jwt.verify(token,JWT_SECRET);
        req.user=decoded;
        next();
    } catch (error) {
        return res.status(403).json({ message: "Forbidden: Invalid or expired token" });
    }
}