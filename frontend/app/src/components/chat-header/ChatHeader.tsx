import React from "react";
import {Chat} from "../../interfaces/chat";
import ChatService from "../../services/chat";

interface ChatHeaderProps {
  chat: Chat;
  chatsUpdater: CallableFunction;
  currentChatHandler: CallableFunction;
}


const ChatHeader: React.FC<ChatHeaderProps> = (props) => {
  const leaveChat = async() => {
    await ChatService.leaveChat(props.chat.id);
    await props.chatsUpdater();
    props.currentChatHandler();
  }

  return (
    <div className='ChatHeader'>
      <div className='card fw-bold mb-3'>
        <div className='d-flex flex-row justify-content-between'>
          <div className='ps-2 align-self-center'>
            {props.chat.name}
          </div>
          <button
            className='btn btn btn-danger w-25 h-100'
            onClick={() => leaveChat()}>
            leave
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatHeader;
