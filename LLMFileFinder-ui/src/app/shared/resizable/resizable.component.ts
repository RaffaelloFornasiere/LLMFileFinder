import {Component, ElementRef, input, signal, ViewChild} from '@angular/core';

@Component({
  selector: 'app-resizable',
  imports: [],
  templateUrl: './resizable.component.html',
  styleUrl: './resizable.component.scss'
})
export class ResizableComponent {
  @ViewChild('container') container: ElementRef<HTMLDivElement> | undefined
  defaultOneDim = input(50)
  oneDim = signal(this.defaultOneDim())
  dragging = signal(false)

  dragStart() {
    this.dragging.set(true)
  }

  drag(event: any) {
    if (this.dragging()) {
      const draggedWidth =   event.clientX - this.container!.nativeElement.getBoundingClientRect().left
      const blockWith = this.container!.nativeElement.offsetWidth
      this.oneDim.set(Number((draggedWidth / blockWith * 100).toFixed(2)))
    }
  }

  dragEnd() {
    this.dragging.set(false)
  }




}
