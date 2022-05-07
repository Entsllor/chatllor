export interface Chat {
  id: number;
  name: string;
}

export interface ChatUser {
  chat: Chat
  joinedAt: Date
}
