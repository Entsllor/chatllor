import axios, {AxiosResponse} from "axios";

export const BASE_URL = "http://localhost:8000/"

export const api = axios.create({
  withCredentials: true,
  baseURL: BASE_URL
})


api.interceptors.request.use((config) => {
  config.headers!.Authorization = `Bearer ${localStorage.getItem('accessToken')}`;
  return config;
})

api.interceptors.response.use((config) => {
    return config;
  },
  async (error) => {
    switch (error.response.status) {
      case 401: {
        let response: AxiosResponse<{ accessToken: string }> = await axios.post(`${BASE_URL}`, null, {withCredentials: true});
        if (response.status !== 401)
          localStorage.setItem("accessToken", response.data.accessToken);
        else
          localStorage.removeItem("accessToken");
        break;
      }
    }
  })

export default api
