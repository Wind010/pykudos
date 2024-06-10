
function getAccessToken() {
    let access_token = getCookie('access_token')
    if(access_token)
    {
        redirect();
        return;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const code = urlParams.get('code');
    
    if (!code) {
        return;
    }
    
    console.log(`Code present: ${code}`);
    fetch(`${BASE_API_URL}/auth/github/callback?code=${code}`, {
        credentials: "include"
    })
    .then(data => data.json())
    .then(data => setCookie('access_token', data.access_token, 7))
    .catch(err => console.error(err));
    
    waitForAccessToken();
}

function waitForAccessToken() {
    setInterval(function() {
        access_token = getCookie('access_token');
        console.log(`Access token: ${access_token}`);
    
        if (access_token) {
            redirect();
        }
    
      }, 1000);
}

function notSupport() {
    alert('Not supported.')
}

document.getElementById('github').addEventListener('click', getAccessToken)
document.getElementById('facebook').addEventListener('click', notSupport)
document.getElementById('twitter').addEventListener('click', notSupport)

// Once we hit the callback URI, the user is prompted to authorize the app.
// User gets redirected back to login page with code=xxx.
window.onload = getAccessToken()
