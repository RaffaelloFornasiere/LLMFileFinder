import {Component, computed, inject, OnInit, signal} from '@angular/core';
import {ActivatedRoute} from '@angular/router';
import {FormsModule} from '@angular/forms';
import {Service} from '../../service';

@Component({
  selector: 'app-few-shot-examples',
  imports: [
    FormsModule
  ],
  templateUrl: './few-shot-examples.component.html',
  styleUrl: './few-shot-examples.component.scss'
})
export class FewShotExamplesComponent implements OnInit {
  _examples = signal<any[]>([]);

  get examples() {
    return this._examples();
  }

  set examples(value) {
    this._examples.set(value);
  }

  readonly WORD_TOKEN_CONV = 3.0/4.0;
  tokenCount = signal(0);


  protected activatedRoute = inject(ActivatedRoute);
  protected service = inject(Service);


  ngOnInit() {
    this.activatedRoute.data.subscribe(({examples}) => {
      this.examples = examples;
    })
    this.service.getTokenCount(this.examples.join('\n---\n\n')).subscribe((response: any) => {
      this.tokenCount.set(response.data)
    })
  }

  save() {
    this.examples = this.examples.filter(e => e);
    this.service.saveExamples(this.examples).subscribe()
  }
}
