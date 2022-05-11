import React, {useEffect, useState} from "react";
import {Chat} from "../../interfaces/chat";
import ChatService from "../../services/chat";

const ChatSearch: React.FC<{}> = (props) => {
  const [chats, setChats] = useState<Chat[]>([])

  useEffect(() => {
    ChatService.fetchChats().then(response => setChats(response.data));
  }, [])

  return (
    <div className='ChatSearch'>
      {chats.map((chat) => (
        <div key={chat.id} className="card card-header mb-3">
          {chat.name}
        </div>
      ))}
    </div>
  )
};

export default ChatSearch;
