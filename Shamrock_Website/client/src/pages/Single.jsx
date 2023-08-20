import React, { useEffect, useState } from 'react'
import axios from 'axios'
import { useLocation } from 'react-router'

function Single() {
  const [article, setArticle] = useState([])

  const location = useLocation()
  const articleID = location.pathname.split("/")[2]

  useEffect(() => {
      const fetchData = async () => {
          try {
              const res = await axios.get(`http://localhost:8080/api/articles/${articleID}`)
              setArticle(res.data)
          } catch(err) {
              console.log(err)
          }
      }
      fetchData()
  }, [articleID]);

//   function parseDate(stamp) {
//       // return(stamp.toLocaleDateString('en-us'))
//       return stamp.slice(0,10) // until date parsing works
//   }

  console.log(article)
  return (
    <div className='single'>
        <div className="content">
             <img src={article.img} alt="" />
             <h1>{article.title}</h1>
                 <div className="info">
                    <span>{article.author}</span>
                    <br/> 
                    {article.date && <span>{article.date.slice(0,10)}</span>}
                    <br/>
                 </div>
              <p>{article.article}</p>
          </div>
    </div>
  )
}

export default Single