$(document).ready(function () {
    $('*[data-background-image]').each(function () {
        $(this).css({
            'background-image': 'url(' + $(this).data('background-image') + ')'
        });
    });
});