import React, {useState} from 'react';
import AuthForm from "../auth-form/AuthForm";
import AuthService from "../../services/auth";
import LogoutButton from "../logout_button/LogoutButton";

const App = () => {
  const [accessToken, setAccessToken] = useState<string | null>(localStorage.getItem('accessToken'))

  return (
    <div className="App">
      <div className="container">
        {!accessToken ?
          <AuthForm handleAccessToken={setAccessToken}/> :
          <LogoutButton accessTokenHandler={setAccessToken}/>
        }
      </div>
    </div>
  );
};

export default App;
