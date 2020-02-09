// for drop down menu of the user account
let btn = document.querySelector('#dropbtn');
btn.addEventListener('click',()=>{
    let dropdown = document.getElementById('myDropdown');
    dropdown.classList.toggle('show');
});

window.addEventListener('click',(e)=>{
    
    if (!e.target.matches('#dropbtn')){
        let dropdown = document.querySelector('#myDropdown');
        if(dropdown.classList.contains('show')){
            dropdown.classList.remove('show');
        }
    }
})

// ajax csrftoken protection
let csrftoken = Cookies.get('csrftoken');
function csrfsafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}
$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfsafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("x-CSRFToken", csrftoken);
        }
    }
});

// // for image detail.html like functionality
// $('a.like').click(function(e){
//     e.preventDefault();
//     $.post('socio.com:8000/images/like/',
//     {
//         id: $(this).data('id'),
//         action: $(this).data('action')
//     },
//     function(data){
//         if (data['status']=='ok'){
//             let previous_action = $('a.like').data('action')

//             // toggle data-action
//             $('a.like').data('action', previous_action == 'like'?'unlike':'like');
//             //toggle link text
//             $('a.like').text(previous_action=='like'?'Unlike':'Like');

//             // update total likes
//             let previous_likes = parseInt($('span.count .total').text());
//             $('span.count .total').text(previous_action == 'like' ? previous_likes + 1 : previous_likes - 1);
//         }
//     });
// });

// // ajax pagination list view for images
// let page = 1;
// let empty_page = false;
// let block_request = false;

// $(window).scroll(function(){
//     let margin = $(document).height()- $(window).height()-200;
//     if ($(window).scrollTop()> margin && empty_page == false && block_request == false){
//         block_request = true;
//         page +=1;
//         $.get('?page='+ page,function(data){
//             if(data ==''){
//                 empty_page = true;
//             }
//             else {
//                 block_request = false;
//                 $('#image-list').append(data);
//             }
//         });
//     }
// });
