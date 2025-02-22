import prisma from "../config/prisma.js";
import dayjs from "dayjs";
import axios from "axios";

const SCRAPER_URL = "http://127.0.0.1:5000/search";

export const getProduct = async (req, res) => {
    try {
        const { query } = req.body;
        console.log("Received query:", query);

        // Check if products exist in the database
        const existingProducts = await prisma.product.findMany({
            where: {
                title: {
                    contains: query,
                    mode: "insensitive",
                },
            }
        });
        console.log("Existing products:", existingProducts);

        // Filter fresh products (updated within 24 hours)
        const freshProducts = existingProducts.filter(product => {
            const lastUpdated = new Date(product.lastUpdated);
            const hoursSinceLastUpdated = (new Date() - lastUpdated) / 1000 / 3600;
            return hoursSinceLastUpdated <= 24;
        });
        console.log("Fresh products:", freshProducts);

        // Return fresh products if available
        if (freshProducts.length > 0) {
            return res.json(freshProducts);
        }

        // Delete outdated products
        await prisma.product.deleteMany({
            where: {
                title: {
                    contains: query,
                    mode: "insensitive",
                },
                lastUpdated: {
                    lt: new Date(new Date().setHours(new Date().getHours() - 24)),
                },
            },
        });

        // Call Flask scraper
        console.log("Calling Flask scraper...");
        console.log("Sending request to:", SCRAPER_URL); // Log the URL
        console.log("Request payload:", { query }); // Log the payload

        const response = await axios.post(SCRAPER_URL, { query }, {
            headers: {
                "Content-Type": "application/json",
            },
        });
        console.log("Response from Flask scraper:", response.data);
        const scrapedProducts = response.data;

        // Save scraped products to the database
        await prisma.product.createMany({
            data: scrapedProducts.map(product => ({
                title: product.title,
                url: product.title,
                image: product.image,
                currentPrice: product.currentPrice,
                lastUpdated: new Date(),
            })),
        });

        // Return scraped products
        return res.json(scrapedProducts);
    } catch (error) {
        console.error("Error fetching products:", error);
        if (error.response) {
            console.error("Flask scraper response error:", error.response.data);
        }
        return res.status(500).json({ message: "Internal Server Error" });
    }
}