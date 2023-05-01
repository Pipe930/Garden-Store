import { Component, OnInit } from '@angular/core';
import { ProductService } from '../../services/product.service';

@Component({
  selector: 'app-offer-products',
  templateUrl: './offer-products.component.html',
  styleUrls: ['./offer-products.component.scss']
})
export class OfferProductsComponent implements OnInit {

  constructor(private service: ProductService) { }

  ngOnInit(): void {
    this.service.getProductsOffer();
  }

  get servicio(){
    return this.service;
  }
}
