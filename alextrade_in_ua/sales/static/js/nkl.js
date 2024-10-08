
function ChangeOst(id, nam, val) {
  var input = $('#'+id+' input[name$="'+nam+'"] ');
  input.attr("value", val);
}

function ChangeNkl(obj, id, id_nkl) {
  var name = $(obj).attr("name");
  var val = parseInt($(obj).val() || 0, 0);
  var parent = $(obj).parent();
  var nkl_val = $('#'+id_nkl+' input[name$="'+name+'"] ');
  if (nkl_val.html() != "") {
    var nam = parent.find(".nam");
    var input = parent.find(".val");
    var res = $("#"+id_nkl+" ul li ul").append('<li class="node"><span class="nam">'+nam.html()+'</span><input class="val" type="text" name="'+input.attr("name")+'"/><input class="del" main_name="'+input.attr("name")+'" type="button" value="Удалить"/></li>');
    res.bind("click", function () {return false;});
    var li = res.find("li").last();
    li.find(".del").bind("click", function () {
      ChangeOst(id, $(this).attr("main_name"), 0);
      $(this).parent().remove();
    });
    nkl_val = li.find(".val");
    nkl_val.bind("change", function () {
      ChangeOst(id, $(this).attr("name"), $(this).val());
      return false;
    });
  }

  if (val > 0) {
    nkl_val.attr("value", val);
  } else {
    nkl_val.parent().remove();
  }
}

function MakeNkl(id, id_nkl) {
  $("#"+id+" .node .val").bind("change", function () {
    ChangeNkl(this, id, id_nkl);
  });
}