import React, {useState} from 'react';
import AuthForm from "../auth-form/AuthForm";
import Header from "../header/Header";
import ChatList from "../chat-list/ChatList";

const App = () => {
  const [accessToken, setAccessToken] = useState<string | null>(localStorage.getItem('accessToken'))

  return (
    <div className="App">
      <Header handleAccessToken={setAccessToken} accessToken={accessToken}/>
      <div className="container mt-3">
        {!accessToken ?
          <AuthForm handleAccessToken={setAccessToken}/> :
          <ChatList/>
        }
      </div>
    </div>
  );
};

export default App;
