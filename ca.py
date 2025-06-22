import numpy as np

def evolve(state, rule, radius, size):
    """
    Evolves a 1D cellular automaton state based on the given rule and neighborhood radius.

    Parameters:
    - state (list or iterable): The current state of the automaton as a sequence of 0s and 1s.
    - rule (dict): A dictionary mapping binary neighborhood strings (e.g., '111', '010') to output values (0 or 1).
    - radius (int): The radius of the neighborhood to consider on each side of a cell.
    - size (int): The size of the automaton (number of cells).

    Returns:
    - list: The next state of the automaton after applying the rule.
    """

    # Handle changes in lattice size either crop the existing or pad with 0s
    if len(state) > size:
        state = list(state)[:size]
    elif len(state) < size:
        state = list(state)+([0] * (size-len(state)))
    else:
        state = list(state)

    # Initialize empty new state
    next_state = [0 for _ in range(size)]

    # Compute next state
    for i in range(len(state)):

        # Get neighbohood
        if i < radius:
            # Left edge handling
            neighborhood = state[-(radius-i):] + state[:i+radius+1]
        elif i>size-radius-1:
            # Right edge handling
            neighborhood = state[i-radius:] + state[:(i+radius)%size+1]
        else:
            neighborhood = state[i-radius:i+radius+1]

        # Apply rule by referencing the rule dictionary
        next_state[i] = rule[''.join(str(x) for x in neighborhood)]

    return next_state

