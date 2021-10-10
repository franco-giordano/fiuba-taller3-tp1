from locust import HttpUser, task, between

"""
NOTES:
------------- BREAKPOINT TEST
Todas las cloud funcs limitadas a 2 instancias maximo
Con commit: 908275409ebfa97538eef5ef94fee5e9b2edb157 (sin cachear render_template en /app, con about_offices)
Sin cachear counters con Memorystore
30000 users max, incrementos +1/s, ~5min de run total
firestore: 20 shards por collection
duracion: 10/8/2021, 11:38:28 AM - 10/8/2021, 11:43:37 AM

CONCLUSIONES:
get_count forma un cuello de botella en el sistema (ver ex times)
asi, el sistema llega hasta 17.9RPS sin errores, 78 usuarios aprox
firestore alcanza hasta 400reads/s, pero 20writes/s.
--> Esto limita al incremento de contadores, pero no a su lectura,
	por lo que el bloqueante de get_count no es firestore en si.
la siguiente funcion que mas tarda es store-inc-counter
-> al final, store-inc-counter tambien se estaba quedando corta de instancias!
	Siguiente candidato a optimizar? Sera el siguiente breakpoint?
Los tiempos de ejecucion de las func, cuando si se ejecutan, se mantienen
	constantes a pesar de la carga
Locust ve tiempos de 11000ms en get-counter, pero gcp reporta 400ms, que paso?

"""

BASE_APP_URL = "https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/app"

class CuriousUser(HttpUser):
	wait_time = between(3,5)

	@task(3)
	def get_home(self):
		# grab html
		self.client.get(BASE_APP_URL + "?view=home")

		# grab stats
		self._get_stats('home')

	@task(4)
	def get_jobs(self):
		# grab html
		self.client.get(BASE_APP_URL + "?view=jobs")
		
		# grab stats
		self._get_stats('jobs')

	@task(2)
	def get_about(self):
		# grab html
		self.client.get(BASE_APP_URL + "?view=about")

		# grab stats
		self._get_stats('about')
	
	@task(2)
	def get_about_offices(self):
		# grab html
		self.client.get(BASE_APP_URL + "?view=about_offices")

		# grab stats
		self._get_stats('about_offices')


	@task(1)
	def get_about_legals(self):
		# grab html
		self.client.get(BASE_APP_URL + "?view=about_legals")

		# grab stats
		self._get_stats('about_legals')

	def _get_stats(self, v_type):
		self.client.post(f'https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/inc-counter?visit_type={v_type}')
		self.client.get(f'https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/get-counter?visit_type={v_type}')

	# # no quiero probar gcs! lo comento en todos los tasks
	# def _get_resources(self):
	# 	self.client.get("https://storage.googleapis.com/fgiordano-static/assets/css/main.css")
	# 	self.client.get("https://storage.googleapis.com/fgiordano-static/assets/css/fontawesome-all.min.css")
	# 	self.client.get("https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,700,900,300italic")
	# 	self.client.get("https://storage.googleapis.com/fgiordano-static/images/favicon.png")
	# 	self.client.get("https://storage.googleapis.com/fgiordano-static/assets/js/jquery.min.js")
	# 	self.client.get("https://storage.googleapis.com/fgiordano-static/assets/js/jquery.dropotron.min.js")
	# 	self.client.get("https://storage.googleapis.com/fgiordano-static/assets/js/main.js")
