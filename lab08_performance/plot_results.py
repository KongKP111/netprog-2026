import json
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

with open("results.json") as f:
    results = json.load(f)

distances = [r["distance_m"] for r in results]
throughput = [r["throughput_mbps"] for r in results]
loss = [r["loss_percent"] for r in results]

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.plot(distances, throughput, marker="o")
ax1.set_xlabel("Distance from AP (m)")
ax1.set_ylabel("Throughput (Mbps)")
ax1.set_title("Throughput vs. Distance")

ax2.plot(distances, loss, marker="o", color="crimson")
ax2.set_xlabel("Distance from AP (m)")
ax2.set_ylabel("Packet Loss (%)")
ax2.set_title("Packet Loss vs. Distance")

fig.tight_layout()
fig.savefig("performance_plot.png", dpi=150)
print("Saved performance_plot.png")
