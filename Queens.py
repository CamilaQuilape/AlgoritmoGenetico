import random
import math
import matplotlib.pyplot as plt

def fitness(member):
    sizeMember = len(member)
    counter = sizeMember # Contador, si se mantiene en sizeMember se encontró la solución
    options = list(range(sizeMember))
    # Se revisan las columnas
    for i in options:
        value = member.count(i)
        if value > 1:
            counter -= int((value*(value-1))/2)

    # Se revisan las diagonales
    for i in range(sizeMember - 1):
        for j in range(i+1,sizeMember):
            module = abs(member[i] - member[j])
            if module == abs(i - j):
                counter -= 1

    return counter

class Queens:

    def __init__(self,n,size,ffitness):
        self.n = n # Tamaño de la población
        self.size = size # Tamaño del tablero
        self.fitness = ffitness # Función de fitness
        self.population = [] # Población
        self.fitnessPopulation = [] # Fitness de los individuos
        self.solution = [] # Posiciones de las reinas
        self.solutionFound = False
        self.numberGenerations = 0 # Número de generaciones
        self.options = list(range(self.size)) # Lista de opciones que puede tomar el valor de cada gen
        self.fitnessMean = [] # Almacenará los fitness promedio por población
        self.fitnessMaximum = [] # Almacenará los fitness máximos por población

    def initialize(self):
        for i in range(self.n):
            member = []
            for j in range(self.size):
                # Cada gen se elige al azar desde self.options
                member.append(random.choice(self.options))
            self.population.append(member)
        self.fitnessPopulation = self.applyFitness(self.population)
        self.fitnessMaximum.append(max(self.fitnessPopulation))
        self.fitnessMean.append(self.mean(self.fitnessPopulation))

    def applyFitness(self, population):
        # Calcula el fitness de cada miembro de population y retorna una lista con los resultados
        listFitness = []
        for member in population:
            fit = self.fitness(member)
            listFitness.append(fit)
            if fit == self.size: # Si ninguna reina ataca a otra
                self.solutionFound = True
                self.solution = member
        return listFitness

    def tournament(self,population,listFitness,k):
        best = -1  # Inicialización
        for i in range(k):
            ind = random.randint(0, self.n - 1) # Índice aleatorio
            if best == -1 or listFitness[ind] > listFitness[best]:
                best = ind
        return population[best]

    def reproduce(self,population,listFitness):
        participants = (3 * self.n) // 4 # El 75% de la población
        divider = 100 // self.size # Es el largo de los intervalos
        # Por ejemplo si se trabajan con seis genes, divider es 16
        newPopulation = []
        i = 0
        while i < self.n:
            parent1 = self.tournament(population,listFitness,participants)
            parent2 = self.tournament(population,listFitness,participants)
            # Se divide el número aleatorio en el largo del intervalo y se le aplica techo
            mixingPoint = math.ceil(random.randint(0, 100) / divider)
            child = parent1[:mixingPoint] + parent2[mixingPoint:]
            for j in range(self.size):
                mutationRate = random.random()
                if mutationRate < 0.1: # Si esto ocurre, se cambia el gen por otro
                    copy = self.options.copy()
                    copy.remove(child[j])
                    child[j] = random.choice(copy) # Se elige un número distinto al actual
            newPopulation.append(child)
            i += 1
        return newPopulation

    def reproducePopulation(self):
        newGeneration = self.population
        fitnessNewGeneration = self.fitnessPopulation
        while not self.solutionFound:
            newGeneration = self.reproduce(newGeneration,fitnessNewGeneration)
            fitnessNewGeneration = self.applyFitness(newGeneration)
            self.fitnessMaximum.append(max(fitnessNewGeneration))
            self.fitnessMean.append(self.mean(fitnessNewGeneration))
            self.numberGenerations += 1
        return self.solution

    def numberOfGenerations(self):
        return self.numberGenerations

    def mean(self,listFitness):
        summation = sum(listFitness)
        m = summation/self.n
        return m

    def graphFitnessMean(self):
        plt.plot(range(self.numberGenerations+1),self.fitnessMean, marker = 'o')
        plt.title('Fitness promedio por generación, incluyendo el de la población inicial')
        plt.xlabel('Datos' + '\n' + 'Tamaño de la población: ' + str(self.n) + ', Cantidad de generaciones: ' + str(self.numberGenerations) + '\n'
                   + 'Tamaño del tablero: ' + str(self.size))
        plt.ylabel('Fitness promedio')
        plt.show()

    def graphFitnessMaximum(self):
        plt.plot(range(self.numberGenerations+1),self.fitnessMaximum, marker = 'o')
        plt.title('Fitness máximo por generación, incluyendo el de la población inicial')
        plt.xlabel('Datos' + '\n' + 'Tamaño de la población: ' + str(self.n) + ', Cantidad de generaciones: ' + str(self.numberGenerations) + '\n'
                   + 'Tamaño del tablero: ' + str(self.size))
        plt.ylabel('Fitness máximo')
        plt.show()


def main():
    n = 300
    algoritmo = Queens(n, 8, fitness)
    algoritmo.initialize()
    palabrasecreta = algoritmo.reproducePopulation()
    numGeneraciones = algoritmo.numberOfGenerations()
    algoritmo.graphFitnessMean()
    algoritmo.graphFitnessMaximum()
    print(palabrasecreta)
    print(numGeneraciones)


main()

