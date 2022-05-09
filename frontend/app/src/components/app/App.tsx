import React, {useEffect, useState} from 'react';
import AuthForm from "../auth-form/AuthForm";
import Header from "../header/Header";
import ChatList from "../chat-list/ChatList";
import {Chat, ChatUser} from "../../interfaces/chat";
import MessagesField from "../messages-field/MessagesField";
import ChatHeader from "../chat-header/ChatHeader";
import ChatService from "../../services/chat";

const App = () => {
  const [accessToken, setAccessToken] = useState<string | null>(localStorage.getItem('accessToken'))
  const [currentChat, setCurrentChat] = useState<Chat>()
  const [userChats, setUserChats] = useState<ChatUser[]>([])

  useEffect(() => {
    updateUserChats()
  }, [accessToken])

  const updateUserChats = async () => {
    await ChatService.fetchUserChats().then(response => setUserChats(response.data))
  }

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
              <ChatList userChats={userChats} handleCurrentChat={setCurrentChat}/>
            </div>
            <div className='col col-8'>
              {currentChat && <div>
                <ChatHeader chatsUpdater={updateUserChats} chat={currentChat} currentChatHandler={setCurrentChat}/>
                <MessagesField chatId={currentChat.id}/>
              </div>
              }
            </div>
          </div>
        }
      </div>
    </div>
  );
};

export default App;
