
document.addEventListener("DOMContentLoaded", function () {

  const btnMostrar = document.getElementById("btnMostrarFormulario");
  const modal = $("#modalEvento");

  const inputNombre = document.getElementById("nombreEvento");
  const inputFecha = document.getElementById("fechaEvento");
  const inputHora = document.getElementById("horaEvento");
  const inputDesc = document.getElementById("descripcionEvento");

  const tablaBody = document.querySelector("table tbody");

  // Mostrar modal
  btnMostrar.addEventListener("click", function () {
    modal.modal("show");
  });

  // Guardar evento en tabla
  document.getElementById("formCrearEvento").addEventListener("submit", function (e) {
    e.preventDefault(); // Evita que se recargue

    // Crear fila nueva
    let fila = `
          <tr>
            <td>${inputNombre.value}</td>
            <td>—</td>
            <td><span class="badge badge-success">Nuevo</span></td>
            <td>—</td>
            <td>
              <div class="d-flex align-items-center">
                <span class="mr-2">0%</span>
                <div class="progress">
                  <div class="progress-bar bg-info" style="width: 0%;"></div>
                </div>
              </div>
            </td>
            <td>
              <a href="#" class="btn btn-info btn-sm"><i class="fas fa-edit"></i></a>
              <button class="btn btn-danger btn-sm"><i class="fas fa-trash"></i></button>
            </td>
          </tr>
        `;

    // Insertar fila
    tablaBody.insertAdjacentHTML("beforeend", fila);

    // Cerrar modal
    modal.modal("hide");

    // Limpiar campos
    inputNombre.value = "";
    inputFecha.value = "";
    inputHora.value = "";
    inputDesc.value = "";
  });

});


function previewImage(event, previewId) {
  const input = event.target;
  const preview = document.getElementById(previewId);
  if (!input.files || !input.files[0]) {
    if (preview) preview.style.display = 'none';
    return;
  }
  const reader = new FileReader();
  reader.onload = function (e) {
    if (preview) {
      preview.src = e.target.result;
      preview.style.display = 'block';
    }
  }
  reader.readAsDataURL(input.files[0]);
}

function previewImage(event, id) {
  const img = document.getElementById(id);
  img.src = URL.createObjectURL(event.target.files[0]);
  img.style.display = "block";
}

function previewImage(event, id) {
  const file = event.target.files[0];
  if (!file) {
    console.log("No se seleccionó archivo");
    return;
  }

  const img = document.getElementById(id);
  img.src = URL.createObjectURL(file);
  img.style.display = "block";

  console.log("Vista previa cargada:", img.src);
}

// Desplazamiento suave para enlaces internos
document.querySelectorAll('a[href^="#"]').forEach(link => {
  link.addEventListener('click', function (e) {
    e.preventDefault();
    const target = document.querySelector(this.getAttribute('href'));
    target.scrollIntoView({ behavior: 'smooth' });

    // Quita el # de la URL
    history.replaceState(null, null, ' ');
  });
});

/* Filtrado de eventos por estado de eventos */
document.addEventListener("DOMContentLoaded", function () {

  const botones = document.querySelectorAll(".filter-btn");
  const eventos = document.querySelectorAll(".event-card");

  botones.forEach(boton => {
    boton.addEventListener("click", () => {

      const filtro = boton.dataset.filter;

      eventos.forEach(evento => {
        const estado = evento.dataset.estado;

        if (filtro === "all" || estado === filtro) {
          evento.style.display = "block";
        } else {
          evento.style.display = "none";
        }
      });

      botones.forEach(b => b.classList.remove("active"));
      boton.classList.add("active");

    });
  });

});

/* filtrado de noticias por fecha */
document.addEventListener("DOMContentLoaded", function () {

  const botones = document.querySelectorAll(".date-filter");
  const noticias = document.querySelectorAll(".news-card");

  const hoy = new Date();
  hoy.setHours(0, 0, 0, 0);

  botones.forEach(btn => {
    btn.addEventListener("click", () => {

      const filtro = btn.dataset.filter;

      noticias.forEach(noticia => {

        const fechaNoticia = new Date(noticia.dataset.fecha);
        let mostrar = false;

        if (filtro === "all") {
          mostrar = true;
        }

        if (filtro === "today") {
          mostrar = fechaNoticia.getTime() === hoy.getTime();
        }

        if (filtro === "week") {
          const hace7 = new Date(hoy);
          hace7.setDate(hoy.getDate() - 7);
          mostrar = fechaNoticia >= hace7;
        }

        if (filtro === "month") {
          const hace30 = new Date(hoy);
          hace30.setDate(hoy.getDate() - 30);
          mostrar = fechaNoticia >= hace30;
        }

        noticia.style.display = mostrar ? "block" : "none";

      });

      botones.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

    });
  });

});
