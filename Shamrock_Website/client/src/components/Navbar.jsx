import React, { useContext } from 'react'
import {Link} from "react-router-dom"
import Logo from "../img/shamrockLogo.png"
import { AuthContext } from '../context/authContext'

const Navbar = () => {

    const {currentUser, logout} = useContext(AuthContext);

  return (
    <div className="navbar">
        <div className="container">
            <div className="logo">
                <Link to="/">
                    <img src={Logo} alt="shamrock logo" />
                </Link>
            </div>
            <div className="links">
                <Link className='link' to="/">
                    <p>Home</p>
                </Link>
                <p>|</p>
                <p>{currentUser?.username}</p>
                {currentUser ? <span onClick={logout}>Logout</span> : <Link className="link" to="/login">Login</Link>}
            </div>
        </div>
    </div>
  )
}

export default Navbar