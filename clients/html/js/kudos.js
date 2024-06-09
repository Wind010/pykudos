
function getTeamMembers() {
    fetch(`${BASE_API_URL}/users/github/team`, {
        credentials: "include"
      })
    .then(response => response.json())
    .then(data => {
        //console.log(data);
        const datalist = document.getElementById('members');
        datalist.innerHTML = '';
        data.logins.forEach(item => {
            const option = document.createElement('option');
            option.value = item;
            datalist.appendChild(option);
        });
    })
    .catch(err => console.error(err));
}


function submitForm(formId) {
    event.preventDefault();
    const form = document.getElementById(formId);
    const formData = new FormData(form);

    form.action = `${BASE_API_URL}/item/`

    //const data = {};
    // formData.forEach((value, key) => {
    //   data[key] = value;
    // });

    const checkbox = document.getElementById('isOpportunity');
    const isOppertunity = checkbox.checked ? 'true' : 'false';
    const data = {
        "username": document.getElementById('member').value,
        "isOppertunity": isOppertunity,
        "description": document.getElementById('kudos').value,
    }
  
    fetch(form.action, {
        credentials: "include",
        method: form.method,
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then( response => {
        if (!response.ok) { throw response }
        return response.json();
      })
    .then(json => {
        cheer();
    })
    .then(data => {
        console.log(data);
    })
    .then()
    .catch(error => {
        console.error(error);
    });
    
}


window.onload = getTeamMembers()