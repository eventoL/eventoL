const form = document.getElementById("emailForm");
  const errorMsg = document.getElementById("error-message");
  const successMsg = document.getElementById("success-message");

  form.addEventListener("submit", function(e) {
    e.preventDefault(); // Evita el envío tradicional
    
    const email = document.getElementById("userEmail").value;
    const regex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    // Validación
    if (!regex.test(email)) {
      errorMsg.style.display = "block";
      return false;
    }

    // Ocultar error si estaba visible
    errorMsg.style.display = "none";

    // Envío con Fetch API (alternativa moderna)
    fetch(form.action, {
      method: "POST",
      body: new FormData(form),
    })
    .then(response => {
      if (response.ok) {
        form.style.display = "none"; // Oculta el formulario
        successMsg.style.display = "block"; // Muestra éxito
      }
    })
    .catch(error => {
      alert("Error al enviar: " + error);
    });
  });