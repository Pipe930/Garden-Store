import { Component, OnInit } from '@angular/core';
import { Product } from '../../modules/product';
import { ProductService } from '../../services/product.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-product',
  templateUrl: './product.component.html',
  styleUrls: ['./product.component.scss']
})
export class ProductComponent implements OnInit {

  public productSlug: string = '';
  public product: Product | any;
  public dominio: string = 'http://127.0.0.1:8000';
  public quality: number = 1;
  public stockPorduct: number = 0;
  public idProduct: number = 0;

  constructor(
    private servicio: ProductService,
    private ruta: ActivatedRoute,
    // private cart: CartService,
    // private rout: Router
  ) {
    this.ruta.params.subscribe(resultado => {
      this.productSlug = resultado['slug'];
    }, error => {
      console.log(error);
    });

    this.servicio.getProduct(this.productSlug).subscribe(resultado => {
      this.product = resultado;
      this.stockPorduct = resultado.stock;
      this.idProduct = resultado.id;
    }, error => {
      console.log(error);
    });
  }

  ngOnInit(): void {

  }

  public sum():void{
    if(this.stockPorduct > this.quality){
      this.quality = this.quality + 1;
    }
  }

  public substract():void{
    if(this.quality > 1){
      this.quality = this.quality - 1;
    }
  }

  // public addCart():void{
  //   const user = JSON.parse(sessionStorage.getItem('user')!);

  //   if(user){

  //     const product = {
  //       product: this.idProduct,
  //       quantity: this.quality,
  //       idCart: user.idCart,
  //       price: this.product.price
  //     }

  //     this.cart.cartAdd(product);
  //   } else {
  //     Swal.fire({
  //       title: "Debes inicar Sesion",
  //       text: "Para poder agregar productos a tu carrito inicia sesion",
  //       icon: "info"
  //     })
  //     this.rout.navigate(['auth/login']);
  //   }

  // }
}
