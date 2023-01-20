import requests
from enum import Enum
import heapq

# minimum cardinality bipartite - reference: https://tryalgo.org/en/matching/2016/08/05/konig/
def augment(u, bigraph, visit, match):
    for v in bigraph[u]:
        if not visit[v]:
            visit[v] = True
            if match[v] is None or augment(match[v], bigraph,
                                           visit, match):
                match[v] = u       # found an augmenting path
                return True
    return False


def max_bipartite_matching(bigraph):
    """Bipartie maximum matching

    :param bigraph: adjacency list, index = vertex in U,
                                    value = neighbor list in V
    :assumption: U = V = {0, 1, 2, ..., n - 1} for n = len(bigraph)
    :returns: matching list, match[v] == u iff (u, v) in matching
    :complexity: `O(|V|*|E|)`
    """
    n = len(bigraph)               # same domain for U and V
    match = [None] * n
    for u in range(n):
        augment(u, bigraph, [False] * n, match)
    return match


def alternate(u, bigraph, visitU, visitV, matchV):
    """extend alternating tree from free vertex u.
      visitU, visitV marks all vertices covered by the tree.
    """
    visitU[u] = True
    for v in bigraph[u]:
        if not visitV[v]:
            visitV[v] = True
            assert matchV[v] is not None   # otherwise match not maximum
            alternate(matchV[v], bigraph, visitU, visitV, matchV)


def koenig(bigraph):
    """Bipartie minimum vertex cover by Koenig's theorem

    :param bigraph: adjacency list, index = vertex in U,
                                    value = neighbor list in V
    :assumption: U = V = {0, 1, 2, ..., n - 1} for n = len(bigraph)
    :returns: boolean table for U, boolean table for V
    :comment: selected vertices form a minimum vertex cover,
              i.e. every edge is adjacent to at least one selected vertex
              and number of selected vertices is minimum
    :complexity: `O(|V|*|E|)`
    """
    V = range(len(bigraph))
    matchV = max_bipartite_matching(bigraph)
    matchU = [None for u in V]
    for v in V:                      # -- build the mapping from U to V
        if matchV[v] is not None:
            matchU[matchV[v]] = v
    visitU = [False for u in V]      # -- build max alternating forest
    visitV = [False for v in V]
    for u in V:
        if matchU[u] is None:        # -- starting with free vertices in U
            alternate(u, bigraph, visitU, visitV, matchV)
    inverse = [not b for b in visitU]
    return sum(inverse) + sum(visitV)


DOT = "."
class Move(Enum):
    # For each peg, the following ordering should be applied: left, down, right, up
    UP = 1
    RIGHT = 2
    DOWN = 3
    LEFT = 4

    def __lt__(self, other):
        return (self.value < other.value)


class Board:
    def __init__(self, tiles):
        self.tiles = [row[:] for row in tiles]

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return other.tiles == self.tiles
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def is_valid_tile(self, i, j):
        return i >= 0 and j >= 0 and i < len(self.tiles) and j < len(self.tiles[0])

    def is_goal(self):
        cnt = 0
        for row in self.tiles:
            for el in row:
                cnt = cnt + 1 if el != DOT else cnt
                if (cnt > 1):
                    return False
        return True


class Pair:
    def __init__(self, State, priority):
        self.State = State
        self.priority = priority

    def __lt__(self, other):
        this = self.State
        that = other.State

        if (this.f() != that.f()):
            return this.f() < that.f()
        elif (this.explanation[0] != that.explanation[0]):   # pegs
            return this.explanation[0] < that.explanation[0]
        elif (this.explanation[1].value != that.explanation[1].value):
            # priorities: left (4), down (3), right (2), up (1)
            return this.explanation[1].value > that.explanation[1].value
        else:
            return self.priority < other.priority


class State:
    # g: cost so far
    # prev: previous state
    def __init__(self, board, g, h,  prev=None, explanation=None, gs=False):
        self.board = board
        self.g = g
        self.h = h
        self.possible_actions = self.get_possible_actions(self.board.tiles)
        self.prev = prev
        self.explanation = explanation
        self.gs = gs

    def get_possible_actions(self, tiles):
        actions = {}
        for i in range(len(tiles)):
            for j in range(len(tiles[i])):
                el = tiles[i][j]
                if (el != DOT):
                    up = i - 1
                    down = i + 1
                    right = j + 1
                    left = j - 1

                    while (up >= 0 and tiles[up][j] != DOT):
                        up -= 1
                    while (down < len(tiles) and tiles[down][j] != DOT):
                        down += 1
                    while (left >= 0 and tiles[i][left] != DOT):
                        left -= 1
                    while (right < len(tiles[i]) and tiles[i][right] != DOT):
                        right += 1

                    possible_dests = []

                    if (up >= 0 and up != i - 1):
                        possible_dests.append((Move.UP, i - up - 1))
                    if (down < len(tiles) and down != i + 1):
                        possible_dests.append((Move.DOWN, down - i - 1))
                    if (left >= 0 and left != j - 1):
                        possible_dests.append((Move.LEFT, j - left - 1))
                    if (right < len(tiles[i]) and right != j + 1):
                        possible_dests.append((Move.RIGHT, right - j - 1))

                    if (possible_dests):
                        actions[(tiles[i][j], i, j)] = possible_dests
        # sort according to first element (peg) of the first tuple (key)
        return self.sort_possible_actions(actions)

    def expand(self):
        neighbors = []
        for key, actions in self.possible_actions.items():  # should we sort this
            peg, i, j = key
            for act in actions:
                tiles_copy = [row[:] for row in self.board.tiles]
                move, pegs_eaten = act
                explanation = (peg, move)

                i_ = i
                j_ = j
                for _ in range(pegs_eaten + 1):
                    tiles_copy[i_][j_] = DOT

                    if move == Move.UP:
                        i_ -= 1
                    if move == Move.DOWN:
                        i_ += 1
                    if move == Move.LEFT:
                        j_ -= 1
                    if move == Move.RIGHT:
                        j_ += 1

                tiles_copy[i_][j_] = peg
                neighbor = State(Board(tiles_copy), self.g +
                                 move.value, self.h, prev=self, explanation=explanation, gs=self.gs)
                neighbors.append(neighbor)
        return neighbors

    def __str__(self):
        retr = "-" * 10 + "\n"
        retr += "Board:\n"
        for i, _ in enumerate(self.board.tiles):
            for j, _ in enumerate(self.board.tiles[i]):
                retr += str(self.board.tiles[i][j]) + " "
            retr += "\n"
        retr += "Possible actions: \n"
        for key, value in self.possible_actions.items():
            retr += f"{key} --> {value}\n"
        retr += f"Cost of this state: {self.f()}\n"
        retr += "-" * 10
        return retr

    def sort_possible_actions(self, possible_actions):
        for key in possible_actions.keys():
            possible_actions[key] = sorted(possible_actions[key], reverse=True)

        return dict(sorted(possible_actions.items(), key=lambda item: item[0][0]))

    def is_goal(self):
        return self.board.is_goal()

    def f(self):
        if (not self.gs):
            return self.h(self.board) + self.g
        else:
            return self.h(self.board)

    def __lt__(self, other):
        if (self.f() != other.f()):
            return self.f() < other.f()
        elif (self.explanation[0] != other.explanation[0]):
            return self.explanation[0] < other.explanation[0]
        else:
            # priorities: left (4), down (3), right (2), up (1)
            return self.explanation[1].value > other.explanation[1].value


