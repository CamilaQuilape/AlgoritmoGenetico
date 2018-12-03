import random
import math
import matplotlib.pyplot as plt

def fitness(palabra):
    palabra_secreta = "computador"
    tam = len(palabra_secreta)
    letrasCorrectas = 0
    for i in range(tam):
        if palabra[i] == palabra_secreta[i]:
            letrasCorrectas += 1
    return letrasCorrectas

class AlgoritmoPalabra:

    def __init__(self,n,tamano,ffitness):
        self.n = n
        self.tam = tamano
        self.fitness = ffitness
        self.palabraSecreta = ""
        self.poblacion = []
        self.fitnessPoblacion = []
        self.palabraEncontrada = False
        self.numeroGeneraciones = 0
        self.alfabeto = "abcdefghijklmnñopqrstuvwxyz" # 27 letras
        self.fitnessMaximo = []

    def inicializar(self):
        for i in range(self.n):
            secuencia = ""
            for i in range(self.tam):
                secuencia += random.choice(self.alfabeto)
            self.poblacion.append(secuencia)
        self.fitnessPoblacion = self.aplicarFitness(self.poblacion)
        self.fitnessMaximo.append(max(self.fitnessPoblacion))

    def aplicarFitness(self, poblacion):
        listaFitness = []
        for secuencia in poblacion:
            fit = self.fitness(secuencia)
            listaFitness.append(fit)
            if fit == self.tam:
                self.palabraEncontrada = True
                self.palabraSecreta = secuencia
        return listaFitness

    def torneo(self,poblacion,listaFitness,k):
        mejor = -1  # Inicializacion
        for i in range(k):
            ind = random.randint(0, self.n - 1) # Índice aleatorio
            if mejor == -1 or listaFitness[ind] > listaFitness[mejor]:
                mejor = ind
        return poblacion[mejor]

    def reproducir(self,poblacion,listaFitness):
        participantes = (3 * self.n) // 4
        divisor = 100 // self.tam
        nuevaPoblacion = []
        i = 0
        while i < self.n:
            padre1 = self.torneo(poblacion,listaFitness,participantes)
            padre2 = self.torneo(poblacion,listaFitness,participantes)
            puntoMezcla = math.ceil(random.randint(0, 100) / divisor)
            hijo = padre1[:puntoMezcla] + padre2[puntoMezcla:]
            hijoMutado = ""
            for j in hijo:
                tasaMutacion = random.random()
                if tasaMutacion < 0.1:
                    hijoMutado += random.choice(self.alfabeto) # Puede dar el mismo
                else:
                    hijoMutado += j
            nuevaPoblacion.append(hijoMutado)
            i += 1
        return nuevaPoblacion

    def reproducirPoblacion(self):
        nuevaGeneracion = self.poblacion
        fitnessNuevaGeneracion = self.fitnessPoblacion
        while not self.palabraEncontrada:
            nuevaGeneracion = self.reproducir(nuevaGeneracion,fitnessNuevaGeneracion)
            fitnessNuevaGeneracion = self.aplicarFitness(nuevaGeneracion)
            self.fitnessMaximo.append(max(fitnessNuevaGeneracion))
            self.numeroGeneraciones += 1
        return self.palabraSecreta

    def cantidadGeneraciones(self):
        return self.numeroGeneraciones

    def graficarFitnessMaximo(self):
        plt.plot(range(self.numeroGeneraciones+1),self.fitnessMaximo, marker = 'o')
        plt.title('Fitness máximo por generación, incluyendo el de la población inicial')
        plt.xlabel('Tamaño de la población: ' + str(self.n) + ', Cantidad de generaciones: ' + str(self.numeroGeneraciones) + '\n'
                   + 'Largo de la palabra secreta: ' + str(self.tam))
        plt.show()

def main():
    n = 50
    algoritmo = AlgoritmoPalabra(n, 10, fitness)
    algoritmo.inicializar()
    palabraSecreta = algoritmo.reproducirPoblacion()
    numeroGeneraciones = algoritmo.cantidadGeneraciones()
    algoritmo.graficarFitnessMaximo()
    print(palabraSecreta)
    print(numeroGeneraciones)

main()