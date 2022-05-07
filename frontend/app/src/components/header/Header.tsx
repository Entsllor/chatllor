import React from "react";
import AuthService from "../../services/auth";


const Header: React.FC<{ handleAccessToken: CallableFunction; accessToken: string | null }> = (props) => {
  return <div className="Header">
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark">
      <div className="container-fluid">
        <a className="navbar-brand" href="#">Chatllor</a>
        <a className="link-light" href="#" onClick={async () => {
          await AuthService.logout();
          props.handleAccessToken("")
        }}>{props.accessToken ? "Log Out" : "Sign In"}</a>
      </div>
    </nav>
  </div>;
};


export default Header
