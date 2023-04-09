import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClientModule } from '@angular/common/http';

import { ProductsRoutingModule } from './products-routing.module';
import { ListProductsComponent } from './list-products/list-products.component';
import { ProductComponent } from './product/product.component';

import { ProductService } from './services/product.service';
import { FilterPipe } from './pipes/filter.pipe';

@NgModule({
  declarations: [
    ListProductsComponent,
    ProductComponent,
    FilterPipe
  ],
  imports: [
    CommonModule,
    ProductsRoutingModule,
    HttpClientModule
  ],
  providers:[
    ProductService
  ]
})
export class ProductsModule { }
