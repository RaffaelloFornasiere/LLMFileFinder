import {Component, inject, OnInit} from '@angular/core';
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
  examples:any[] = []

  protected activatedRoute = inject(ActivatedRoute);
  protected service = inject(Service);


  ngOnInit() {
    this.activatedRoute.data.subscribe(({examples}) => {
      this.examples = examples;
    })
  }

  save() {
    this.examples = this.examples.filter(e => e);
    this.service.saveExamples(this.examples).subscribe()
  }
}
