$(function ()
{
    $("#submit").click(function (event)
    {
        event.preventDefault();
        var emailE = $("input[name='email']");
        var passwordE = $("input[name='password']");
        var rememberE = $("input[name='remember']");

        var email = emailE.val();
        var password = captchaE.val();
        var remember = rememberE.val();

        zlajax.post({
            'url': '/cms/login/',
            'data':
            {
                'email': email,
                'password': password,
                'remember': remember
            },
            'success': function (data)
            {
                if (data['code'] == 200)
                {
                    zlalert.alertSuccessToast('参数错误!');
                }
                else
                {
                    zlalert.alertInfo(data['message']);
                }
            },
            'fail':function (error)
            {
                zlalert.alertNetworkError();
            }
        });
    });
});