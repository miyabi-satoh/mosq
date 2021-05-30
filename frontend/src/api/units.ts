import { BaseAPI } from "./baseClass";

class UnitsAPI extends BaseAPI {
  constructor() {
    super();
    this.endpoint = `/api/units/`;
  }
}

export const apiUnits = new UnitsAPI();
