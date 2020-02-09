(function(){
    let jquery_version = '3.3.1';
    let site_url = 'https://socio.com:8000/';
    let static_url = site_url + 'static/';
    let min_width = 100;
    let min_height = 100;

    function myBookmarklet(msg){
        // here goes the bookmarklet code
        let css = $('link');
        css.attr({
            'rel': 'stylesheet',
            'type': 'text/css',
            'href': static_url + 'css/bookmarklet.css?r=' + Math.floor(Math.random()*9999999999999999)
        });
        $('head').append(css);

        box_html = '<div id="bookmarklet"><a href="#" id="close">&times;</a>' + 
        '<h1>Select an image to bookmark:</h1>'+
        '<div class="images"></div></div>';
        $('body').append(box_html);

        //close event
        $('#bookmarklet #close').click(function(){
            $('#bookmarklet').remove();
        });
        
        // find images on the site and display them
        $.each($('img[src$=".jpg"]'),function(index,image){
            if($(image).width()>=min_width && $(image).height()>min_height){
               let image_url = $(image).attr('src');
                $('#bookmarklet .images').append('<a><img scr="'+image_url +'"></a>');
            }
        });
        $('#bookmarklet .images a').click(function(e){
           let selected_image = $(this).children('img').attr('src');
            $('#bookmarklet').hide();
            // open new window
            window.open(site_url +'images/create/?url='
                    + encodeURIComponent(selected_image)
                    + 'title='
                    + encodeURIComponent($('title').text()),
                    '_blank');
        });
    };

    // check if jquery is loaded
    // if(typeof window.jQuery != 'undefined'){
        mybookmarklet();
    // }else{
        // check for conflicts
        // let conflict = typeof window.$ != 'undefined';
        //create a script and point it to google api
        // let script = document.createElement("script");
        // script.scr = static_url + 'js/jquery/jquery.min.js';
        // document.head.appendChild(script);

        //create a way to wait until script loads
        // let attempts = 15;
        // (function(){
            // check again if jquery is defined
            // if(typeof window.jquery == 'undefined'){
                // if (--attempts > 0) {
                    //calls himself in a few milliseconds
                    // windows.setTimeout(arguments.callee, 250);
                // }else {
                    // too mmuch attempts to load, send erro
                    // alert('an errro occured while loading jquery');
                // }
            // }else{
                // bookmarklet();
            // }
        // })();
    // }

})();