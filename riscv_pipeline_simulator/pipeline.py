def simulate_pipeline(commands):
    result = []
    for i, cmd in enumerate(commands):
        stages = [
            ("IF", i + 1),
            ("ID", i + 2),
            ("EX", i + 3),
            ("MEM", i + 4),
            ("WB", i + 5)
        ]
        result.append({"instruction": cmd, "stages": stages})
    return result