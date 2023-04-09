import { Component, OnInit } from '@angular/core';
import { ProductService } from '../services/product.service';
import { Product } from '../modules/product';

@Component({
  selector: 'app-list-products',
  templateUrl: './list-products.component.html',
  styleUrls: ['./list-products.component.scss']
})
export class ListProductsComponent implements OnInit {

  public listFilter: Array<Product> = [];
  public listProducs: Array<Product> = [];
  public name: string = "";

  constructor(
    private service: ProductService
  ) { }

  ngOnInit(): void {
    this.service.getCategories();
    this.service.getProducts();

    this.service.listProducts$.subscribe(restult => {
        this.listProducs = restult;
      })
  }

  public loadMoreProducts():void{
    this.service.getMoreProducts();
  }

  public search(event: Event):void {
    const element = event.target as HTMLInputElement;
    this.name = element.value;
  }

  get servicio(){
    return this.service;
  }

  public filter(event: Event):void {
    const element = event.target as HTMLSelectElement;
    this.service.filterProduct(
      element.value
      ).subscribe(result => {
      this.listFilter = result.results;
    }, error => {
      console.log(error);
    })
  }
}
