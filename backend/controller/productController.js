import prisma from "../config/prisma.js";
import dayjs from "dayjs";
import axios from "axios";

const SCRAPER_URL = "http://127.0.0.1:5000/search";

export const getProduct = async (req, res) => {
    try {
        const { query } = req.body;

        //products in db or not
        const existingProducts = await prisma.product.findMany({
            where: {
                title: {
                    contains: query,
                    mode: "insensitive",
                },
            }
        });
        // check the time etc
        const freshProducts = existingProducts.filter(product => {
            const lastUpdated = new Date(product.lastUpdated);
            const hoursSinceLastUpdated = (new Date() - lastUpdated) / 1000 / 3600;
            return hoursSinceLastUpdated <= 24;
        });

        //return the rsponse
        if (freshProducts.length > 0) {
            return res.json(freshProducts);
        }

        //if all are outdated produts then we do this
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

        //now we scrape as nothing exists in theh db
        const response = await axios.post(SCRAPER_URL, { query });
        const scrapedProducts = response.data;

        await prisma.product.createMany({
            data: scrapedProducts.map(product => ({
                title: product.title,
                url: product.title,
                image: product.image,
                currentPrice: product.currentPrice,
                lastUpdated: new Date(),
            })
            ),
        });
        return res.json(scrapedProducts);
    } catch (error) {
        console.error("Error fetching products:", error);
        return res.status(500).json({ message: "Internal Server Error" });
    }
}

