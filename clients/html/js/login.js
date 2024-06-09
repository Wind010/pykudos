
function getAccessToken() {
    let access_token = getCookie('access_token')
    if(access_token)
    {
        redirect();
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    console.log('Code present', code);

    fetch(`${BASE_API_URL}/auth/github/callback?code=${code}`, {
        credentials: "include"
    })
    .then(data => data.json())
    .then(data => setCookie('access_token', data.access_token, 7))
    .catch(err => console.error(err));
    

    access_token = getCookie('access_token');
    console.log(access_token);

    if (access_token) {
        redirect();
    }
}


window.onload = getAccessToken()