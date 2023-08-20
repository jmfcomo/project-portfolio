import {db} from "../db.js"

export const getArticles = (req, res) => {
    const q = "SELECT * FROM articles";

    db.query(q, (err, data) => {
        if (err) return res.send(err)

        return res.status(200).json(data)
    })
}

export const getArticle = (req, res) => {
    const q = "SELECT * FROM articles WHERE id = ?;";

    db.query(q, [req.params.id], (err, data) => {
        if (err) return res.status(500).json(err);
    
        return res.status(200).json(data[0]);
      });
}