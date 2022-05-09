import api from "./base";
import {AxiosResponse} from "axios";
import {ChatUser} from "../interfaces/chat";

export default class ChatService {
  static async fetchUserChats(): Promise<AxiosResponse<ChatUser[]>> {
    return api.get('chats/my/')
  }

  static async leaveChat(chatId: number): Promise<AxiosResponse<void>> {
    return api.delete(`/chats/${chatId}/users/`)
  }
}
