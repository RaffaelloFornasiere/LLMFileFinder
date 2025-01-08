import {mergeMap, Observable, of} from 'rxjs';
import {inject} from '@angular/core';
import {HttpResponse} from '@angular/common/http';

import {ActivatedRouteSnapshot} from '@angular/router';
import {Service} from '../../service';

export const modelsResolver =
  (): Observable<null | any[]> => {
    const service = inject(Service)

    return service.getModels().pipe(
      mergeMap((u: HttpResponse<any>) => {
        if (u.body) {
          return of(u.body.data ?? []);
        }
        return of(null);
      }),
    );
  };
export default modelsResolver;
