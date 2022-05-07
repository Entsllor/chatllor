import React from "react";
import AuthService from "../../services/auth";

const LogoutButton: React.FC<{ accessTokenHandler: CallableFunction }> = (props) => {
  return (
    <div className='LogoutButton'>
      <a href="" onClick={async () => {
        await AuthService.logout();
        props.accessTokenHandler("")
      }}>Logout</a>
    </div>
  )
}

export default LogoutButton;
