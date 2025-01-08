import {Component, ContentChildren, Directive, input, model, TemplateRef} from '@angular/core';
import {NgTemplateOutlet} from "@angular/common";



@Directive({
  standalone: true,
  selector: '[jhiTab]'
})
export class TabNameDirective {
  jhiTab = input.required<string>();
  constructor(public template: TemplateRef<any>) {
  }
}

@Component({
  selector: 'jhi-tabs',
  standalone: true,
  imports: [
    NgTemplateOutlet
  ],
  templateUrl: './tabs.component.html',
  styleUrl: './tabs.component.scss'
})
export class TabsComponent {
  @ContentChildren(TabNameDirective) tabs: any;

  activeTab = model<string>()
  selectTab(tab: string): void {
    this.activeTab.set(tab);
  }
}
