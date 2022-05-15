import React, {FormEvent, useState} from "react";
import ChatService from "../../services/chat";

interface ChatCreationFormProps {
  updateChats: CallableFunction
}

const ChatCreationForm: React.FC<ChatCreationFormProps> = (props) => {
  const [chatName, setChatName] = useState<string>("")

  async function createChat(event: FormEvent) {
    event.preventDefault()
    await ChatService.createChat(chatName)
    await props.updateChats()
  }
  
  return (
    <div className='ChatCreationForm mb-3'>
      <form onSubmit={event => createChat(event)}>
        <div className="row row-cols-2">
          <div className="col col-8">
            <input
              className="form-control"
              type="text"
              value={chatName}
              placeholder="Chat name"
              onChange={event => setChatName(event.target.value)}
            />
          </div>
          <div className="col col-4">
            <button
              className="btn btn-success w-100"
              type={"submit"}
            >
              Create
            </button>
          </div>
        </div>
      </form>
    </div>
  )
};

export default ChatCreationForm;
