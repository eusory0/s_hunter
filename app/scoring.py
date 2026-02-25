def score_opportunity(source: str, opp_type: str, title: str, url: str, meta: dict) -> float:
    t = (title or "").lower()
    score = 40.0

    # Noise penalty (enterprise/regulation)
    if any(k in t for k in ["etf", "sec", "approval", "wisdomtree", "wall street", "tokenized"]):
        score -= 30

    # Testnet is our main monetization signal
    if opp_type == "testnet":
        score += 30  # base testnet boost

        # tokenless = big deal (airdrop probability)
        if meta.get("token_found") is False:
            score += 25

        # extra keywords
        if any(k in t for k in ["points", "incentivized", "faucet"]):
            score += 10

        # optional cross-signals (for later)
        if meta.get("funding_detected") is True:
            score += 15

    # Funding (kept smaller than testnet for now)
    if opp_type == "funding":
        score += 15
        if meta.get("token_found") is False:
            score += 10

    # Small generic boosts
    if any(k in t for k in ["airdrop", "retroactive"]):
        score += 10

    return float(max(0.0, min(100.0, score)))