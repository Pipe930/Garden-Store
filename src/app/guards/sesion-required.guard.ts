import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class SesionRequiredGuard implements CanActivate {
  constructor(
    private ruta: Router
    ) {}

  canActivate() {
    if(sessionStorage.getItem('token')!=null){
      return true;
    } else {
      this.ruta.navigate(['login']);
      return false;
    }
  }

}
