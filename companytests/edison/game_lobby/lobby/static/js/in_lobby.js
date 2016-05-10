$(document).ready(function() {
	poll_xhr.abort()
});

leave_lobby = function() {
	$.ajax({
		url: url_in_lobby,
		type: 'POST',
		data: JSON.stringify({'player': player})
		success: function () {
			console.log(player 'leave');
		}
	})
}