import React, {useEffect, useState} from "react";
import {Chat, ChatUser} from "../../interfaces/chat";
import ChatService from "../../services/chat";

const ChatList: React.FC<{handleCurrentChat: CallableFunction}> = (props) => {
  const [userChats, setUserChats] = useState<ChatUser[]>([])

  useEffect(() => {
    ChatService.fetchUserChats().then(response => setUserChats(response.data))
  }, [])
  return (
    <div className='ChatList'>
      <div className="d-flex flex-column gap-1">
        {userChats.map((UserChat) =>
          <div key={UserChat.chat.id}>
            <button
              className='btn btn-success border-0 w-25'
              onClick={() => props.handleCurrentChat(UserChat.chat)}>
              {UserChat.chat.name}
            </button>
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatList;
