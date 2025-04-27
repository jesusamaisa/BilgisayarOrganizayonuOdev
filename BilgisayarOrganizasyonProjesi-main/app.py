from flask import Flask, jsonify, render_template, request

app = Flask(__name__, template_folder="templates")

# Pipeline aşamaları
pipeline_stages = ["Fetch", "Decode", "Execute", "Memory", "Writeback"]

# Örnek instruction havuzu
instruction_pool = [
    "addi x1, x0, 5",
    "addi x2, x1, 3",
    "sub x3, x2, x1",
    "addi x5, x0, 10",
    "sub x6, x5, x0",
    "addi x7, x6, 2",
    "addi x8, x7, 1",
    "sub x9, x8, x2"
]

# Instruction'dan hedef ve kaynak register çıkarma
def parse_instruction(instr):
    parts = instr.replace(",", "").split()
    op = parts[0]
    if op in ["addi", "sub"]:
        dest = parts[1]
        src1 = parts[2]
        return dest, [src1]
    else:
        return None, []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/simulate')
def simulate_pipeline():
    # Kullanıcının seçtiği çekirdek sayısını alıyoruz
    core_count = int(request.args.get('cores', 2))  # default 2 core

    # Çekirdek başına birer küçük program atayalım
    programs = {}
    for core_num in range(1, core_count + 1):
        programs[f"core{core_num}"] = instruction_pool[(core_num-1)%len(instruction_pool):][:3]

    # Pipeline verileri
    pipelines = {core: [] for core in programs}
    program_counters = {core: 0 for core in programs}
    cycle = 1
    result_cycles = []

    while any(pc < len(programs[core]) or pipelines[core] for core, pc in program_counters.items()):
        cycle_info = {"cycle": cycle}

        for core in programs:
            stall = False

            # Fetch aşaması
            if program_counters[core] < len(programs[core]):
                next_instr = programs[core][program_counters[core]]
                next_dest, next_sources = parse_instruction(next_instr)

                if pipelines[core]:
                    last_instr, last_stage = pipelines[core][-1]
                    last_dest, _ = parse_instruction(last_instr)
                    if last_dest and any(src == last_dest for src in next_sources):
                        stall = True

                if not stall:
                    pipelines[core].append((next_instr, 0))
                    program_counters[core] += 1

            # Pipeline aşamalarını hazırla
            stages = [""] * 5
            for instr, stage_idx in pipelines[core]:
                if stage_idx < 5:
                    stages[stage_idx] = pipeline_stages[stage_idx]

            if stall:
                stages[0] = "STALL"

            cycle_info[core] = stages

        result_cycles.append(cycle_info)

        # Aşamaları ilerlet
        for core in pipelines:
            for idx in range(len(pipelines[core])):
                pipelines[core][idx] = (pipelines[core][idx][0], pipelines[core][idx][1] + 1)

        # Writeback aşaması bitenleri çıkar
        for core in pipelines:
            pipelines[core] = [instr for instr in pipelines[core] if instr[1] < 5]

        cycle += 1

    return jsonify({"cycles": result_cycles})

if __name__ == '__main__':
    app.run(debug=True)
