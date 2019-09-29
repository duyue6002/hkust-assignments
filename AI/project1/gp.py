import pandas as pd
import numpy as np
import os

M = 5000
N = 9
pc = 0.9
pm = 0.9
iteration_times = 1000

random_data = np.random.uniform(-4, 4, size=(M, N+1))
initial_pop = random_data[:, :9]
theta = random_data[:, 9]

script_dir = os.path.dirname(__file__)
file_name = 'gp-training-set.csv'
file_path = os.path.join(script_dir, file_name)
df = pd.read_csv('gp-training-set.csv', header=None)
data = np.array(df.iloc[:, :])
X_train, D_train = data[:, :-1], data[:, -1]
data_scale = len(X_train)


def fitness_function(pop):
    fitness = []
    for i in range(len(pop)):
        fitness_value = 0
        for j in range(len(X_train)):
            x = X_train[j]
            d = D_train[j]
            output = 1 if (np.dot(x, pop[i]) >= theta[i]) else 0
            if d == output:
                fitness_value += 1
        fitness.append(fitness_value)
    return fitness


def copy(fitness, pop):
    arr = np.argsort(fitness)[::-1]
    select_pop = np.zeros((M/2, N))
    for i in range(len(arr)/2):
        select_pop[i] = pop[arr[i]]
    return select_pop


def crossover(pc, pop):
    crossover_pop = pop.copy()
    for i in range(len(pop)-1):
        if (np.random.rand() < pc):
            j = int(np.random.rand()*(N))
            crossover_pop[i, j:] = pop[i+1, j:]
    return crossover_pop


def mutation(pm, pop):
    mutation_pop = pop.copy()
    for i in range(len(mutation_pop)):
        if (np.random.rand() < pm):
            j = int(np.random.rand()*(N))
            mutation_pop[i, j] = pop[i, j] + np.random.uniform(-1, 1)
    return mutation_pop


def generation(iteration_times, pop):
    result_pop = np.zeros(N)
    max_data = 0
    result_index = 0
    for i in range(iteration_times):
        fitness = fitness_function(pop)
        if max(fitness) > max_data:
            max_data = max(fitness)
            result_index = fitness.index(max_data)
            result_pop = pop[result_index]
            if max_data == data_scale:
                return [result_pop, result_index, i]
        else:
            select_pop = copy(fitness, pop)
            crossover_pop = crossover(pc, select_pop)
            mutation_pop = mutation(pm, crossover_pop)
            length = len(pop)
            pop[0:length/2] = select_pop[:]
            pop[length/2:length] = mutation_pop[:]
    return [result_pop, result_index, iteration_times]


if __name__ == "__main__":
    [w, index, generation_times] = generation(iteration_times, initial_pop)
    wrong_count = 0
    for i in range(len(X_train)):
        x = X_train[i]
        d = D_train[i]
        output = 1 if (np.dot(x, w) >= theta[index]) else 0
        if d != output:
            wrong_count += 1
    print [w, theta[index], generation_times] if wrong_count == 0 else 'failed'
