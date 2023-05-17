import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import { map, first } from 'rxjs';
import { Login, LoginResponse, ResetPassword } from '../modules/login';
import { Register, RegisterResponse } from '../modules/register';
import Swal from 'sweetalert2';

@Injectable({
  providedIn: 'root'
})
export class AuthenticationService {
  private urlApi: string = "http://127.0.0.1:8000/users/";

  constructor(
    private http: HttpClient,
    private route: Router
  ) { }

  public login(formulario: Login):void{
    this.http.post<LoginResponse>(`${this.urlApi}auth/login`, formulario, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }).pipe(
      map(user => {
        if(user && user.token){
          sessionStorage.setItem('token', user.token);
          sessionStorage.setItem('user', JSON.stringify(user));
        }
        return user;
      })
    ).pipe(first()).subscribe(result => {
      if(result){
        Swal.fire({
          icon: "success",
          title: `Bienvenido ${result.username}`,
          text: "Bienvenido a Garden Store"
        });
        this.route.navigate(['home']);
      }
    }, error => {
      console.log(error);
      Swal.fire({
        icon: "error",
        title: "Error de Inicio Sesion",
        text: "La conexion del servidor no a sido exitosa"
      });
    }
    );
  }

  public register(formulario: Register):void{
    this.http.post<RegisterResponse>(`${this.urlApi}register`, formulario, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }).subscribe(result => {
        if(result){
          Swal.fire({
            icon: "success",
            title: "Te registraste correctamente",
            text: "El registro fue un exito"
          });
          this.route.navigate(['auth/login']);
        }
      }, error => {
        console.log(error);
        Swal.fire({
          icon: "error",
          title: "Error al Registrarse",
          text: "La conexion del servidor no a sido exitosa"
        });
      }

    );
  }

  public logout(token: string):void{
    this.http.get<any>(`${this.urlApi}auth/logout?token=${token}`, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',
        "Authorization": 'Token ' + sessionStorage.getItem('token')!
      })
    }).subscribe(result => {
      if(result){
        sessionStorage.clear();
        this.route.navigate(['home']);
      }
    }, error => {
      console.log(error);
    });
  }

  public resetPassword(formulario: ResetPassword): void{
    this.http.post<any>(`${this.urlApi}password-reset/`, formulario, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json',

      }),
      withCredentials:true
    }).subscribe(result => {
      if(result){
        Swal.fire({
          title: "Envio Exitoso",
          icon: "success",
          text: "Se envio un correo para reestablezer tu contraseña"
        });
        this.route.navigate(['auth/login']);
      }
  }, error => {
    console.log(error);
  });
  }
}
