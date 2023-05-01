import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

import { ProductsRoutingModule } from './products-routing.module';
import { ListProductsComponent } from './components/list-products/list-products.component';
import { ProductComponent } from './components/product/product.component';

import { ProductService } from './services/product.service';
import { CartService } from '../cart/services/cart.service';
import { SearchPipe } from './pipes/search.pipe';
import { OfferProductsComponent } from './components/offer-products/offer-products.component';

@NgModule({
  declarations: [
    ListProductsComponent,
    ProductComponent,
    SearchPipe,
    OfferProductsComponent
  ],
  imports: [
    CommonModule,
    ProductsRoutingModule,
    HttpClientModule
  ],
  providers:[
    ProductService,
    CartService
  ]
})
export class ProductsModule { }
