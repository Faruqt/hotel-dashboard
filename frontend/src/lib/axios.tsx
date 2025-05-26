import axios from "axios";

const requestApi = axios.create();

requestApi.interceptors.request.use((config) => {
  config.baseURL = process.env.REACT_APP_BASE_API_URL;

  return config;
});

export default requestApi;
