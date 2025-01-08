import {Component, computed, inject, OnInit, signal} from '@angular/core';
import {ExpansionComponent} from '../../shared/expansion/expansion.component';
import {TreeViewComponent} from '../../shared/tree-view/tree-view.component';
import {ActivatedRoute} from '@angular/router';

@Component({
  selector: 'app-exploration',
  imports: [
    ExpansionComponent,
    TreeViewComponent
  ],
  templateUrl: './exploration.component.html',
  styleUrl: './exploration.component.scss'
})
export class ExplorationComponent implements OnInit {

  activatedRoute = inject(ActivatedRoute);

  appStatus = signal<any>({});
  _history = computed(() => this.appStatus()['history'])
  _objective = computed(() => this.appStatus()['objective'])

  ngOnInit() {
    this.activatedRoute.data.subscribe(({ appStatus }) => {
      this.appStatus.set(appStatus);
    })
  }

  treeView = computed(() => {
    const tree = (this.appStatus() as any)['tree']
    if (!tree) return {}
    const rootName = tree.name
    const convertTree = (tree: any) => {
      delete tree.name
      const children = tree.children
      delete tree.children

      if (children) {
        tree.children = {} as any
        for (const child of children) {
          tree.children[child.name] = convertTree(child)
        }
      }
      return tree
    }
    return {
      [rootName]: convertTree(tree)
    }

  })
}
