(function ($) {

	let paths = window.location.pathname.split('/');
	let type = paths[paths.length - 1].slice(0, -5);

	// Contador de visitas
	fetch(`https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/inc-counter?visit_type=${type}`)
		// .then(response => response.text())
		// .then(data => { $('#contador').text('Contador de visitas: ' + data); })
		// .catch(function (error) {
		// 	console.log('Looks like there was a problem: \n', error);
		// });

	fetch(`https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/get-counter?visit_type=${type}`)
		.then(response => response.text())
		.then(data => { $('#contador').text('Contador de visitas: ' + data); })
		.catch(function (error) {
			console.log('Looks like there was a problem: \n', error);
		});

	// Dropdowns.
	$('#nav > ul').dropotron({
		mode: 'fade',
		noOpenerFade: true,
		alignment: 'center'
	});

})(jQuery);