def read_txt(txt):
    return [[i for i in line.strip()] for line in txt.split("\n") if line]


def get_path(winner):
    stack = []
    while (winner != None):
        stack.append(winner.explanation)
        winner = winner.prev
    stack.pop()  # pop up the first explanation (which is None)

    exp = []
    while (stack):
        tpl = stack.pop()
        exp.append(f"{tpl[0]} {tpl[1].name.lower()}")
    return ", ".join(exp)


def h1(board):
    row_cnt = 0
    for row in board.tiles:
        # increment row counter if any of the element in the row is a peg
        is_not_dot = [i != DOT for i in row]
        row_cnt = row_cnt + 1 if any(is_not_dot) else row_cnt

    col_cnt = 0
    for col_index in range(len(board.tiles[0])):
        col = [row[col_index] for row in board.tiles]

        is_not_dot = [i != DOT for i in col]
        col_cnt = col_cnt + 1 if any(is_not_dot) else col_cnt
    return min(row_cnt, col_cnt) - 1


def h2(board):
    """
    For every peg there is an edge between the corresponding row and column vertices.
    """
    bigraph = {}

    c_dir = {}
    c_inc = 0

    for r in range(len(board.tiles)):
        bigraph[r] = []
        for c in range(len(board.tiles[0])):
            if (board.tiles[r][c] != DOT):
                if c not in c_dir:
                    c_dir[c] = c_inc
                    c_inc += 1
                bigraph[r].append(c)   # r(th) row is connected to c(th) column

    for key in bigraph.keys():
        bigraph[key] = [c_dir[c] for c in bigraph[key]]
    return koenig(bigraph) - 1


def bfs(problem):
    fringe = []
    cnt = 0
    fringe.append(State(Board(problem), 0, lambda _: 0,
                  prev=None,  explanation=None, gs=False))
    while fringe:
        state = fringe.pop(0)
        cnt += 1
        if (state.is_goal()):
            return (state, cnt)
        fringe.extend(state.expand())

def dfs(problem):
    cnt = 0
    fringe = []
    fringe.append(State(Board(problem), 0, lambda _: 0,
                  prev=None,  explanation=None, gs=False))
    while fringe:  # fringe is not None
        state = fringe.pop()
        cnt += 1
        if (state.is_goal()):
            return (state, cnt)
        fringe.extend(state.expand())
    return False  # not found


def pq_search(problem, heuristics, gs=False):
    cnt = 0
    pq_counter = 0
    fringe = []
    fringe.append(Pair(State(Board(problem), 0, heuristics,
                  prev=None, explanation=None, gs=gs), pq_counter))
    pq_counter += 1
    while fringe:  # fringe is not None
        state = heapq.heappop(fringe).State
        cnt += 1
        if (state.is_goal()):
            return (state, cnt)
        for ne in state.expand():
            heapq.heappush(fringe, Pair(ne, +pq_counter))
            pq_counter += 1
    return False


def main():
    search_list = ["BFS", "DFS", "UCS", "GS", "A*", "A*2"]
    search = "A*2"
    target_url = "https://www.cmpe.boun.edu.tr/~emre/courses/cmpe480/hw1/input1.txt"
    txt = requests.get(target_url).text

    problem = read_txt(txt)

    def console(tpl):
        solution = tpl[0]
        cnt = tpl[1]

        path = get_path(solution)
        print("Number of nodes removed from the fringe:", cnt)
        print("Path cost:", solution.g)
        print("Path:", path)

    if (search == "BFS"):
        console(bfs(problem))
    elif (search == "DFS"):
        console(dfs(problem))
    elif (search == "UCS"):
        console(pq_search(problem, heuristics=lambda _: 0))
    elif (search == "GS"):
        console(pq_search(problem, heuristics=h1, gs=True))
    elif (search == "A*"):
        console(pq_search(problem, heuristics=h1))
    elif (search == "A*2"):
        console(pq_search(problem, heuristics=h2))


if __name__ == "__main__":
    main()
