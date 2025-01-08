import {Component, computed, inject, OnInit, signal} from '@angular/core';
import {Service} from './service';
import {FormsModule} from '@angular/forms';
import {TabNameDirective, TabsComponent} from './shared/tabs/tabs.component';
import {ActivatedRoute, NavigationEnd, Router, RouterOutlet} from '@angular/router';
import {filter} from 'rxjs';

@Component({
  selector: 'app-root',
  imports: [
    FormsModule,
    TabsComponent,
    TabNameDirective,
    RouterOutlet
  ],
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss'
})
export class AppComponent implements OnInit {
  title = 'LLMFileFinder-ui';
  service = inject(Service);
  tabs = [
    {
      name: "Exploration",
      route: "exploration"
    },
    {
      name: "Prompt Settings",
      route: "prompt-settings"
    },

    {
      name: "Few Shot Examples",
      route: "few-shot-examples"
    }
  ]
  activeTab = signal(this.tabs[0].name);

  router = inject(Router)
  activatedRoute = inject(ActivatedRoute)

  routeTab(tabName: any) {
    const route = this.tabs.find(tab => tab.name === tabName)!.route
    this.router.navigate([route]).then()
  }

  appStatus = signal<any>({})
  models = signal([])

  subActions = [
    {
      name: "Open File",
      system_message: "Open a file",
      user_template_message: "Open a file",
    }
  ]

  ngOnInit() {
    this.service.getAppStatus().subscribe(({data: data}: any) => {
      this.appStatus.set(data);
    })
    this.service.getModels().subscribe(({data: data}: any) => {
      this.models.set(data);
    })

    this.router.events.pipe(filter(e => e instanceof NavigationEnd)).subscribe((event) => {
      this.activeTab.set(this.tabs.find(tab => tab.route === event.url.split('/')[1])?.name ?? this.tabs[0].name)
    })
  }


  get systemMessage() {
    return this._systemMessage()
  }

  set systemMessage(value: string) {
    this.appStatus.set({
      ...this.appStatus(),
      system_message: value
    })
  }

  get objective() {
    return this._objective()
  }

  set objective(value: string) {
    this.appStatus.set({
      ...this.appStatus(),
      objective: value
    })
  }

  get userTemplateMessage() {
    return this._userTemplateMessage()
  }

  set userTemplateMessage(value: string) {
    this.appStatus.set({
      ...this.appStatus(),
      user_template_message: value
    })
  }

  history = computed(() => (this.appStatus() as any)['history'])
  _systemMessage = computed(() => (this.appStatus() as any)['system_message'])
  _userTemplateMessage = computed(() => (this.appStatus() as any)['user_template_message'])
  _objective = computed(() => (this.appStatus() as any)['objective'])

}
