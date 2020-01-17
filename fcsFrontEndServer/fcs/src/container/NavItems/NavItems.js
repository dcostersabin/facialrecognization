import React from "react";

const NavItems = (props)=>{
    return(
        <ul className="collapse navbar-collapse">
            {props.items.map(item=>(
                <NavItem item={item}/>
            ))}
        </ul>
    )
};

const NavItem =(props)=>{
    return(
        <li className="nav-item active">
            {props.item.label}
        </li>
    )
}
export default NavItems;