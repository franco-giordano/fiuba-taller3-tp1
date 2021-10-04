from locust import HttpUser, task

"""
NOTES:
Todas las cloud funcs limitadas a 10 instancias maximo
Con commit: 39ac3d0e5142ae21587a4ec72581010a041dc6a3 (sin cachear render_templte en /app)
Sin cachear counters con Memorystore
100 users max, incrementos +1/s, ~3min de run total
firestore: 20 shards por collection
duracion: 10/3/2021, 6:51:40 PM - 6:54:22 PM

CONCLUSIONES:
get_count parece ser la unica que lanzo errores
get_count usa bastante ram, pero no tan distinto a otras
get_count tarda mucho en ejecutarse, hasta 400ms cuando el resto usa 50-100ms.
firestore alcanza hasta 400reads/s, pero 20writes/s.
--> Esto limita al incremento de contadores, pero no a su lectura,
	por lo que el bloqueante de get_count no es firestore en si.
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