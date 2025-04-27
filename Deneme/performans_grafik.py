import matplotlib.pyplot as plt

# Örnek veriler — bunlar dinamik olarak simülasyondan gelecek
metrics = {
    "Toplam Clock Cycle": 120,
    "CPI": 2.4,
    "Stall Sayısı": 7,
    "Forwarding Sayısı": 12,
    "Branch Misprediction Sayısı": 3
}
    
def plot_performance(metrics):
    keys = list(metrics.keys())
    values = list(metrics.values())

    plt.figure(figsize=(10, 5))
    bars = plt.bar(keys, values, color=["steelblue", "darkorange", "green", "purple", "red"])
    plt.title("📊 Pipeline Performans Ölçümleri")
    plt.ylabel("Değer")
    plt.xticks(rotation=15)
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    # Bar üzerine değer yazdırma
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2.0, yval + 0.5, f'{yval}', ha='center', va='bottom')

    plt.tight_layout()
    plt.show()

# Fonksiyonu çalıştır
plot_performance(metrics)
