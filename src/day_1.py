def get_fuel_cost(mass):
    return (mass // 3) - 2


def get_recursive_fuel_cost(mass):
    additional_mass = get_fuel_cost(mass)
    total_mass = 0

    while additional_mass > 0:
        total_mass += additional_mass
        additional_mass = get_fuel_cost(additional_mass)

    return total_mass

if __name__ == "__main__":
    with open('../input/day_1.in') as f:
        mass = list(map(int, f))
    
    fuel_costs = map(get_fuel_cost, mass)
    print(sum(fuel_costs))

    module_and_fuel_costs = map(get_recursive_fuel_cost, mass)
    print(sum(module_and_fuel_costs))
