
const agregarInputEnvio = () => {
    const idElemento = document.getElementById('field-modificable');
    idElemento.innerHTML = [` 
    <label for="" class="label-form-comprar2">Direccion: </label>
    <input type="text" required name="direccion" id="direccion" class="input-form-comprar">
    `];
}
function eventoCheckBoxEnvio(){
    const idRadio = document.getElementById('envio');
    idRadio.addEventListener('click', agregarInputEnvio());
}

const agregarInputRetiro = () => {
    const idElemento = document.getElementById('field-modificable');
    idElemento.innerHTML = [` 
    <label for="" class="label-form-comprar2">Tienda: </label>
    <select name="direccion" id="direccion" class="select-form-comprar">
        <option selected value="La Cisterna 4567">La Cisterna 4567</option>
        <option value="San Bernardo 3748">San Bernardo 3748</option>
        <option value="Estacion Central 2144">Estacion Central 2144</option>
        <option value="Puente Alto 3849">Puente Alto 3849</option>
        <option value="Maipu 4758">Maipu 4758</option>
    </select>
    `];
}

function eventoCheckBoxRetiro(){
    const idRadio = document.getElementById('retirar');
    idRadio.addEventListener('click', agregarInputRetiro());
}
