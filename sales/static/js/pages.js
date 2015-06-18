
function MakePages(id) {
  $("#"+id+" > .page").hide();
  $("#"+id+" > .page > h1").hide();
  $("#"+id+" > .page.active-page").show();
  $.each($("#"+id+" > .page > h1"), function () {
    if ($(this).parent().hasClass("active-page")) {
      $("#"+id+" > .page-list").append('<li class="active-page"><a href="#" pageid="'+$(this).parent().attr('id')+'">'+$(this).text()+'</a></li>')
    } else {
      $("#"+id+" > .page-list").append('<li><a href="#" pageid="'+$(this).parent().attr('id')+'">'+$(this).text()+'</a></li>')
    }
  });
  $("#"+id+" > .page-list li").bind("click", function () {
    $("#"+id+" > .page-list li").removeClass("active-page");
    $(this).addClass("active-page");
    $("#"+id+" > .page.active-page").hide().removeClass("active-page");
    $("#"+$(this).children("a").attr("pageid")).show().addClass("active-page");
  });
}
