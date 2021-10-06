from locust import HttpUser, task, between

# REHACER ------------------------------------------------------
# mal configuradas las cloud funcs

"""
NOTES:
Todas las cloud funcs limitadas a 10 instancias maximo
Con commit: e94da430acc73d9c6c4a6e758631d294113588a0 (sin cachear render_templte en /app)
Sin cachear counters con Memorystore
300 users max, incrementos +1/s, ~XXXmin de run total
firestore: 20 shards por collection
duracion: 

CONCLUSIONES:
"""

BASE_APP_URL = "https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/app"

class CuriousUser(HttpUser):
	wait_time = between(6,10)

	@task(3)
	def get_home(self):
		# grab html
		self.client.get(BASE_APP_URL + "?view=home")

		# grab resources
		# self._get_resources()

		# grab stats
		self._get_stats('home')

	@task(4)
	def get_jobs(self):
		# grab html
		self.client.get(BASE_APP_URL + "?view=jobs")

		# grab resources
		# self._get_resources()
		# self.client.get("https://storage.googleapis.com/fgiordano-static/images/fiuba1.png")
		
		# grab stats
		self._get_stats('jobs')

	@task(2)
	def get_about(self):
		# grab html
		self.client.get(BASE_APP_URL + "?view=about")

		# grab resources
		# self._get_resources()
		# self.client.get("https://storage.googleapis.com/fgiordano-static/images/fiuba2.png")
		
		# grab stats
		self._get_stats('about')

	@task(1)
	def get_about_legals(self):
		# grab html
		self.client.get(BASE_APP_URL + "?view=about_legals")

		# grab resources
		# self._get_resources()
		
		# grab stats
		self._get_stats('about_legals')

	# no quiero probar gcs! lo comento en todos los tasks
	def _get_resources(self):
		self.client.get("https://storage.googleapis.com/fgiordano-static/assets/css/main.css")
		self.client.get("https://storage.googleapis.com/fgiordano-static/assets/css/fontawesome-all.min.css")
		self.client.get("https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,700,900,300italic")
		self.client.get("https://storage.googleapis.com/fgiordano-static/images/favicon.png")
		self.client.get("https://storage.googleapis.com/fgiordano-static/assets/js/jquery.min.js")
		self.client.get("https://storage.googleapis.com/fgiordano-static/assets/js/jquery.dropotron.min.js")
		self.client.get("https://storage.googleapis.com/fgiordano-static/assets/js/main.js")

	def _get_stats(self, v_type):
		self.client.get(f'https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/inc-counter?visit_type={v_type}')
		self.client.get(f'https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/get-counter?visit_type={v_type}')
