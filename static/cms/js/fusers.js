$(function (){
    $(".delete-fuser-btn").click(function (event){
        var self = $(this);
        var tr = self.parent().parent();
        var fuser_id = tr.attr('fuser-id');

        zlalert.alertConfirm({
            "msg":"您确定要删除这个用户么?",
            'confirmCallback': function (){
                zlajax.post({
                    'url':'/cms/dfusers/',
                    'data':{
                        'fuser_id':fuser_id
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