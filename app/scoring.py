def score_opportunity(source: str, opp_type: str, title: str, url: str, meta: dict) -> float:
    t = (title or "").lower()
    score = 40.0

    # Testnet boost
    if opp_type == "testnet":
        score += 30

        if meta.get("token_found") is False:
            score += 25

        if meta.get("funding_detected") is True:
            score += 20

    # Funding boost
    if opp_type == "funding":
        score += 20

    # Generic keywords
    if any(k in t for k in ["airdrop", "retroactive", "incentive", "points"]):
        score += 15

    # Noise penalty
    if any(k in t for k in ["etf", "sec approval", "regulated", "tokenized mmes"]):
        score -= 30

    return float(max(0.0, min(100.0, score)))