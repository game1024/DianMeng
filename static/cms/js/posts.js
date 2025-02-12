$(function () {
    $(".highlight-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr  = self.parent().parent();
        var post_id = tr.attr("data-id");
        var highlight = parseInt(tr.attr("data-highlight"));
        var url = "";
        if(highlight){
            url = "/cms/uhpost/";
        }
        else {
            url = "/cms/hpost/"
        }
        zlajax.post({
            'url':url,
            'data':{
                'post_id':post_id
            },
            'success':function (data) {
                if(data['code'] == 200){
                    zlalert.alertSuccessToast('操作成功！');
                    setTimeout(function () {
                        window.location.reload();
                    },500);
                }
                else{
                    zlalert.alertInfo(data['message']);
                }
            }
        });
    });
});

$(function () {
    $(".remove-btn").click(function (event) {
        event.preventDefault();
        var self = $(this);
        var tr  = self.parent().parent();
        var post_id = tr.attr("data-id");
        var url = "";

        zlalert.alertConfirm({
            "msg":"确定要删除这个帖子么?",
            'confirmCallback': function (){
                zlajax.post({
                    'url':'/cms/dpost/',
                    'data':{
                        'post_id':post_id
                    },
                    'success': function (data){
                        if(data['code'] == 200)
                        {
                            window.location.reload();
                        }
                        else
                        {
                            zlalert.alertInfo(data['message']);
                        }
                    }
                })
            }
        });
    });
});