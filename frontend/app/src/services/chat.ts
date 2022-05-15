import api from "./base";
import {AxiosResponse} from "axios";
import {Chat, ChatUser} from "../interfaces/chat";

export default class ChatService {
  static async fetchUserChats(): Promise<AxiosResponse<ChatUser[]>> {
    return api.get('chats/my/')
  }

  static async fetchChats(): Promise<AxiosResponse<Chat[]>> {
    return api.get('chats/')
  }

  static async createChat(chatName: string): Promise<AxiosResponse<Chat[]>> {
    return api.post('chats/', {name: chatName})
  }

  static async leaveChat(chatId: number): Promise<AxiosResponse<void>> {
    return api.delete(`/chats/${chatId}/users/`)
  }
}
