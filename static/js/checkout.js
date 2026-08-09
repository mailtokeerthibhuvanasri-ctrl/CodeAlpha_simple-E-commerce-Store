(function () {
  const cardInput = document.getElementById('card_number');
  if (cardInput) {
    cardInput.addEventListener('input', () => {
      let digits = cardInput.value.replace(/\D/g, '').slice(0, 16);
      cardInput.value = digits.replace(/(.{4})/g, '$1 ').trim();
    });
  }
  const expiryInput = document.getElementById('card_expiry');
  if (expiryInput) {
    expiryInput.addEventListener('input', () => {
      let digits = expiryInput.value.replace(/\D/g, '').slice(0, 4);
      if (digits.length >= 3) {
        expiryInput.value = digits.slice(0, 2) + '/' + digits.slice(2);
      } else {
        expiryInput.value = digits;
      }
    });
  }
})();
