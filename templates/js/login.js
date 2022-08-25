const labels = document.querySelectorAll('.form-control label')

labels.forEach(label => {
    letter = label.innerText.split('');
    const el =[];
    for (let i = 0;  i< letter.length; i++) {
        el[i] = `<span style="transition-delay:${i*30}ms">${letter[i]}</span>`; 
    };
    label.innerHTML = el.join('');
})