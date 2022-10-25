async function fetchRequest(url, params, csrf_token) {
    bloqueoInterfaz();
    const resp = await fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token,
        },
        body: JSON.stringify(params),
        credentials: 'same-origin',
    });

    if (resp.status !== 200) {
        desbloqueoInterfaz();
        return {
            result: false,
            message: 'Error al realizar la petición'
        }
    }
    const data = await resp.json();
    if(!data.result) data["result"] = true;
    desbloqueoInterfaz();
    return data;
}

function appendValuesToSelect(id, values) {
    const select = document.getElementById(id);
    select.innerHTML = "";
    const option = document.createElement("option");
    option.value = "";
    option.text = "---------";
    select.add(option);
    values.forEach(value => {
        const keys = Object.keys(value);
        const option = document.createElement('option');
        option.value = value[keys[0]];
        option.text = value[keys[1]];
        select.appendChild(option);
    });
    return;
}
