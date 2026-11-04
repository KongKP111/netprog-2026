import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("rtt_near.json") as f:
    near = json.load(f)
with open("rtt_far.json") as f:
    far = json.load(f)

plt.plot(near, label="near (5m)", marker=".")
plt.plot(far, label="far (28m)", marker=".")
plt.xlabel("Message number")
plt.ylabel("Application RTT (ms)")
plt.title("Application-Level RTT: Near vs. Far")
plt.legend()
plt.tight_layout()
plt.savefig("rtt_plot.png", dpi=150)
print("Saved rtt_plot.png")
