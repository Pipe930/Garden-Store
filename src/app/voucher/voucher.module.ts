import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

import { VoucherRoutingModule } from './voucher-routing.module';
import { VoucherComponentComponent } from './voucher-component/voucher-component.component';


@NgModule({
  declarations: [
    VoucherComponentComponent
  ],
  imports: [
    CommonModule,
    VoucherRoutingModule
  ]
})
export class VoucherModule { }
