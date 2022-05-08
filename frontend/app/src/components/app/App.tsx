import React, {useState} from 'react';
import AuthForm from "../auth-form/AuthForm";
import Header from "../header/Header";
import ChatList from "../chat-list/ChatList";
import {Chat, ChatUser} from "../../interfaces/chat";

const App = () => {
  const [accessToken, setAccessToken] = useState<string | null>(localStorage.getItem('accessToken'))
  const [currentChat, setCurrentChat] = useState<Chat>()

  return (
    <div className="App">
      <Header handleAccessToken={setAccessToken} accessToken={accessToken}/>
      <div className="container mt-3">
        {!accessToken ?
          // if not is authenticated 
          <AuthForm handleAccessToken={setAccessToken}/> :
          // if is authenticated
          <ChatList handleCurrentChat={setCurrentChat}/>
        }
      </div>
    </div>
  );
};

export default App;
