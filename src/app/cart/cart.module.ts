import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { CartRoutingModule } from './cart-routing.module';

import { CartService } from './services/cart.service';
import { TokenInterceptorService } from '../services/token-interceptor.service';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { ComponentCartComponent } from './component-cart/component-cart.component';

@NgModule({
  declarations: [
    ComponentCartComponent
  ],
  imports: [
    CommonModule,
    CartRoutingModule,
    HttpClientModule
  ],
  providers: [
    CartService,
    {provide: HTTP_INTERCEPTORS, useClass: TokenInterceptorService, multi: true}
  ]
})
export class CartModule { }
