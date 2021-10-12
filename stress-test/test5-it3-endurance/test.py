import matplotlib.pyplot as plt

stages = [
    {"duration": 525, "users": 450, "spawn_rate": 2},
    {"duration": 625, "users": 650, "spawn_rate": 2},
    {"duration": 685, "users": 650, "spawn_rate": 2},
    {"duration": 1160, "users": 300, "spawn_rate": 2},
    {"duration": 1310, "users": 1, "spawn_rate": 2}
]

def tick(now):
    run_time = now

    for stage in stages:
        if run_time < stage["duration"]:
            tick_data = (stage["users"], stage["spawn_rate"])
            return tick_data

    return None

times = []
ticks = []
current_users = 0
current_target = (0,0)

for i in range(0,22*60, 5):
    current_target = tick(i)
    if current_target!=None:
        change = 0
        if current_users < current_target[0]:
            change = current_target[1]
        elif current_users > current_target[0]:
            change = -current_target[1]
        current_users = current_users+change*5
        times.append(i)
        ticks.append(current_users)

plt.plot(times,ticks)
plt.show()