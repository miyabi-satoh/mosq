import { BaseAPI } from "./baseClass";

class PrintsAPI extends BaseAPI {
  constructor() {
    super();
    this.endpoint = `/api/prints/`;
  }
}

export const apiPrints = new PrintsAPI();
