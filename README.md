# Algoritmo Genético

En esta tarea se resolvió el problema n-queen, el cual consiste en ubicar n reinas en un tablero de
ajedrez de nxn, de modo que ninguna ataque a otra, dicho en otras palabras, que en una determinada
fila, columna o diagonal se encuentre a lo más una reina.

En los problemas de secuencias binarias y normales, los miembros de una población se modelaron
como strings, es decir cada caracter es un gen. En ambos casos la función de fitness compara letra
a letra la palabra generada(un individuo) con la previamente establecida como variable local y va
sumando uno a un contador por cada coincidencia. Se halla la solución cuando el contador es
igual al largo de la palabra secreta.
