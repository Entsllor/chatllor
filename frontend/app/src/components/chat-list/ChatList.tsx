import React, {useEffect, useState} from "react";
import {ChatUser} from "../../interfaces/chat";
import ChatService from "../../services/chat";

const ChatList: React.FC<{}> = (props) => {
  const [chats, setChats] = useState<ChatUser[]>([])

  useEffect(() => {
    ChatService.fetchUserChats().then(response => setChats(response.data))
  }, [])
  return (
    <div className='ChatList'>
      <div className="d-flex flex-column gap-1">
        {chats.map((chat_user) =>
          <div key={chat_user.chat.id}>
            {chat_user.chat.name}
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatList;
