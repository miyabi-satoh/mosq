import axios from "axios";
import { BaseAPI } from "./baseClass";

class AuthAPI extends BaseAPI {
  constructor() {
    super();
    this.endpoint = `/api/users/`;
  }

  async login(username: string, password: string) {
    this.endpoint = `/api-token-auth/`;
    try {
      const data = await this.create({
        username,
        password,
      });
      axios.defaults.headers.common["Authorization"] = `JWT ${data.token}`;
      return data;
    } catch (error) {
      throw error;
    }
  }
}

export const apiAuth = new AuthAPI();
