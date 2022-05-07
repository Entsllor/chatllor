import api from "./base";
import {AxiosResponse} from "axios";
import {Chat, ChatUser} from "../interfaces/chat";

export default class ChatService {
  static async fetchUserChats(): Promise<AxiosResponse<ChatUser[]>> {
    return api.get('chats/my/')
  }
}
