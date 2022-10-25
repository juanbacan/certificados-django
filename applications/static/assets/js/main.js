function ready(callback){
    // in case the document is already rendered
    if (document.readyState!='loading') callback();
    // modern browsers
    else if (document.addEventListener) document.addEventListener('DOMContentLoaded', callback);
    // IE <= 8
    else document.attachEvent('onreadystatechange', function(){
        if (document.readyState=='complete') callback();
    });
}

const ocultarElementos = (arrayOfIds) => {
    arrayOfIds.forEach(element => {
        document.getElementById(element).style.display = 'none';
    });
}
const mostrarElementos = (arrayOfIds) => {
    arrayOfIds.forEach(element => {
        document.getElementById(element).style.display = 'flex';
    });
}
const validarElementos = (arrayOfIds) => {
    arrayOfIds.forEach(element => {
        document.getElementById(element).required = true;
    });
}
const noValidarElementos = (arrayOfIds) => {
    arrayOfIds.forEach(element => {
        document.getElementById(element).required = false;
    });
}

function bloqueoInterfaz() {
    console.log("Bloqueando Interfaz");
    document.getElementById( 'loading-static' ).style.display = 'flex';
}
function desbloqueoInterfaz() {
    console.log("Desbloqueando Interfaz");
    document.getElementById( 'loading-static' ).style.display = 'none';
}

// const modalEdicion = document.getElementById('modalEdicion');
const modals = document.getElementsByClassName('formmodal');
for (let i = 0; i < modals.length; i++) {
    modals[i].addEventListener('click', async function(e) {
        try {
            e.preventDefault()
            const nhref = modals[i].getAttribute('nhref');
            if (!nhref) return;

            bloqueoInterfaz();
            const resp = await fetch(nhref);
            
            desbloqueoInterfaz();

            if (resp.ok){
                const data = await resp.text();
                // from data get the all the content of the tag "script"
                const scripts = data.match(/<script[^>]*>([\s\S]*?)<\/script>/gi);
                // Remove all the scripts from the data
                const dataClean = data.replace(scripts, '');
                const modalEdicion = document.getElementById('modalEdicion');
                modalEdicion.innerHTML = dataClean;
                const myModal = new bootstrap.Modal(modalEdicion);
                myModal.show()
                // Put the scripts in the body of the page
                scripts.forEach(script => {
                    // If script contain src
                    if (script.includes('src')) {
                        // Get the src
                        const src = script.match(/src="([^"]*)"/)[1];
                        // Create a new script tag
                        const newScript = document.createElement('script');
                        // Set the src of the new script tag
                        newScript.src = src;
                        // Append the new script tag to the body
                        document.body.appendChild(newScript);
                    } else {
                        const scriptClean = script.replace(/<script[^>]*>|<\/script>/gi, '');
                        // Create a new script tag
                        const newScript = document.createElement('script');
                        // Set the innerHTML of the new script tag
                        newScript.innerHTML = scriptClean;
                        // Append the new script tag to the body
                        document.body.appendChild(newScript);
                    }
                } );
            } else{
                console.log('Error al cargar el formulario');
                desbloqueoInterfaz();
            }
            
        } catch{
            console.log('Error al cargar el formulario')
            desbloqueoInterfaz();
        }
    })
}

// Función para enviar un formulario dinámico en modal
const submitModalForm1 = async () => {
    const form = document.getElementById('modalForm1');
    //if (!form.reportValidity()) return;
    form.classList.add('was-validated')
    
    if (!form.checkValidity()) return;

    bloqueoInterfaz();
    const resp = await fetch(form.getAttribute('action'), {
        method: 'POST',
        body: new FormData(form)
    })

    console.log(resp)

    if (resp.status === 200) {

        if(!resp.redirected){
            console.log("No redireccionado");
            console.log("bUU")
            const data2 = await resp.text();
            console.log(data2)

            // TODO: Ver si se retorna un formulario y agregar esto al html sino no
            const modalEdicion = document.getElementById('modalEdicion');
            modalEdicion.innerHTML = data2;
            return;
        }
        location.href = resp.url;
        return;

    } else if (resp.status === 400) {
        console.log("Respuesta 400");
        const data = await resp.json();
        console.log(data.mensaje)
        desbloqueoInterfaz();
        return;
    } else {
        const data3 = await resp.json();
        console.log('Error al cargar el formulario');
        console.log(data3.mensaje);
        desbloqueoInterfaz();
        return;
    }
}