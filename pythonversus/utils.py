def elo_to_rank(elo: float) -> str:
    # Convert elo to int
    elo = int(elo)
    ranks = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Masters"]
    divisions = ["5", "4", "3", "2", "1"]

    if elo < 0:
        return "Invalid Elo"
    elif elo < 400:
        return "Unranked"
    elif elo >= 2900:
        return "Masters 1"
    elif elo >= 2500:
        masters_division = min(5, max(1, 5 - (elo - 2500) // 100))
        return f"Masters {masters_division}"

    rank_index = min(4, elo // 500)
    division_index = (elo % 500) // 100

    return f"{ranks[rank_index]} {divisions[division_index]}"
