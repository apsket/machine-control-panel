import axios from "axios";

const client = axios.create({
  baseURL: "http://127.0.0.1:8000", // backend FastAPI URL
});

export default client;