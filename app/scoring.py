def score_opportunity(source: str, opp_type: str, title: str, url: str, meta: dict) -> float:
    t = (title or "").lower()

    score = 40.0  # baseline

    # Keywords (MVP heuristic)
    if any(k in t for k in ["airdrop", "retroactive", "incentive", "rewards", "campaign"]):
        score += 30
    if any(k in t for k in ["testnet", "alpha", "beta", "devnet"]):
        score += 20
    if any(k in t for k in ["grant", "hackathon", "bounty"]):
        score += 20
    if any(k in t for k in ["governance", "snapshot", "proposal"]):
        score += 10
    if any(k in t for k in ["launch", "tge", "token generation", "vesting", "unlock"]):
        score += 10

    # Source bias (very light)
    if source == "github" and opp_type == "release":
        score += 5

    # Clamp
    if score > 100:
        score = 100.0
    if score < 0:
        score = 0.0

    return float(score)