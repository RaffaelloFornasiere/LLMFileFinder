import {inject, Injectable} from '@angular/core';
import {HttpClient} from '@angular/common/http';


@Injectable({
  providedIn: 'root'
})
export class Service {
  baseUrl = "http://localhost:8080"
  http = inject(HttpClient)

  getAppStatus() {
    return this.http.get(`${this.baseUrl}/app_status`, { observe: 'response' })
  }

  setPath(path: string) {
    return this.http.post(`${this.baseUrl}/path`, {path: path})
  }

  newTree() {
    return this.http.get(`${this.baseUrl}/new_tree`)
  }

  getModels() {
    return this.http.get(`${this.baseUrl}/models`, { observe: 'response' })
  }

  saveAppStatus(appStatus: any) {
    return this.http.post(`${this.baseUrl}/app_status`, appStatus)
  }

  saveAppStatusProperty(property: string, value: any, appStatus: any) {
    appStatus[property] = value
    return this.saveAppStatus(appStatus).subscribe()
  }

  getExamples() {
    return this.http.get(`${this.baseUrl}/examples`, { observe: 'response' })
  }

  saveExamples(examples: any) {
    return this.http.post(`${this.baseUrl}/examples`, examples)
  }
}
