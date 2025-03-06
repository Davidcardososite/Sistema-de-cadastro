// Validação do CPF
const cpfInput = document.getElementById('cpf');
if (cpfInput) {
  cpfInput.addEventListener('input', function () {
    const cpf = cpfInput.value.replace(/\D/g, ''); // Remove todos os caracteres não numéricos
    if (cpf.length !== 11) {
      cpfInput.setCustomValidity('CPF deve conter 11 dígitos.');
    } else {
      cpfInput.setCustomValidity(''); // Limpa a mensagem de erro
    }
  });
}



