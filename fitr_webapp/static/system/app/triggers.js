$('#navDrop').on('show.bs.dropdown', function () {
    $('body').addClass("noti-dark");
});

$('#navDrop').on('hide.bs.dropdown', function () {
    $('body').removeClass("noti-dark");
});

$('#profileDrop').on('show.bs.dropdown', function () {
    $('body').addClass("noti-dark");
});

$('#profileDrop').on('hide.bs.dropdown', function () {
    $('body').removeClass("noti-dark");
});

$('#sidebar').on("click", function (e) {
    if ($("#navDrop").hasClass("show")) {
        $('#navDrop').dropdown('toggle')
    } else if ($("#profileDrop").hasClass("show")) {
        $('#profileDrop').dropdown('toggle')
    }
});