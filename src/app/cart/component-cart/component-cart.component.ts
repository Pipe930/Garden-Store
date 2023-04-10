import { Component, OnInit } from '@angular/core';
import { CartService } from '../services/cart.service';
import { Cart } from '../modules/cart';

@Component({
  selector: 'app-component-cart',
  templateUrl: './component-cart.component.html',
  styleUrls: ['./component-cart.component.scss']
})
export class ComponentCartComponent implements OnInit {

  public items: Array<any> = [];
  public cart: Cart =  {
    id: 0,
    idUser: 0,
    items: [],
    total: 0
  };

  public user = JSON.parse(sessionStorage.getItem('user')!);

  constructor(
    private service: CartService
  ) { }

  ngOnInit(): void {
    this.service.getCart(
      this.user.user_id
      ).pipe(result => result).subscribe(result => {
        this.items = result.items;

        this.cart = result;
      }, error => {
        console.log(error);
      });
  }

  public substractProduct(productid: number):void{

    const json = {
      product: productid,
      idCart: this.cart.id

    }

    this.service.cartSubstract(json);

    window.location.reload();

  }

  public sumProduct(productid: number):void {
    const json = {
      product: productid,
      quantity: 1,
      idCart: this.cart.id
    }

    this.service.cartSum(json);

    window.location.reload();

  }

}
