import {Component, inject, OnInit, signal} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {Service} from '../../service';

@Component({
  selector: 'app-prompt-settings',
  imports: [
    FormsModule
  ],
  templateUrl: './prompt-settings.component.html',
  styleUrl: './prompt-settings.component.scss'
})
export class PromptSettingsComponent implements OnInit {
  models = signal<any[]>([]);
  appStatus = signal<any>({});

  protected activatedRoute = inject(ActivatedRoute);
  protected service = inject(Service);

  ngOnInit() {
    this.activatedRoute.data.subscribe(({models, appStatus}) => {
      this.models.set(models);
      this.appStatus.set(appStatus);
    })
  }

  set systemMessage(message: string) {
    this.appStatus.set({...this.appStatus(), system_message: message})
  }

  get systemMessage() {
    return this.appStatus().system_message
  }

  set userTemplateMessage(message: string) {
    this.appStatus.set({...this.appStatus(), user_template_message: message})
  }

  get userTemplateMessage() {
    return this.appStatus().user_template_message
  }


}
