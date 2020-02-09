let csrftoken = Cookies.get('csrftoken');
function csrfsafeMethod(method){
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function(xhr,settings){
        if(!scrfsafeMethod(settings.type) && !this.crossDomain){
            xhr.setRequestHeader("x-CSRFToken",csrftoken);
        }
    }
});