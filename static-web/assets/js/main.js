(function ($) {

	const BASE_PATH = 'https://southamerica-east1-taller3-fgiordano.cloudfunctions.net';

	const search_params = new URLSearchParams(window.location.search);
	const page_type = search_params.get('page');

	// Contador de visitas
	fetch(BASE_PATH + '/inc-counter?visit_type=' + page_type, { method: 'POST' })

	fetch(BASE_PATH + '/get-counter?visit_type=' + page_type)
		.then(response => response.json())
		.then(data => { $('#contador').text('Contador de visitas: ' + data['msg']); })
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