var $messages = $('.messages-content'),
    d, h, m,
    i = 0;

$(window).load(function() {
  $messages.mCustomScrollbar();
  setTimeout(function() {
    //fakeMessage();
  }, 100);
});

function updateScrollbar() {
  $messages.mCustomScrollbar("update").mCustomScrollbar('scrollTo', 'bottom', {
    scrollInertia: 10,
    timeout: 0
  });
}

function setDate(){
  d = new Date()
  if (m != d.getMinutes()) {
    m = d.getMinutes();
    $('<div class="timestamp">' + d.getHours() + ':' + m + '</div>').appendTo($('.message:last'));
  }
}

function insertMessage() {
  msg = $('.message-input').val();
  if ($.trim(msg) == '') {
    return false;
  }
  $('<div class="message message-personal">' + msg + '</div>').appendTo($('.mCSB_container')).addClass('new');
  setDate();
  $('.message-input').val(null);
  updateScrollbar();
	interact(msg);
  setTimeout(function() {
    //fakeMessage();
  }, 1000 + (Math.random() * 20) * 100);
}

$('.message-submit').click(function() {
  insertMessage();
});

$(window).on('keydown', function(e) {
  if (e.which == 13) {
    insertMessage();
    return false;
  }
});



$(document).on('click','.satisfy-button', function (){
  var log_pk = this.value;
  var feedback = 1;
  var csrftoken = getCookie('csrftoken');
  $.post("/feedback/", {
	  lpk: log_pk,
	  actual: feedback,
	  csrfmiddlewaretoken: csrftoken,
	}).done(function(reply) {
  	
  	$("#recom_" + log_pk).fadeOut( "fast", function() {
            // Animation complete.
          });
  	$("#mrecom_" + log_pk).append("학습완료!! 피드백 감사드려요:)");
  	
	}).fail(function() {
	  alert('error calling function');
	});
});


$(document).on('click','.unsatisfy-button', function (){
  
  var log_pk = this.value;
  var feedback = 0;
  var csrftoken = getCookie('csrftoken');
  $.post("/feedback/", {
	  lpk: log_pk,
	  actual: feedback,
	  csrfmiddlewaretoken: csrftoken,
	}).done(function(reply) {
  	
  	$("#recom_" + log_pk).fadeOut( "fast", function() {
            // Animation complete.
          });
  	$("#mrecom_" + log_pk).append("학습완료!! 피드백 감사드려요:)");
  	
	}).fail(function() {
	  alert('error calling function');
	});
});



$(document).on('click','.see-detail', function(){
  
  var log_pk = this.id;
  var csrftoken = getCookie('csrftoken');
  $.post("/seeDetail/", {
	  lpk: log_pk,
	  csrfmiddlewaretoken: csrftoken,
	}).done(function(reply) {
  	  //history.pushState(null,null,event.target.href);
    var $toastContent = $('<div><span class ="glyphicon glyphicon-remove toast-out" style="float: right" aria-hidden="true"></span><h5>' + reply['rTitle'] + '</h5><p>주재료: ' + reply['rPrimary'] + '</p><p>부재료: ' + reply['rSub'] + '</p><p>'+ reply['rText'] + '</p></div>');
    Materialize.toast($toastContent, 50000);
    event.preventDefault();
      // <p>당신이 좋아 할 확률 : '+ reply['aprob'] + '</p>
  	
	}).fail(function() {
	  alert('error calling function');
	});
});

$(document).on('click', '.toast-out', function(){
  	$(".toast").fadeOut( "fast", function() {
            // Animation complete.
    });
  
});  

  $(document).ready(function(){
    $('.collapsible').collapsible({
      accordion : true // A setting that changes the collapsible behavior to expandable instead of the default accordion style
    });
  });


// using jQuery
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}




function interact(message){
	// loading message
  $('<div class="message loading new"><figure class="avatar"><img src="/static/res/botprofile.png" /></figure><span></span></div>').appendTo($('.mCSB_container'));
	// make a POST request [ajax call]
	var csrftoken = getCookie('csrftoken');
	$.post("/message/", {
	  msg: message,
	  csrfmiddlewaretoken: csrftoken,
	}).done(function(reply) {
		// Message Received
		// 	remove loading meassage
    $('.message.loading').remove();
		// Add message to chatbox
    if ('image' in reply) {
      $('<div class="message new" id="mrecom_' + reply['logPK'] + '"><figure class="avatar"><img src="/static/res/botprofile.png" /></figure><div class="well" id="recom_' + reply['logPK'] +'" style=width:230px;height:auto;"><img style="width:200px;height:auto;" src="'+ reply['image'] + '"/><p style="color:black;">' + reply['text'] + '</p><p><a class="see-detail" type="submit" id="' + reply['logPK'] + '"  href="#">자세히보기</a></p><button style="max-width:100px;" value="' + reply['logPK'] + '" type="submit" class="satisfy-button btn btn-success teal accent-4">만족</button><button style="max-width:100px;"  value="' + reply['logPK'] + '" type="submit" class="unsatisfy-button btn btn-success teal accent-4">불만족</button></div></div>').appendTo($('.mCSB_container')).addClass('new');
     }
     else {       
      $('<div class="message new"><figure class="avatar"><img src="/static/res/botprofile.png" /></figure>' + reply['text'] + '</div>').appendTo($('.mCSB_container')).addClass('new');
     }
    setDate();
    updateScrollbar();

		}).fail(function() {
				alert('error calling function');
				});
}

