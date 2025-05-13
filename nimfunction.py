def selfish_moves(piles): #selfish bot moves
    max_index = piles.index(max(piles))
    taken = piles[max_index]
    piles[max_index] = 0
    return taken
def scoring_nim_dp(max_size, bonus):
    G = [[[0]*(max_size+1) for _ in range(max_size+1)]
                              for _ in range(max_size+1)]
    for a in range(max_size+1):
        for b in range(max_size+1):
            for c in range(max_size+1):
                if a==0 and b==0 and c==0:
                    continue
                best = float('-inf')
                for i, pile in enumerate((a, b, c)):
                    for m in range(1, pile+1):
                        na, nb, nc = a, b, c
                        if   i==0: na -= m
                        elif i==1: nb -= m
                        else:      nc -= m

                        val = m - G[na][nb][nc]
                        if na + nb + nc == 0:
                            val += bonus
                        best = max(best, val)

                G[a][b][c] = best
    return G

def best_move(a, b, c, G, bonus):
    target = G[a][b][c]
    for i, pile in enumerate((a, b, c)):
        for m in range(1, pile + 1):
            na, nb, nc = a, b, c
            if   i==0: na -= m
            elif i==1: nb -= m
            else:      nc -= m

            val = m - G[na][nb][nc]
            if na + nb + nc == 0:
                val += bonus
            if val == target:
                return i, m