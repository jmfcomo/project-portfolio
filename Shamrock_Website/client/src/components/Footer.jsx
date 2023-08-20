import React from 'react'
import Logo from "../img/shamrockLogo.png"

const Footer = () => {
  return (
    <footer>
        <img src={Logo} alt="shamrock logo" />
        <span>
            Made with <b>React.js</b>
        </span>
    </footer>
  )
}

export default Footer