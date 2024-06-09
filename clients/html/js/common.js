const BASE_API_URL = "http://127.0.0.1:8000"

function setCookie(name, value, days, sameSite = true) {
    var expires = "";
    if (days) {
      var date = new Date();
      date.setTime(date.getTime() + (days * 24 * 60 * 60 * 1000));
      expires = "; expires=" + date.toUTCString();
    }

    var sameSiteValue = ""
    if (sameSite) {
        var sameSiteValue = "; SameSite=" + sameSite;
    }
    document.cookie = name + "=" + (value || "") + expires + sameSiteValue + "; path=/";
}

function getCookie(name) {
    var value = "; " + document.cookie;
    var parts = value.split("; " + name + "=");
    if (parts.length === 2) return parts.pop().split(";").shift();
}

function redirect(path = "kudos.html") {
    const url = window.location.href;
    const pathParts = url.split('/');
    pathParts.pop();
    pathParts.push(path);
    targetUrl = pathParts.join('/');
    window.location.href = targetUrl;
}
