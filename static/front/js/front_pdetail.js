$(document).ready(function() {

  $("#summernote").summernote({
    height: 120,
    toolbar: [
        ['style', ['style']],
        ['font', ['bold', 'italic', 'underline', 'clear']],
        ['fontname', ['fontname']],
        ['fontsize', ['fontsize']],
        ['color', ['color']],
        ['para', ['ol', 'ul', 'paragraph', 'height']],
        ['table', ['table']],
        ['insert', ['link']],
    ]
  });
});

$(function () {
    $("#comment-btn").click(function(event) {
        event.preventDefault();
        var loginTag = $("#login-tag").attr("data-is-login");
        if(!loginTag){
            window.location = '/signin/';
        }
        else{
            var content = $("#summernote").summernote('code');
            var post_id = $("#post-content").attr("data-id");
            zlajax.post({
                'url': '/acomment/',
                'data':{
                    'content': content,
                    'post_id': post_id
                },
                'success':function (data) {
                    if(data['code'] == 200){
                        window.location.reload();
                    }
                    else{
                        zlalert.alertInfo(data['message']);
                    }
                }
            });
        }
    });
});