import express from "express"
import articleRoutes from "./routes/articles.js"
import authRoutes from "./routes/auth.js"
import cookieParser from "cookie-parser"


const app = express()

app.use(express.json())
app.use(cookieParser())
app.use("/api/articles", articleRoutes)
app.use("/api/auth", authRoutes)

app.listen(8080,() => {
    console.log("Connected")
})