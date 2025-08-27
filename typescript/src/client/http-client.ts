import { AxiosInstance, AxiosResponse } from 'axios';

export class OtfHttpClient {
  constructor(private axios: AxiosInstance) {}

  private getJsonFromResponse(response: AxiosResponse): any {
    try {
      return response.data;
    } catch (error) {
      return { raw: response.data?.toString() || '' };
    }
  }

  async request<T>({ method, path, data, params }: {
    method: string;
    path: string;
    data?: any;
    params?: any;
  }): Promise<T> {
    const response = await this.axios.request({
      method,
      url: path,
      data,
      params
    });
    return this.getJsonFromResponse(response);
  }
}