from locust import HttpUser, task, between

"""
NOTES:
------------- ENDURANCE TEST
HACER!

CONCLUSIONES:

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
