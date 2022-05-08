import React, {useState} from 'react';
import AuthForm from "../auth-form/AuthForm";
import Header from "../header/Header";
import ChatList from "../chat-list/ChatList";
import {Chat} from "../../interfaces/chat";
import MessagesField from "../messages-field/MessagesField";

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
          <div className='row row-cols-2'>
            <div className='col col-4'>
              <ChatList handleCurrentChat={setCurrentChat}/>
            </div>
            <div className='col col-8'>
              {currentChat?.id && <MessagesField chatId={currentChat.id}/>}
            </div>
          </div>
        }
      </div>
    </div>
  );
};

export default App;
