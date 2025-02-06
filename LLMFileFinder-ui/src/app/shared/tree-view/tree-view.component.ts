import {AfterViewInit, Component, Directive, ElementRef, input, model, QueryList, ViewChildren} from '@angular/core';
import {ExpansionComponent} from '../expansion/expansion.component';
import {KeyValuePipe, NgTemplateOutlet} from '@angular/common';

@Directive({
  selector: '[jhiTreeNode]',
  standalone: true,
})
export class TreeNodeDirective {
  level = input.required<number>();

  constructor(
    public elementRef: ElementRef,
    public component: ExpansionComponent,
  ) {
  }
}

@Component({
  selector: 'jhi-tree-view',
  standalone: true,
  imports: [ExpansionComponent, KeyValuePipe, NgTemplateOutlet, TreeNodeDirective],
  templateUrl: './tree-view.component.html',
  styleUrl: './tree-view.component.scss',
})
export class TreeViewComponent implements AfterViewInit {
  @ViewChildren(TreeNodeDirective) expansions!: QueryList<TreeNodeDirective>;
  tree = model<any>();
  compact = input<boolean>(false);
  expandLevels = model<number>(0);
  activePath = model<string[]>();

  openLevels(expansions: TreeNodeDirective[]) {
    expansions.forEach(expansion => {
      const level = expansion.level();
      expansion.component.opened.set(this.expandLevels() > level);
    })
  }

  ngAfterViewInit() {
    this.openLevels(this.expansions.toArray());
    this.expansions.changes.subscribe((expansions) => this.openLevels(expansions));
  }

  getPathWithNode(path: string, node: any): string[] {
    if (path.length === 0) {
      return [node];
    }
    return [...path, node];
  }

  setActivePath(path: any, node: any): void {
    this.activePath.set(this.getPathWithNode(path, node));
  }

  isNodeActive(path: string[]) {
    return this.activePath()?.join('.').startsWith(path.join('.'));
  }

  typeOf(value: any) {
    return typeof value;
  }

}
