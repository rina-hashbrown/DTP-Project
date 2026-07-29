const rocketSearch = document.getElementById('rocketSearch');
rocketSearch.addEventListener('keyup', e => {
    let currentValue = e.target.value.toLowerCase();
    console.log(currentValue);
});