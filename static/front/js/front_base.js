$(function () {
   $("#search-btn").click(function (event) {
        event.preventDefault();
        var searchInput = $('input[name="search_content"]');
        var search_content = searchInput.val();

        zlajax.get({
            'url':'/index/',
            'data':{
                'search_content':search_content,
            },
            'success':function (data) {
                // searchInput.val("");
            }
        });
   });
});