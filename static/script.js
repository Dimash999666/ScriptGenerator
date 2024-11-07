document.addEventListener('DOMContentLoaded', function () {
  const generateButton = document.getElementById('generate-button');

  generateButton.addEventListener('click', function () {
    const prompt = document.getElementById('prompt').value;
    const style = document.getElementById('style').value;
    const length = document.getElementById('length').value;

    fetch('/generate-script', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ prompt, style, length }),
    })
      .then((response) => response.json())
      .then((data) => {

        document.getElementById('script-output').textContent = data.script;
      })
      .catch((error) => console.error('Error:', error));
  });
});
