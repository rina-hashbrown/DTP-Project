const rocketSearch = document.getElementById('rocketSearch');
rocketSearch.addEventListener('keyup', e => {
    let currentValue = e.target.value.toLowerCase();
    let rockets = document.querySelectorAll('h3.title');
    rockets.forEach(rocket => {
        if (rocket.textContent.toLowerCase().includes(currentValue)) {
            rocket.parentNode.parentNode.style.display = '';
        } else {
            rocket.parentNode.parentNode.style.display = 'none';
        }
    })
});