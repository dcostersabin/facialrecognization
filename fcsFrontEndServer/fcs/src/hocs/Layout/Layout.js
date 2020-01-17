import React, {Component} from 'react';
import NavItems from "../../container/NavItems/NavItems";


class Layout extends Component
{

    state={
        navItems:[
            {id:1 , label:'Home'},
            {id:2 , label:'Services'},
            {id:3 , label:'About'},
            {id:4 , label:'Products'},
            {id:5 , label:'Contacts'},
        ]
    }

    render(){
        return(
            <main>

                <NavItems items={this.state.navItems}/>
            </main>
        )
    }

}

export default Layout;