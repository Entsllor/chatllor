import api from "./base";
import {AxiosResponse} from "axios";
import {AuthResponse, UserPrivate} from "../interfaces/auth";

export default class AuthService {
  static async login(username: string, password: string): Promise<AxiosResponse<AuthResponse>> {
    return api.post(
      '/auth/login',
      `username=${username}&password=${password}`,
      {headers: {"Content-Type": "application/x-www-form-urlencoded"}}
    ).then(response => {
      localStorage.setItem("accessToken", response.data.accessToken);
      return response
    })
  }

  static async registration(username: string, email: string, password: string): Promise<AxiosResponse<UserPrivate>> {
    return api.post("users/", {username: username, password: password, email: email})
  }

  static async revoke(): Promise<AxiosResponse<AuthResponse>> {
    return api.post("auth/revoke").then(response => {
      localStorage.setItem("accessToken", response.data.accessToken);
      return response
    })
  }

  static async logout(): Promise<AxiosResponse<void>> {
    localStorage.removeItem('accessToken')
    return api.post("/auth/logout")
  }
}
