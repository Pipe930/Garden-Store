import { ComponentFixture, TestBed } from '@angular/core/testing';

import { OfferProductsComponent } from './offer-products.component';

describe('OfferProductsComponent', () => {
  let component: OfferProductsComponent;
  let fixture: ComponentFixture<OfferProductsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ OfferProductsComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(OfferProductsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
