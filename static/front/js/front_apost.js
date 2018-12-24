$(document).ready(function() {

  $("#summernote").summernote({
    height: 300,
    toolbar: [
        ['style', ['style']],
        ['font', ['bold', 'italic', 'underline', 'strikethrough', 'superscript', 'subscript', 'clear']],
        ['fontname', ['fontname']],
        ['fontsize', ['fontsize']],
        ['color', ['color']],
        ['para', ['ol', 'ul', 'paragraph', 'height']],
        ['table', ['table']],
        ['insert', ['link']],
        ['view', ['undo', 'redo', 'fullscreen', 'codeview', 'help']]
    ]
  });
});

$(function () {

   $("#submit-btn").click(function (event) {
        event.preventDefault();
        var titleInput = $('input[name="title"]');
        var boardSelect = $("select[name='board_id']");
        var contentInput = $("#summernote").summernote('code');

        var title = titleInput.val();
        var board_id = boardSelect.val();
        var content = contentInput;

        zlajax.post({
            'url':'/apost/',
            'data':{
                'title':title,
                'content':content,
                'board_id':board_id
            },
            'success':function (data) {
                if(data['code'] == 200)
                {
                    zlalert.alertConfirm({
                       'msg':'恭喜!帖子发布成功!',
                       'cancelText':'回到首页',
                       'confirmText':'再发一篇',
                       'cancelCallback':function () {
                           window.location = '/'
                       },
                        'confirmCallback':function () {
                            titleInput.val("");
                            $("#summernote").summernote('code', '');
                        }
                    });
                }
                else
                {
                    zlalert.alertInfo(data['message']);
                }
            }
        });
   });
});