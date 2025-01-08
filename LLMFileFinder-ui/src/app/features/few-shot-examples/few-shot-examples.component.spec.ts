import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FewShotExamplesComponent } from './few-shot-examples.component';

describe('FewShotExamplesComponent', () => {
  let component: FewShotExamplesComponent;
  let fixture: ComponentFixture<FewShotExamplesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [FewShotExamplesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(FewShotExamplesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
