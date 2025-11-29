def map_attack_label_to_risk(label: str) -> str:
    if label is None:
        return "LOW"

    l = str(label).lower()

    # HIGH risk attacks
    high_keywords = ["dos", "ddos", "bruteforce", "sql", "infiltration", "xss", "bot", "heartbleed"]
    # MEDIUM risk (scans, suspicious)
    med_keywords = ["portscan", "scan", "ftp", "ssh", "suspicious"]
    # LOW risk (normal or benign)
    low_keywords = ["normal", "benign"]

    for kw in high_keywords:
        if kw in l:
            return "HIGH"
    for kw in med_keywords:
        if kw in l:
            return "MEDIUM"
    for kw in low_keywords:
        if kw in l:
            return "LOW"

    return "LOW"
