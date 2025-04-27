import matplotlib.pyplot as plt
import pandas as pd

# Örnek komut listesi ve her komutun aşama başlangıç zamanları
instructions = [
    {"name": "addi x1, x0, 5", "stages": [0, 1, 2, 3, 4]},
    {"name": "lw x2, 0(x1)",   "stages": [1, 2, 3, 4, 5]},
    {"name": "add x3, x1, x2", "stages": [2, 3, 4, 5, 6]},
    {"name": "sw x3, 0(x1)",   "stages": [3, 4, 5, 6, 7]},
    {"name": "beq x3, x0, label", "stages": [4, 5, 6, 7, 8]}
]

stage_labels = ['IF', 'ID', 'EX', 'MEM', 'WB']
colors = ['skyblue', 'lightgreen', 'salmon', 'plum', 'gold']

# DataFrame oluştur
data = []
for i, instr in enumerate(instructions):
    for j, stage_start in enumerate(instr['stages']):
        data.append({
            "Instruction": instr["name"],
            "Stage": stage_labels[j],
            "Start": stage_start,
            "Duration": 1,
            "Row": i
        })

df = pd.DataFrame(data)

# Görselleştirme
fig, ax = plt.subplots(figsize=(12, 6))

for i, row in df.iterrows():
    ax.broken_barh(
        [(row.Start, row.Duration)],
        (row.Row * 10, 9),
        facecolors=colors[stage_labels.index(row.Stage)],
        label=row.Stage if i < 5 else ""  # sadece ilk 5 için legend
    )
    ax.text(row.Start + 0.4, row.Row * 10 + 4, row.Stage, va='center', ha='center', fontsize=9)

# Ayarlar
ax.set_yticks([i * 10 + 4.5 for i in range(len(instructions))])
ax.set_yticklabels([instr["name"] for instr in instructions])
ax.set_xlabel("Clock Cycle")
ax.set_title("RISC-V 5 Aşamalı Pipeline Görselleştirmesi")
ax.grid(True)
ax.legend(loc='upper right')
plt.tight_layout()
plt.show()
