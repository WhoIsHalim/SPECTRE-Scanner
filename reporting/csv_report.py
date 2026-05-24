import csv


def save_csv(results, path="results.csv"):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        writer.writerow([
            "ip",
            "port",
            "title",
            "server"
        ])

        for r in results:
            writer.writerow([
                r.ip,
                r.port,
                r.http.title if r.http else "",
                r.http.server if r.http else ""
            ])