import sys, os

import random


def main(*args, **kwargs):
    # Inputs

    # Locking countries: you can either make it exclusive in the player list or in the locking country dict

    # locking country
    # players = [("Katta", "Italy"), "Sharon", "Florian", "Carolina", "Sudo", "Tim", "Michael"]
    players = ["Katta", "Sharon", "Florian", "Carolina", "Sudo", "Tim", "Michael"]
    countries = [
        "Sweden",
        "Ukraine",
        "Germany",
        "Luxembourg",
        "Lithuania",
        "Spain",
        "Estonia",
        "Ireland",
        "Latvia",
        "Greece",
        "United Kingdom",
        "Norway",
        "Italy",
        "Serbia",
        "Finland",
        "Portugal",
        "Armenia",
        "Cyprus",
        "Switzerland",
        "Slovenia",
        "Croatia",
        "Georgia",
        "France",
        "Austria",
    ]

    # non exclusive locking
    # locked_countries = {"italy": ["katta"]}
    locked_countries = {}
    remove_rest = False
    rescale_prizes = True

    ticket = 10

    # code
    players = sanitize_players(players)
    countries = sanitize_countries(countries)
    assert len(players) < len(countries)

    ans = distribute_countries(
        players, countries, ticket, locked_countries, remove_rest, rescale_prizes
    )

    print(ans)


def compute_prizes(ticket_price, np, nc, remove_rest, rescale_prizes):
    total = ticket_price * np
    if remove_rest or not rescale_prizes:
        return total, None, None, None
    n = int(nc / np)

    lucky_prize = total * n / (n + 1)
    payback = (total - lucky_prize) / (np - 1)
    return total, lucky_prize, payback, n


def print_correct_prize(
    total, lucky_prize, payback, npc, n, remove_rest, rescale_prizes
):
    if not remove_rest and rescale_prizes:
        if npc > n:
            return f". Price: {lucky_prize}, payback: {round(payback*100)/100}"
    return f". Prize: {total}"


def sanitize_players(players):
    ans = [
        (i.lower(), None) if isinstance(i, str) else (i[0].lower(), i[1].lower())
        for i in players
    ]
    assert len(players) == len(set([i[0] for i in ans]))
    return ans


def sanitize_countries(countries):
    return list(set(i.lower() for i in countries))


def distribute_countries(
    players, countries, ticket, locked_countries, remove_rest, rescale_prizes
):
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

        if i < n_lucky and not remove_rest:
            l += 1
        ans[i][1].extend(unassigned_countries[j : j + l])
        j += l

    total, lucky_prize, payback, n = compute_prizes(
        ticket,
        len(players),
        len(countries),
        remove_rest=remove_rest,
        rescale_prizes=rescale_prizes,
    )

    s = "\n".join(
        f"{i[0]}: "
        + ", ".join(j for j in i[1])
        + print_correct_prize(
            total, lucky_prize, payback, len(i[1]), n, remove_rest, rescale_prizes
        )
        for i in ans
    )

    s += "\n" + ", ".join(unassigned_countries[j:])
    return s


if __name__ == "__main__":
    main()
