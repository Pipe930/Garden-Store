import { Pipe, PipeTransform } from '@angular/core';
import { Product } from '../modules/product';
import { ProductService } from '../services/product.service';

@Pipe({
  name: 'filter'
})
export class FilterPipe implements PipeTransform {

  constructor(
    private servicio: ProductService
  ) {}

  transform(products: Array<Product>, name: string): Array<Product> {
    this.servicio.searchProduct(name);

    if(this.servicio.listSearch.length){
      return this.servicio.listSearch;
    } else if (name == "") {
      return products;
    } else {
      return products;
    }
  }

}
