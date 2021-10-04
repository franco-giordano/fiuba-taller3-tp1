from locust import HttpUser, task

"""
NOTES:
Todas las cloud funcs limitadas a 10 instancias maximo
Con commit: 39ac3d0e5142ae21587a4ec72581010a041dc6a3 (sin cachear render_templte en /app)
Sin cachear counters con Memorystore
100 users max, incrementos +1/s, ~3min de run total
firestore: 20 shards por collection
"""

BASE_APP_URL = "https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/app"

class HelloWorldUser(HttpUser):
	@task
	def view_home(self):
		self.get_home()

	def get_home(self):
		# grab html
		self.client.get(BASE_APP_URL + "?view=home")

		# grab resources
		self.client.get("https://storage.googleapis.com/fgiordano-static/assets/css/main.css")
		self.client.get("https://storage.googleapis.com/fgiordano-static/assets/css/fontawesome-all.min.css")
		self.client.get("https://fonts.googleapis.com/css?family=Source+Sans+Pro:300,400,700,900,300italic")
		self.client.get("https://storage.googleapis.com/fgiordano-static/images/favicon.png")
		self.client.get("https://storage.googleapis.com/fgiordano-static/assets/js/jquery.min.js")
		self.client.get("https://storage.googleapis.com/fgiordano-static/assets/js/jquery.dropotron.min.js")
		self.client.get("https://storage.googleapis.com/fgiordano-static/assets/js/main.js")

		# grab stats
		self.client.get('https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/inc-counter?visit_type=home')
		self.client.get('https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/get-counter?visit_type=home')