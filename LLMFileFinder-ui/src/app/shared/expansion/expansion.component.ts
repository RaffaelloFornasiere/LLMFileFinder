import { Component, model } from '@angular/core';
import 'material-icons/iconfont/material-icons.css';

@Component({
  selector: 'jhi-expansion',
  standalone: true,
  templateUrl: './expansion.component.html',
  styleUrl: './expansion.component.scss',
})
export class ExpansionComponent {
  opened = model<boolean>(false);

  toggle(): void {
    this.opened.set(!this.opened());
  }
}
