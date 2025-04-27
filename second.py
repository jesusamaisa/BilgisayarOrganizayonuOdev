from flask import Flask, render_template, request, send_file
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

pipeline_stages = ["IF", "ID", "EX", "MEM", "WB"]

# Daha fazla RISC-V komutunun analizini destekle
# Basit RISC-V komutları: add, sub, lw, sw, beq, addi, and, or, xor, sll, srl, sra
def parse_registers(instr):
    instr = instr.replace(',', '')
    parts = instr.split()
    if not parts:
        return None, []
    opcode = parts[0]

    try:
        if opcode in ["add", "sub", "and", "or", "xor", "sll", "srl", "sra"]:
            return parts[1], [parts[2], parts[3]]
        elif opcode == "addi":
            return parts[1], [parts[2]]
        elif opcode == "lw":
            return parts[1], [parts[2].split('(')[1].strip(')')]
        elif opcode == "sw":
            return None, [parts[1], parts[2].split('(')[1].strip(')')]
        elif opcode == "beq":
            return None, [parts[1], parts[2]]
        else:
            return None, []
    except:
        return None, []

def simulate_pipeline(instructions):
    pipeline_matrix = []
    reg_write_history = {}
    current_cycle = 0

    for i, instr in enumerate(instructions):
        dest, sources = parse_registers(instr)
        stall_cycles = 0

        for src in sources:
            if src in reg_write_history:
                last_written_cycle = reg_write_history[src]
                if current_cycle < last_written_cycle + 2:
                    required_stall = (last_written_cycle + 2) - current_cycle
                    stall_cycles = max(stall_cycles, required_stall)

        row = ["NOP"] * stall_cycles + pipeline_stages.copy()
        pipeline_matrix.append(row)

        if dest:
            reg_write_history[dest] = current_cycle + stall_cycles + 4

        current_cycle += 1 + stall_cycles

    max_len = max(len(row) for row in pipeline_matrix)
    for row in pipeline_matrix:
        while len(row) < max_len:
            row.append("")

    return pipeline_matrix

def draw_pipeline(pipeline_matrix, instructions):
    fig, ax = plt.subplots(figsize=(16, 6))
    for i, row in enumerate(pipeline_matrix):
        for j, stage in enumerate(row):
            if stage:
                color = "khaki" if stage == "NOP" else "lightgreen"
                ax.text(j, -i, stage, ha='center', va='center',
                        bbox=dict(boxstyle='round', facecolor=color))
    ax.set_xlim(0, len(pipeline_matrix[0]))
    ax.set_ylim(-len(instructions), 1)
    ax.set_xticks(range(len(pipeline_matrix[0])))
    ax.set_yticks([-i for i in range(len(instructions))])
    ax.set_yticklabels(instructions)
    ax.grid(True)
    plt.title("RISC-V Pipeline Simülasyonu")
    plt.tight_layout()
    output_path = os.path.join("static", "pipeline.png")
    plt.savefig(output_path)
    plt.close()
    return output_path

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        raw_input = request.form["instructions"]
        instructions = [line.strip() for line in raw_input.strip().split("\n") if line.strip()]
        pipeline_matrix = simulate_pipeline(instructions)
        img_path = draw_pipeline(pipeline_matrix, instructions)
        return render_template("index.html", image_path=img_path, default_input=raw_input)
    return render_template("index.html", image_path=None, default_input="")

if __name__ == "__main__":
    app.run(debug=True)
