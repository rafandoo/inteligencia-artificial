import random
import itertools
import collections
import timeit

class No:
    """
    Uma classe que representa um no
    - 'puzzle' é uma instância de Puzzle
    - 'pai' é o no precedente gerado, se houver
    - 'acao' é a acao tomada para resolver o puzzle, se houver
    """
    def __init__(self, puzzle, pai=None, acao=None):
        self.puzzle = puzzle
        self.pai = pai
        self.acao = acao
        if (self.pai != None):
            self.g = pai.g + 1
        else:
            self.g = 0

    @property
    def estado(self):
        """
        Retorna uma representação hashable de self
        """
        return str(self)

    @property 
    def caminho(self):
        """
        Reconstrói um caminho a partir do nó raiz 'pai'
        """
        no, p = self, []
        while no:
            p.append(no)
            no = no.pai
        yield from reversed(p)

    @property
    def resolvido(self):
        """ Wrapper para verificar se 'puzzle' está resolvido """
        return self.puzzle.ehResolvido

    @property
    def acoes(self):
        """ Wrapper para 'acoes' acessíveis no estado atual """
        return self.puzzle.acoes

    def __str__(self):
        return str(self.puzzle)

class Solucionador:
    """
    Classe que soluciona o puzzle 8
    - 'start' é o puzzle inicial
    """
    def __init__(self, start):
        self.start = start

    def resolver(self):
        """
        Realiza busca em largura e retorna um caminho
        para a solução, se ela existir
        """
        fila = collections.deque([No(self.start)])
        vistos = set()
        vistos.add(fila[0].estado)
        cVistos = 0
        while fila:
            fila = collections.deque(sorted(list(fila), key=lambda no: no.g))
            no = fila.popleft()
            if no.resolvido:
                return no.caminho, cVistos

            for mover, acao in no.acoes:
                filho = No(mover(), no, acao)

                if filho.estado not in vistos:
                    fila.appendleft(filho)
                    vistos.add(filho.estado)
                    cVistos += 1

class Puzzle:
    """
    A classe Puzzle possui as seguintes propriedades:
    - 'tamanho' é o tamanho do puzzle
    - 'puzzle' é uma lista de listas que representa o puzzle
    
    EX: [[1,2,3],[4,0,6],[7,5,8]]
    """
    def __init__(self, puzzle):
        self.tamanho = len(puzzle[0])
        self.puzzle = puzzle

    @property
    def ehResolvido(self):
        """
        O puzzle ehResolvido se os numeros do puzzle estiverem em ordem 
        crescente da esquerda para a direita e o '0' estiver na ultima 
        posicao do puzzle
        """
        n = self.tamanho ** 2
        return str(self) == ''.join(map(str, range(1, n))) + '0'

    @property 
    def acoes(self):
        """
        Retorna uma lista de tuplas (mover, acao) onde mover eh uma 
        funcao que retorna um novo puzzle com o '0' movido na direcao 
        de acao
        """
        def criarMovimento(atual, novo):
            return lambda: self.mover(atual, novo)

        movimentos = []
        for i, j in itertools.product(range(self.tamanho), range(self.tamanho)):
            direcoes = {
                    'D':(i, j-1),
                    'E':(i, j+1),
                    'B':(i-1, j),
                    'C':(i+1, j)
                    }

            for acao, (x, y) in direcoes.items():
                if x >= 0 and y >= 0 and x < self.tamanho and y < self.tamanho and self.puzzle[x][y] == 0:
                    mover = criarMovimento((i,j), (x,y)), acao
                    movimentos.append(mover)
        return movimentos
    
    def embaralhar(self):
        """
        Retorna um novo puzzle que foi embaralhado com 1000 movimentos 
        aleatorios
        """
        puzzle = self
        for _ in range(1000):
            puzzle = random.choice(puzzle.acoes)[0]()
        return puzzle

    def copiar(self):
        """
        Retorna um novo puzzle com o mesmo puzzle que 'self'
        """
        puzzle = []
        for row in self.puzzle:
            puzzle.append([x for x in row])
        return Puzzle(puzzle)

    def mover(self, atual, novo):
        """
        Retorna um novo puzzle com o '0' movido de 'atual' para 'novo'
        """
        copia = self.copiar()
        i, j = atual
        x, y = novo
        copia.puzzle[i][j], copia.puzzle[x][y] = copia.puzzle[x][y], copia.puzzle[i][j]
        return copia

    def imprimePuzzle(self):
        """
        Impressao do puzzle
        """
        for row in self.puzzle:
            print(row)
        print()

    def __str__(self):
        return ''.join(map(str, self))

    def __iter__(self):
        for row in self.puzzle:
            yield from row



if __name__ == '__main__':
    
    # Definindo o puzzle
    puzzle = [[1,2,3],[4,5,0],[6,7,8]]
    puzzle = Puzzle(puzzle)
    
    # Embaralhando o puzzle
    # puzzle = puzzle.embaralhar()
    
    # Resolvendo o puzzle
    s = Solucionador(puzzle)
    inicio = timeit.default_timer()
    p, nos = s.resolver()
    fim = timeit.default_timer()

    # Imprimindo os passos para resolver o puzzle
    passos = 0
    for no in p:
        print(no.acao)
        no.puzzle.imprimePuzzle()
        passos += 1

    print("Numero de passos: {}".format(passos))
    print("Total de tempo para resolver: {} segundos".format(round(fim - inicio, 2)))
    print("Total de nos visitados: {}".format(nos))