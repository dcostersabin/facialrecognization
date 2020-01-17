import React from "react";
import NavItems from "../NavItems/NavItems";

const NavBar = (props)=>{
    return(
        <nav class="navbar navbar-expand-md navbar-dark bg-dark fixed-top">

            <NavItems items={props.navItems}/>

        </nav>
    )
}