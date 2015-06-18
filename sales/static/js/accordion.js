
function MakeAccordion(id) {
  $("#"+id+" li ul").hide();
  $("#"+id+" ul li").click(function() {
    $(this).children("ul").each(function () {
      $(this).parent().siblings("li").toggle();
      $(this).stop(true, true).toggle();
    }); 
    return false;
  });
}
