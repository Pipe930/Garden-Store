import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CartRoutingModule } from './cart-routing.module';

import { CartService } from './services/cart.service';

@NgModule({
  declarations: [],
  imports: [
    CommonModule,
    CartRoutingModule
  ],
  providers: [
    CartService
  ]
})
export class CartModule { }
