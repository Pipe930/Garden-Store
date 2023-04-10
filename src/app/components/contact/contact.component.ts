import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.scss']
})
export class ContactComponent implements OnInit {
  public formularioContacto: FormGroup | any;

  constructor(
    private builder: FormBuilder
  ) {
    this.formularioContacto = this.builder.group({
      correo: new FormControl("", [Validators.required, Validators.email]),
      mensaje: new FormControl("", [Validators.minLength(10), Validators.maxLength(255)])
    });
  }

  public enviarContacto():void{

    const formulario = this.formularioContacto.value;

    const contacto = {
      "correo": formulario.correo,
      "mensaje": formulario.mensaje
    }

    if(this.formularioContacto.invalid){
      this.formularioContacto.markAllAsTouched();
    } else {
      console.log("enviado");
      console.log(contacto);
    }
  }

  get correo(){
    return this.formularioContacto.get('correo');
  }

  get mensaje(){
    return this.formularioContacto.get('mensaje');
  }

  ngOnInit(): void {

  }
}
