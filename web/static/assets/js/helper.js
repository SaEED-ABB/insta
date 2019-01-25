$(document).ready(function () {
    resize();
});
$(window).on('load', function () {

});
$(window).resize(function () {
    setTimeout(resize, 20);
});
const resize = function () {
    var height = document.body.clientHeight;
    var width = document.body.clientWidth;
    $('.body_height').css('height', height + 'px');
    $('.body_width').css('width', width + 'px');
    $('.body_min_height').css('min-height', height + 'px');
};