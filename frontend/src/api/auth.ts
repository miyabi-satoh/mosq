// import axios from "axios";
import { BaseAPI } from "./baseClass";

class AuthAPI extends BaseAPI {
  constructor() {
    super();
    this.endpoint = `/api/users/`;
  }

  async login(username: string, password: string) {
    try {
      // CSRF トークンを更新
      this.endpoint = `/api/csrf-cookie/`;
      await this.list();

      this.endpoint = `/api/login/`;
      const data = await this.create({
        username,
        password,
      });
      // axios.defaults.headers.common["Authorization"] = `JWT ${data.token}`;
      return data;
    } catch (error) {
      throw error;
    }
  }

  async logout() {
    try {
      this.endpoint = `/api/logout/`;
      return await this.list();
    } catch (error) {
      throw error;
    }
  }

  async me() {
    try {
      // CSRF トークンを更新
      this.endpoint = `/api/csrf-cookie/`;
      await this.list();

      this.endpoint = `/api/users/me/`;
      return await this.list();
    } catch (error) {
      throw error;
    }
  }
}

export const apiAuth = new AuthAPI();
