import express from "express"
import {getArticle, getArticles} from "../controllers/article.js"

const router = express.Router()

router.get("/", getArticles)
router.get("/:id", getArticle)

export default router