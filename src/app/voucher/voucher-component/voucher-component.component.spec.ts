import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VoucherComponentComponent } from './voucher-component.component';

describe('VoucherComponentComponent', () => {
  let component: VoucherComponentComponent;
  let fixture: ComponentFixture<VoucherComponentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ VoucherComponentComponent ]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VoucherComponentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
