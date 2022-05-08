import api from "./base";
import {Message} from "../interfaces/messages";
import {AxiosResponse} from "axios";

export default class MessagesService {
  static async fetchMessages(chatId: number): Promise<AxiosResponse<Message[]>> {
    return api.get(`/chats/${chatId}/messages/`)
  }
}
