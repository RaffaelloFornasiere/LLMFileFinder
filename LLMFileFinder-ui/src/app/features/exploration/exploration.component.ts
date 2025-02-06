import {Component, computed, inject, OnInit, signal} from '@angular/core';
import {ExpansionComponent} from '../../shared/expansion/expansion.component';
import {TreeViewComponent} from '../../shared/tree-view/tree-view.component';
import {ActivatedRoute} from '@angular/router';
import {Service} from '../../service';
import {tap} from 'rxjs';

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
  service = inject(Service);

  appStatus = signal<any>({});
  _history = computed(() => this.appStatus()['tree']['action_history'])
  _objective = computed(() => this.appStatus()['objective'])

  ngOnInit() {
    this.activatedRoute.data.subscribe(({appStatus}) => {
      this.appStatus.set(appStatus);
    })
  }

  nextAction = signal<any>({
    "action": "open",
    "node": "jpalioapp/src/main/java/it/rf/jpalioapp/GeneratedByJHipster.java",
    "short_comment": "The 'GeneratedByJHipster.java' file could contain the game rest controller since it is a generated component and likely part of the main application logic."
  });
  errors = signal<any[]>([]);
  warnings = signal<any[]>([]);

  loading = signal(false);
  getNextAction() {
    this.loading.set(true)
    this.service.getNextAction()
      .pipe(tap(() => this.loading.set(false)))
      .subscribe((response: any) => {
      const {action, errors, warnings} = response.data
      this.nextAction.set(action)
      this.errors.set(errors)
      this.warnings.set(warnings)
    })
  }

  runAction(action: string) {
    this.service.runAction(action).subscribe((appStatus) => {
      this.appStatus.set(appStatus)
    })
  }

  treeView = computed(() => {
    const tree = (this.appStatus() as any)['tree']['tree']
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
