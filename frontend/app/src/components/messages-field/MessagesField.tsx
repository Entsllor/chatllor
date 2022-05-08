import React, {useEffect, useState} from "react";
import {Message} from "../../interfaces/messages";
import MessagesService from "../../services/messages";

const MessagesField: React.FC<{ chatId: number }> = (props) => {
  const [messages, setMessages] = useState<Message[]>([])

  useEffect(() => {
    MessagesService.fetchMessages(props.chatId).then(response => setMessages(response.data));
  }, [props.chatId])

  return (
    <div className='MessagesField'>
      <div className='d-flex flex-column gap-2'>
        {messages.map((message) => (
          <div key={message.id} className="bg-secondary">
            <div className='col col-4 d-flex'>{message.userId}</div>
            <div className='col col-8'>{message.body}</div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default MessagesField;
