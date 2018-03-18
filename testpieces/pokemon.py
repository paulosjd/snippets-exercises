""" Take the following selection of 70 English Pokemon names and generate the/a sequence with the highest possible number
of Pokemon names where the subsequent name starts with the final letter of the preceding name. No Pokemon name is to
be repeated. """

names = 'audino bagon baltoy banette bidoof braviary bronzor carracosta charmeleon cresselia croagunk darmanitan ' \
        'deino emboar emolga exeggcute gabite girafarig gulpin haxorus heatmor heatran ivysaur jellicent jumpluff ' \
        'kangaskhan kricketune landorus ledyba loudred lumineon lunatone machamp magnezone mamoswine nosepass ' \
        'petilil pidgeotto pikachu pinsir poliwrath poochyena porygon2 porygonz registeel relicanth remoraid rufflet ' \
        'sableye scolipede scrafty seaking sealeo silcoon simisear snivy snorlax spoink starly tirtouga trapinch ' \
        'treecko tyrogue vigoroth vulpix wailord wartortle whismur wingull yamask'.split(' ')


def string_chain(pokemons):
    container = []
    n = 0
    for x in pokemons:
        pok = [pokemons[n]]
        for i in pokemons:
            if i[0] == pok[0][-1]:
                pok.append(i)
            break
        for a in pokemons:
            if a[0] == pok[-1][-1]:
                pok.append(a)
        n += 1
        container.append(pok)
    for a in container:
        if len(a) == max([len(a) for a in container]):
            return a


print(string_chain(names))
