// Modo Claro/Oscuro
  // Cargar preferencia guardada
  if (localStorage.getItem("theme") === "dark") {
      document.body.classList.add("dark-mode");
  }

  document.getElementById("theme-toggle").addEventListener("click", function () {
      document.body.classList.toggle("dark-mode");

      // Guardar preferencia
      if (document.body.classList.contains("dark-mode")) {
          localStorage.setItem("theme", "dark");
      } else {
          localStorage.setItem("theme", "light");
      }
  });

