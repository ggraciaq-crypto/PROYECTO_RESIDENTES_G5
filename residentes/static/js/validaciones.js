document.addEventListener("DOMContentLoaded", function () {

    // VALIDAR TELÉFONO
    document.querySelectorAll(".validar-telefono").forEach(function (input) {

        input.addEventListener("input", function () {

            const mensaje = input.parentElement.querySelector(".mensaje-validacion");
            const telefono = input.value.trim();

            input.classList.remove("input-error", "input-success");
            mensaje.innerHTML = "";

            if (telefono === "") {
                return;
            }

            if (/^09\d{8}$/.test(telefono)) {
                input.classList.add("input-success");
            } else {
                input.classList.add("input-error");

                mensaje.innerHTML = `
                    <div class="error-text">
                        <i class="bi bi-x-circle-fill"></i>
                        El teléfono debe tener 10 dígitos y comenzar con 09.
                    </div>
                `;
            }

        });

    });


    // VALIDAR CÉDULA
    document.querySelectorAll(".validar-cedula").forEach(function (input) {

        input.addEventListener("input", function () {

            const mensaje = input.parentElement.querySelector(".mensaje-validacion");
            const cedula = input.value.trim();

            input.classList.remove("input-error", "input-success");
            mensaje.innerHTML = "";

            if (cedula === "") {
                return;
            }

            if (/^\d{10}$/.test(cedula)) {
                input.classList.add("input-success");
            } else {
                input.classList.add("input-error");

                mensaje.innerHTML = `
                    <div class="error-text">
                        <i class="bi bi-x-circle-fill"></i>
                        La cédula debe contener exactamente 10 dígitos.
                    </div>
                `;
            }

        });

    });


    // VALIDAR PLACA
    document.querySelectorAll(".validar-placa").forEach(function (input) {

        input.addEventListener("input", function () {

            const mensaje = input.parentElement.querySelector(".mensaje-validacion");
            let placa = input.value.toUpperCase().trim();

            input.value = placa;

            input.classList.remove("input-error", "input-success");
            mensaje.innerHTML = "";

            if (placa === "") {
                return;
            }

            if (/^[A-Z]{3}-\d{4}$/.test(placa)) {
                input.classList.add("input-success");
            } else {
                input.classList.add("input-error");

                mensaje.innerHTML = `
                    <div class="error-text">
                        <i class="bi bi-x-circle-fill"></i>
                        La placa debe tener el formato ABC-1234.
                    </div>
                `;
            }

        });

    });

});