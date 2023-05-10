import sys, os

import random


def main(*args, **kwargs):
    # Inputs
    players = [("Katta", "Italy"), ("Sharon", "UK"), "florian", ("michael", "UK")]
    countries = ["Italy", "UK", "france", "finland", "sweden", "ireland", "spain"]
    ticket_price = 10

    # code
    players = sanitize_players(players)
    countries = sanitize_countries(countries)
    assert len(players) < len(countries)

    ans = distribute_countries(players, countries, ticket_price)

    print(ans)


def compute_prices(ticket_price, np, nc):
    total = ticket_price * np

    n = int(nc / np)

    lucky_price = total * n / (n + 1)
    payback = (total - lucky_price) / (np - 1)
    return total, lucky_price, payback, n


def print_correct_price(total, lucky_price, payback, n, npc):
    if npc > n:
        return f". Price: {lucky_price}, payback: {round(payback*100)/100}"
    return f". Price: {total}"


def sanitize_players(players):
    ans = [
        (i.lower(), None) if isinstance(i, str) else (i[0].lower(), i[1].lower())
        for i in players
    ]
    assert len(players) == len(set([i[0] for i in ans]))
    return ans


def sanitize_countries(countries):
    return list(set(i.lower() for i in countries))


def distribute_countries(players, countries, ticket_price):
    locked_countries = {}
    for player, country in players:
        if country and country in countries:
            if country in locked_countries:
                locked_countries[country].append(player)
            else:
                locked_countries[country] = [player]

    ans = {player: [] for player, _ in players}
    for country, l in locked_countries.items():
        player = random.choice(l)
        ans[player] = [country]

    ans = [[k, v] for k, v in ans.items()]
    random.shuffle(ans)

    unassigned_countries = [
        country for country in countries if country not in locked_countries
    ]
    random.shuffle(unassigned_countries)

    n_lucky = len(countries) % len(players)
    base = int(len(countries) / len(players))

    j = 0
    for i in range(len(ans)):
        l = base - len(ans[i][1])
        if i < n_lucky:
            l += 1
        ans[i][1].extend(unassigned_countries[j : j + l])
        j += l

    total, lucky_price, payback, n = compute_prices(
        ticket_price, len(players), len(countries)
    )

    return "\n".join(
        f"{i[0]}: "
        + ", ".join(j for j in i[1])
        + print_correct_price(total, lucky_price, payback, n, len(i[1]))
        for i in ans
    )


if __name__ == "__main__":
    main()
