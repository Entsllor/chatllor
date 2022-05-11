import React from "react";
import {ChatUser} from "../../interfaces/chat";

const ChatList: React.FC<{ handleCurrentChat: CallableFunction, userChats: ChatUser[] }> = (props) => {

  return (
    <div className='ChatList'>
      <div className="d-flex flex-column gap-1">
        {props.userChats.map((UserChat) =>
          <div key={UserChat.chat.id}>
            <button
              className='btn btn-success border-0 w-100'
              onClick={() => props.handleCurrentChat(UserChat.chat)}>
              {UserChat.chat.name}
            </button>
          </div>
        )}
        <button className='btn btn-secondary border-0 w-100'
                onClick={() => props.handleCurrentChat()}>
          +
        </button>
      </div>
    </div>
  )
}

export default ChatList;
