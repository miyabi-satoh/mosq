import { BaseAPI } from "./baseClass";

class MasterAPI extends BaseAPI {
  masterUrl: string;

  constructor() {
    super();
    this.masterUrl = `/api/master/`;
  }

  async units() {
    this.endpoint = `${this.masterUrl}units/`;
    return await this.list();
  }

  async printtypes() {
    this.endpoint = `${this.masterUrl}printtypes/`;
    return await this.list();
  }
}

export const apiMaster = new MasterAPI();
