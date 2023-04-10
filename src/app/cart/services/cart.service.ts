import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Router } from '@angular/router';
import Swal from 'sweetalert2';
import { Cart } from '../modules/cart';
import { AddCart } from '../modules/add-cart';

@Injectable({
  providedIn: 'root'
})
export class CartService {
  public urlCart: string = 'http://127.0.0.1:8000/carts/';
  public cart: Cart | any;

  constructor(
    private http: HttpClient,
    private rout: Router
  ) { }

  public cartAdd(product: AddCart):void{
    this.http.post<Cart>(`${this.urlCart}item/add`, product, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }).subscribe(result => {
      if(result){
        Swal.fire({
          title: "Se agrego con exito el producto la carrito",
          icon: "success"
        });
        this.rout.navigate(['cart']);
      }
    }, error => {
      Swal.fire({
        title: "Ocurrio un error no se agrego el producto al carrito",
        icon: "error"
      });
      console.log(error);
    });
  }

  public getCart(id: number):void{
    this.http.get<Cart>(`${this.urlCart}cart/user/${id}`, {
      headers: new HttpHeaders({
        'Content-Type': 'application/json'
      })
    }).subscribe(result => {
      if(result){
        this.cart = result;
      }
    }, error => {
      console.log(error);
    })
  }
}
