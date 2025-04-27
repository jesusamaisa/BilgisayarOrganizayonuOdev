def parse_instruction(instr):
    """
    Bir RISC-V instruction'ı alır, hangi registera yazıyor (dest) ve hangi registerları okuyor (sources) bulur.
    """
    parts = instr.replace(",", "").split()
    op = parts[0]  # İşlem türü (addi, sub, vs.)

    if op in ["addi", "sub"]:
        dest = parts[1]     # Hedef register
        src1 = parts[2]     # Kaynak 1
        # addi sabit eklediği için src2 yok, sub'da da gerek yok burada
        return dest, [src1]

    else:
        return None, []  # Bilmediğimiz bir işlemse boş döneriz



# Core Programları
program_core1 = [
    "addi x1, x0, 5",
    "addi x2, x1, 3",
    "sub x3, x2, x1"
]

program_core2 = [
    "addi x5, x0, 10",
    "sub x6, x5, x0",
    "addi x7, x6, 2"
]

# Pipeline aşamaları
pipeline_stages = ["Fetch", "Decode", "Execute", "Memory", "Writeback"]

# Her çekirdek için pipeline durumları (instruction, stage)
core1_pipeline = []
core2_pipeline = []

# Kaçıncı instructiondayız
core1_pc = 0
core2_pc = 0

# Toplam cycle sayacı
cycle = 1

print("Çok Çekirdekli Pipeline Simülasyonu Başlıyor...\n")

# Simülasyonu başlat
while core1_pc < len(program_core1) or core2_pc < len(program_core2) or core1_pipeline or core2_pipeline:
    print(f"--- Cycle {cycle} ---")

    # --- Core 1 için Fetch ---
    stall_core1 = False

    if core1_pc < len(program_core1):
        # Fetch etmeye çalıştığımız instruction
        next_instr = program_core1[core1_pc]
        next_dest, next_sources = parse_instruction(next_instr)

        if core1_pipeline:
            last_instr, last_stage = core1_pipeline[-1]
            last_dest, _ = parse_instruction(last_instr)

            # Eğer önceki instruction'ın yazdığı registerı yeni instruction okuyorsa → Stall
            if last_dest and any(src == last_dest for src in next_sources):
                stall_core1 = True

        if not stall_core1:
            core1_pipeline.append((next_instr, 0))  # Fetch
            core1_pc += 1

    # --- Core 2 için Fetch ---
    stall_core2 = False

    if core2_pc < len(program_core2):
        next_instr = program_core2[core2_pc]
        next_dest, next_sources = parse_instruction(next_instr)

        if core2_pipeline:
            last_instr, last_stage = core2_pipeline[-1]
            last_dest, _ = parse_instruction(last_instr)

            if last_dest and any(src == last_dest for src in next_sources):
                stall_core2 = True

        if not stall_core2:
            core2_pipeline.append((next_instr, 0))  # Fetch
            core2_pc += 1


    # Çekirdeklerin pipeline'ını çiz
    def draw_pipeline(core_pipeline, stall=False):
        result = ""
        active_stages = ["       "] * 5  # 5 aşama boş

        for instr, stage_idx in core_pipeline:
            if stage_idx < 5:
                active_stages[stage_idx] = pipeline_stages[stage_idx][:7]  # "Fetch", "Decode", vb.

        if stall:
            # Eğer bu cycle'da stall varsa Fetch aşamasına STALL yaz
            active_stages[0] = "STALL"

        for stage in active_stages:
            result += f"[{stage.center(7)}] -> "
        return result[:-4]  # sondaki "-> " sil


    print(f"Core 1: {draw_pipeline(core1_pipeline, stall_core1)}")
    print(f"Core 2: {draw_pipeline(core2_pipeline, stall_core2)}")

    # Pipeline'daki her instruction'ı bir aşama ilerlet
    for idx in range(len(core1_pipeline)):
        core1_pipeline[idx] = (core1_pipeline[idx][0], core1_pipeline[idx][1] + 1)

    for idx in range(len(core2_pipeline)):
        core2_pipeline[idx] = (core2_pipeline[idx][0], core2_pipeline[idx][1] + 1)

    # Writeback sonrası tamamlanan instruction'ı çıkar
    core1_pipeline = [instr for instr in core1_pipeline if instr[1] < 5]
    core2_pipeline = [instr for instr in core2_pipeline if instr[1] < 5]

    cycle += 1
    print()

    # İstatistikleri hesapla
    core1_total_instructions = len(program_core1)
    core2_total_instructions = len(program_core2)

    core1_total_cycles = cycle - 1
    core2_total_cycles = cycle - 1

    core1_ipc = core1_total_instructions / core1_total_cycles
    core2_ipc = core2_total_instructions / core2_total_cycles

    print("Simülasyon bitti.\n")

    print("------ Sonuçlar ------")
    print(f"Core 1:")
    print(f" - Toplam Instruction: {core1_total_instructions}")
    print(f" - Toplam Cycle: {core1_total_cycles}")
    print(f" - IPC (Instruction per Cycle): {core1_ipc:.3f}\n")

    print(f"Core 2:")
    print(f" - Toplam Instruction: {core2_total_instructions}")
    print(f" - Toplam Cycle: {core2_total_cycles}")
    print(f" - IPC (Instruction per Cycle): {core2_ipc:.3f}")

print("Simülasyon bitti.")
