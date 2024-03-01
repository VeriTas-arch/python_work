from settings import Settings
import math
import numpy as np

set = Settings()


class Eva:
    """class for Evolutionary Algorithm (EVA)"""

    def __init__(self):
        self.max_fitness = 0
        self.best_ind = []


node_num = set.length
POP_SIZE = set.POP_SIZE
DNA_SIZE = set.DNA_SIZE
MUTATION_RATE = set.MUTATION_RATE


def fillBits(size):
    return 1 << size - 1


def target_function():
    """set sine function as target function"""
    # define the constants
    blen = set.beam_length
    sep_x = (set.screen_width - (set.row_lenh - 1) * blen * math.sqrt(3))/2
    sep_y = (set.screen_height - ((set.row_num - 1)/2) * blen)/2

    # define the sine function related parameters
    T = set.beam_length * 2 * math.sqrt(3) * 1.02
    omiga = 2 * math.pi / T
    Amp = set.beam_length / 25
    # bias = set.beam_length * 0.65
    bias = set.screen_height - sep_y + 7
    return lambda x: Amp * math.sin(omiga * (x - sep_x) + math.pi/2) + bias


def avoid_function_lin():
    """set the function that the input nodes should avoid"""
    # type1 linear function
    sep_y = (set.screen_height - ((set.row_num - 1)/2) * set.beam_length)/2
    Amp = set.beam_length / 2
    bias = Amp / 3
    return lambda x: sep_y + bias


def avoid_function_sin():
    """set the function that the input nodes should avoid"""
    # type2 sine function
    T = set.screen_width
    omiga = 2 * math.pi / T
    Amp = set.beam_length / 2
    bias = Amp / 4
    return lambda x: Amp * math.sin(omiga * x + math.pi) + bias


def get_fitness(indPos):
    """calculate the fitness of a certain individual"""
    target = target_function()
    # avoid = avoid_function_sin()
    length = set.row_lenh
    num  = node_num - 1
    # sum_input = 0
    sum_output = 0

    for i in range(length):
        # bias_in = (avoid(indPos[i][0]) - indPos[i][1]) ** 2
        # print(f"node {num - i - 1} position: {indPos[num - i - 1]}")
        # print(f"target {num - i - 1}: {target(indPos[num - i - 1][0])}")
        # print(f"reference position: {indPos[7]}")

        bias_out = (target(indPos[num - i][0]) - indPos[num - i][1]) ** 2
        sum_output += bias_out

    rms_out = math.sqrt(sum_output / length)
    fitness = 1 / (math.exp(rms_out) + 1)

    return fitness


def select_parent(pop, fitness):
    """choose the parent based on fitness"""
    index = np.random.choice(POP_SIZE, size=POP_SIZE, replace=True, p=fitness / sum(fitness))
    temp = [pop[index[i]] for i in range(POP_SIZE)]

    return temp


def crossover(pop, parent):
    """crossover the parents to generate offspring"""
    # choose an individual from the population to crossover
    index = np.random.randint(0, POP_SIZE - 1)
    # choose a crossover point
    point = np.random.randint(1, DNA_SIZE - 1)
    crossover_result = [np.concatenate((parent[i][:point], pop[index][i][point:])) for i in range(node_num)]

    return crossover_result


def mutate(child):
    """mutation operator"""
    child = np.array(child)
    interval = np.max(child) - np.min(child)

    # mutation process
    for i in range(DNA_SIZE):
        if np.random.rand() < MUTATION_RATE:
            point = i
            child = point + interval / (1 + child) + point * np.random.rand(node_num, node_num)

    return child


def process(pop, parent):
    """process the population with crossover and mutation"""
    offspring = crossover(pop, parent)
    offspring = mutate(offspring)

    return offspring