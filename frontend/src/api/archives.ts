import { BaseAPI } from "./baseClass";

class ArchivesAPI extends BaseAPI {
  constructor() {
    super();
    this.endpoint = `/api/archives/`;
  }
}

export const apiArchives = new ArchivesAPI();
