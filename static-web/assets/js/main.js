(function ($) {

	var $window = $(window),
		$body = $('body');

	console.log(window.location.pathname.substr(1).slice(0, -5));

	// Contador de visitas
	fetch('https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/get-counter?visit_type=home')
		.then(response => response.text())
		.then(data => { $('#contador').text('Contador de visitas: ' + data); })
		.catch(function (error) {
			console.log('Looks like there was a problem: \n', error);
		});

	// Breakpoints.
	breakpoints({
		xlarge: ['1281px', '1680px'],
		large: ['981px', '1280px'],
		medium: ['737px', '980px'],
		small: [null, '736px']
	});

	// Play initial animations on page load.
	$window.on('load', function () {
		window.setTimeout(function () {
			$body.removeClass('is-preload');
		}, 100);
	});

	// Dropdowns.
	$('#nav > ul').dropotron({
		mode: 'fade',
		noOpenerFade: true,
		alignment: 'center'
	});

	// Nav.

	// Title Bar.
	$(
		'<div id="titleBar">' +
		'<a href="#navPanel" class="toggle"></a>' +
		'</div>'
	)
		.appendTo($body);

	// Panel.
	$(
		'<div id="navPanel">' +
		'<nav>' +
		$('#nav').navList() +
		'</nav>' +
		'</div>'
	)
		.appendTo($body)
		.panel({
			delay: 500,
			hideOnClick: true,
			hideOnSwipe: true,
			resetScroll: true,
			resetForms: true,
			side: 'left',
			target: $body,
			visibleClass: 'navPanel-visible'
		});

})(jQuery);