from locust import HttpUser, task, between
from locust import LoadTestShape

"""
NOTES:
------------- ENDURANCE TEST
cloud funcs limitadas a 2 instancias maximo EXCEPTO POR
	store-inc-counter con 4 instancias
Con commit:  (cacheando L1 10 segs get-counter, otros cambios son en GCP)
CACHEANDO CON VARIABLE GLOBAL, 10 SEGUNDOS TTL 
custom shape, ~XXXmin de run total
firestore: 20 shards por collection
duracion: 


CONCLUSIONES:

"""

BASE_APP_URL = "https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/app"


class CuriousUser(HttpUser):
    wait_time = between(3, 5)

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
        self.client.post(
            f'https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/inc-counter?visit_type={v_type}')
        self.client.get(
            f'https://southamerica-east1-taller3-fgiordano.cloudfunctions.net/get-counter?visit_type={v_type}')


class StagesShape(LoadTestShape):
    """
    A simply load test shape class that has different user and spawn_rate at
    different stages.

    Keyword arguments:

        stages -- A list of dicts, each representing a stage with the following keys:
            duration -- When this many seconds pass the test is advanced to the next stage
            users -- Total user count
            spawn_rate -- Number of users to start/stop per second
            stop -- A boolean that can stop that test at a specific stage

        stop_at_end -- Can be set to stop once all stages have run.
    """

    stages = [
        {"duration": 525, "users": 450, "spawn_rate": 2},
        {"duration": 625, "users": 650, "spawn_rate": 2},
        {"duration": 685, "users": 650, "spawn_rate": 2},
        {"duration": 1160, "users": 300, "spawn_rate": 2},
        {"duration": 1310, "users": 1, "spawn_rate": 2}
    ]

    def tick(self):
        run_time = self.get_run_time()

        for stage in self.stages:
            if run_time < stage["duration"]:
                tick_data = (stage["users"], stage["spawn_rate"])
                return tick_data

        return None
