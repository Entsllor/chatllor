import React, {useEffect, useState} from "react";
import {Chat} from "../../interfaces/chat";
import ChatService from "../../services/chat";

const ChatSearch: React.FC<{}> = (props) => {
  const [chats, setChats] = useState<Chat[]>([])
  const [nameFilter, setNameFilter] = useState<string>('')
  const [filteredChats, setFilteredChats] = useState<Chat[]>([])

  useEffect(() => {
    ChatService.fetchChats().then(response => {
      setChats(response.data)
    });
  }, [])

  useEffect(() => {
    let newFilteredChats = chats;
    newFilteredChats = newFilteredChats.filter(
      (chat) => chat.name.toLowerCase().includes(nameFilter.toLowerCase())
    )
    setFilteredChats(newFilteredChats)
  }, [nameFilter]);

  return (
    <div className='ChatSearch'>
      <input type='text'
             value={nameFilter}
             onChange={event => setNameFilter(event.target.value)}
             placeholder='Search by name'
             className='form-control mb-3'/>

      {filteredChats.map((chat) => (
        <div key={chat.id} className="card card-header mb-3">
          {chat.name}
        </div>
      ))}
    </div>
  );
};

export default ChatSearch;
