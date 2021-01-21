(function($){
    $(".menu-item").on({
        mouseenter: function () {
            $(this).children('ul').children().removeClass('hidden');
        },
        mouseleave: function () {
            $(this).children('ul').children().not('.show').addClass('hidden');
        }
    });
})(jQuery);