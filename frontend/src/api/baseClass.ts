import axios from "axios";

function clg(error: any) {
  console.log(error);
  if (error.response) {
    const { status, statusText } = error.response;
    console.log(`Error ${status} : ${statusText}`);
  }
}

export class BaseAPI {
  endpoint: string;

  constructor() {
    this.endpoint = "";
  }

  async list() {
    const url = `${this.endpoint}`;
    try {
      const resp = await axios.get(url);
      return resp.data;
    } catch (error) {
      clg(error);
      throw error;
    }
  }

  async get(pk: number) {
    const url = `${this.endpoint}${pk}`;
    try {
      const resp = await axios.get(url);
      return resp.data;
    } catch (error) {
      clg(error);
      throw error;
    }
  }

  async create(params: any) {
    const url = `${this.endpoint}`;
    try {
      const resp = await axios.post(url, params);
      return resp.data;
    } catch (error) {
      clg(error);
      throw error;
    }
  }
}
