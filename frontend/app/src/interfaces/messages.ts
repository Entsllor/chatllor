export interface Message {
  id: number
  userId: number;
  body: string;
  createdAt: Date;
  user: {
    username: string;
    id: number
  };
}
