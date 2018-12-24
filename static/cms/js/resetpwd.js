$(function ()
{
    $("#submit").click(function (event)
    {
        event.preventDefault();

        var oldpwdE =  $("input[name=oldpwd]");
        var newpwdE =  $("input[name=newpwd]");
        var newpwd2E = $("input[name=newpwd2]");

        var oldpwd  = oldpwdE.val();
        var newpwd  = newpwdE.val();
        var newpwd2 = newpwd2E.val();

        //1.模板meta标签中渲染一个csrf-token
        //2.在ajax请求头部设置X-CSRFtoken
        zlajax.post({
            'url':'/cms/resetpwd/',
            'data': {
                'oldpwd': oldpwd,
                'newpwd': newpwd,
                'newpwd2': newpwd2
            },
            'success': function (data)
            {
                if(data['code'] == 200)
                {
                    zlalert.alertSuccessToast("密码修改成功!");
                    oldpwdE.val("");
                    newpwdE.val("");
                    newpwd2E.val("");
                }
                else
                {
                    var message = data['message'];
                    zlalert.alertInfo(message);
                }
            },
            'fail':function (error)
            {
                zlalert.alertNetworkError(error);
            }
        });
    });
});