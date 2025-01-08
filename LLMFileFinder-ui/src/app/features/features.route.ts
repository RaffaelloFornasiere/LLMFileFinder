import {Routes} from '@angular/router';
import modelsResolver from '../shared/resolvers/models-resolver.service';
import appStatusResolver from '../shared/resolvers/appStatus-resolver.service';
import fewShotExamplesResolver from './few-shot-examples/fewShotExamples-resolver.service';

export const routes: Routes = [
  {
    path: '',
    redirectTo: 'prompt-settings',
    pathMatch: 'full'
  },
  {
    path: 'prompt-settings',
    resolve: {
      models: modelsResolver,
      appStatus: appStatusResolver
    },
    loadComponent: () => import('./prompt-settings/prompt-settings.component').then(m => m.PromptSettingsComponent)
  },
  {
    path: 'exploration',
    resolve: {
      appStatus: appStatusResolver
    },
    loadComponent: () => import('./exploration/exploration.component').then(m => m.ExplorationComponent)
  },
  {
    path: 'few-shot-examples',
    resolve: {
      examples: fewShotExamplesResolver,
    },
    loadComponent: () => import('./few-shot-examples/few-shot-examples.component').then(m => m.FewShotExamplesComponent)
  }
]

