import pandas as pd
import matplotlib.pyplot as plt

data = [
    {
        "id": "868b6btc9",
        "date_created": "2024-12-05T15:01:33.156000+00:00",
        "date_done": None,
    },
    {
        "id": "868b6btc2",
        "date_created": "2024-12-05T15:01:32.636000+00:00",
        "date_done": "2025-02-01T21:04:48.972000+00:00",
    },
    {
        "id": "868b6btbx",
        "date_created": "2024-12-05T15:01:32.355000+00:00",
        "date_done": "2025-02-01T17:19:51.766000+00:00",
    },
    {
        "id": "868b6btc5",
        "date_created": "2024-12-05T15:01:32.981000+00:00",
        "date_done": None,
    },
    {
        "id": "868b6btc1",
        "date_created": "2024-12-05T15:01:32.537000+00:00",
        "date_done": "2025-02-01T17:19:51.766000+00:00",
    },
    {
        "id": "868b6btbw",
        "date_created": "2024-12-05T15:01:32.305000+00:00",
        "date_done": None,
    },
    {
        "id": "868b6btc9",
        "date_created": "2024-12-05T15:01:33.156000+00:00",
        "date_done": None,
    },
    {
        "id": "868b6btc2",
        "date_created": "2024-12-05T15:01:32.636000+00:00",
        "date_done": "2025-02-01T21:04:48.972000+00:00",
    },
    {
        "id": "868b6btbx",
        "date_created": "2024-12-05T15:01:32.355000+00:00",
        "date_done": "2025-02-01T17:19:51.766000+00:00",
    },
    {
        "id": "868b6btc5",
        "date_created": "2024-12-05T15:01:32.981000+00:00",
        "date_done": None,
    },
    {
        "id": "868b6btc1",
        "date_created": "2024-12-05T15:01:32.537000+00:00",
        "date_done": None,
    },
    {
        "id": "868b6btbw",
        "date_created": "2024-12-05T15:01:32.305000+00:00",
        "date_done": None,
    },
]

df = pd.DataFrame(data)

df["date_created"] = pd.to_datetime(df["date_created"])

df["date_done"] = pd.to_datetime(df["date_done"], errors="coerce")

df["date_created_only"] = df["date_created"].dt.date

df["date_done_only"] = df["date_done"].dt.date

created_counts = df["date_created_only"].value_counts().sort_index()

done_counts = df["date_done_only"].value_counts().sort_index()

plt.figure(figsize=(10, 6))

plt.plot(
    created_counts.index, created_counts.values, label="Tareas Creadas", marker="o"
)

plt.plot(done_counts.index, done_counts.values, label="Tareas Completadas", marker="x")

plt.title("Tareas Creadas y Completadas por Día")

plt.xlabel("Fecha")

plt.ylabel("Número de Tareas")

plt.legend()

plt.xticks(rotation=45)

plt.grid(True)

plt.tight_layout()

plt.savefig("grafico_tareas_no_completadas.png", format="png")
