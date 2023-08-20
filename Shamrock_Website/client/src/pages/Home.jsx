import React, { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import axios from "axios"

const Home = () => {
    const [articles, setArticles] = useState([])

    useEffect(() => {
        const fetchData = async () => {
            try {
                const res = await axios.get("http://localhost:8080/api/articles")
                setArticles(res.data)
            } catch(err) {
                console.log(err)
            }
        }
        fetchData()
    })

    function parseDate(stamp) {
        // return(stamp.toLocaleDateString('en-us'))
        return stamp.slice(0,10) // until date parsing works
    }

  return (
    <div className='home'>
        <div className="articles">
            {articles.map(article => (
                <div className="article" key={article.id}>
                    <div className="img">
                        <img src={article.img} alt="article img" />
                    </div>
                    <div className="content">
                        <Link className="link" to={`/article/${article.id}`}>
                            <h1>{article.title}</h1>
                        </Link>
                        <p>{article.author}</p>
                        <p>{parseDate(article.date)}</p>
                        <button>
                            <Link className="link" to={`/article/${article.id}`}>
                                Read
                            </Link>
                        </button>
                    </div>
                </div>
            ))}
        </div> 
    </div>
  )
}

export default Home