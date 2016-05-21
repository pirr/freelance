// $(document).ready(function () {
// 	on
// 	timer();
// });

var delay = 0;

(function poll(){
	
		setTimeout(function(){

		    $.ajax({ 
		    	url: url_get_lobbys,
		    	success: function(data) {
		    		$('#lobbys_list').html(data);
		    		$.ajax({
		    			url: url_online,
		    			success: function(data) {
		    				$('#online').html(data)
		    			}
		    		})
		    	}, 
		    	dataType: 'html', 
		    	complete: poll, 
		    	timeout: 30000 
		    });
		}, delay);

		delay = 5000
	
})();

timer = function() {
	//
	// add deactivate button "apply"
	//
	var timeout = $.now() + 3000;
	$('#clock').countdown(timeout)
	.on('update.countdown', function(event) {
		var format = '%S';
		$(this).html(event.strftime(format));
	})
	.on('finish.countdown', function(event) {
		$.ajax({
			url: off_timeout,
			method: 'POST',
			success: function() {
				console.log('time to play')
			}
		})
		$('.countdown').empty()

	});
}


confirm_submit = function(form) {
	
	var lobby = $(form).attr('data-lobby-name');
	var apply = confirm('Вы хотите зайти в лобби - ' + lobby);
	if (apply===false) {
		return false
	}
}



// data_post = function(but, url, cnfrm) {

// 	if (cnfrm===1) {
// 		var lobby = $(but).attr('data-lobby-name');
// 		var apply = confirm('Вы хотите зайти в лобби - ' + lobby);

// 		if (apply===false) {
// 			return false
// 		}
// 	}

// 	var item = $(but).attr('value');
// 	console.log(item)
// 	$.ajax({
// 		url: url,
// 		type: 'POST',
// 		data: JSON.stringify({'item':item}),
// 		success: function () {
// 			console.log('ok');
// 		},
// 		complete: function () {
// 			$.ajax({
// 				url: url_get_lobbys,
// 		    	success: function(data) {
// 		    		$('#lobbys_list').html(data);
// 		    	}
// 			});
// 		}
// 	});
// }