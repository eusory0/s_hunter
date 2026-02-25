def score_opportunity(source: str, opp_type: str, title: str, url: str, meta: dict) -> float:
    t = (title or "").lower()
    score = 40.0  # baseline

    # Generic keywords
    if any(k in t for k in ["airdrop", "retroactive", "incentive", "rewards", "campaign"]):
        score += 30
    if any(k in t for k in ["testnet", "alpha", "beta", "devnet"]):
        score += 20
    if any(k in t for k in ["grant", "hackathon", "bounty"]):
        score += 20
    if any(k in t for k in ["governance", "snapshot", "proposal"]):
        score += 10

    # Funding-specific boost
    if opp_type == "funding":
        score += 25
        # Tokenless = foarte valoros pentru airdrop probability
        if meta.get("token_found") is False:
            score += 25

    # Light source bias
    if source == "github" and opp_type == "release":
        score += 5

    return float(max(0.0, min(100.0, score)))