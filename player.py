from board import *
from random import Random


class Player:
    def choose_action(self, board):
        raise NotImplementedError


class RandomPlayer(Player):
    #using random algorithm
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        return self.random.choice([
            Direction.Left,
            Direction.Right,
            Direction.Down,
            Rotation.Anticlockwise,
            Rotation.Clockwise,
        ])       

class FirstPlayer(Player):
    # using genetic algorithm to predict the best actions
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        bestscore = -999
        bestmove = None
        for xtarget in range(10):
            for xorientation in range(4):
                score, moves = self.try_all_moves(board, xtarget, xorientation) 
                # print(bestscore)
                # print(score)       
                if score > bestscore:
                    bestscore = score
                    bestmove = moves       
        return bestmove
                
    def try_all_moves(self, board, xtarget, xorientation):
        clone_board = board.clone()
        moves = []
        if xorientation == 1:
            moves.append(Rotation.Clockwise)
            if clone_board.falling is not None:
                clone_board.rotate(Rotation.Clockwise)
        elif xorientation == 2:
            moves.append(Rotation.Clockwise)
            moves.append(Rotation.Clockwise)
            if clone_board.falling is not None:
                clone_board.rotate(Rotation.Clockwise)
                clone_board.rotate(Rotation.Clockwise)
        elif xorientation == 3:
            moves.append(Rotation.Anticlockwise)
            if clone_board.falling is not None:
                clone_board.rotate(Rotation.Anticlockwise)
        while clone_board.falling is not None:
            if clone_board.falling.left - xtarget > 0:
                difference = clone_board.falling.left - xtarget
                for i in range(difference):
                    moves.append(Direction.Left)
                    if clone_board.falling is not None:
                        clone_board.move(Direction.Left)
                    else:
                        break
            elif clone_board.falling.left - xtarget < 0:
                difference = clone_board.falling.left - xtarget
                for i in range(-difference):
                    moves.append(Direction.Right)
                    if clone_board.falling is not None:
                        clone_board.move(Direction.Right)
                    else:
                        break
            if clone_board.falling is not None:
                moves.append(Direction.Drop)
                clone_board.move(Direction.Drop)
            break
        score = self.score_board(clone_board, board)
        return score, moves

        #  while self.clone_board.falling is not None:
        #     if self.clone_board.falling.left < xtarget:
        #         self.t.append(Direction.Right)
        #         if self.clone_board.falling is not None:
        #             self.clone_board.move(Direction.Right)
        #         else:
        #             break
        #     elif self.clone_board.falling.left > xtarget:
        #         self.t.append(Direction.Left)
        #         if self.clone_board.falling is not None:
        #             self.clone_board.move(Direction.Left)
        #         else:
        #             break
        #     else:
        #         self.t.append(Direction.Drop)
        #         if board.falling is not None:
        #             if self.clone_board.move(Direction.Drop):
        #                 print("drop")
        #             else:
        #                 print("not defined")
        #         else:
        #             break
        #         break        

    def complete_lines(self, clone_board, board):
        originalscore = clone_board.score
        newscore = board.score
        difference = originalscore - newscore
        # print(originalscore)
        # print(newscore)
        # print(difference)
        if difference >= 100 and difference <= 399:
            return 1
        elif difference >= 400 and difference <= 799:
            return 2
        elif difference >= 800 and difference <= 1599:
            return 3
        elif difference >= 1600:
            return 4
        else:
            return 0

    def lines_cleared(self, clone_board, board):
        line_board = max(self.store_column_heights(board))
        line_clone = max(self.store_column_heights(clone_board))
        lines = line_board - line_clone
        line_count = 0
        if lines < 0:
            lines = 0
        return lines

    def bumpiness(self, clone_board):
        bumps = 0
        col = [24, 24, 24, 24, 24, 24, 24, 24, 24, 24]
        for x in range(clone_board.width):
            for y in range(clone_board.height):
                if col[x] > y and (x, y) in clone_board.cells:
                    col[x] = y
                    for num in range(10):
                        col[num] = 24 - col[num]
        for i in range(9):
            bumps += abs(col[i] - col[i+1])
        return bumps
    
    def store_column_heights(self, clone_board):
        columns = [0]
        height_of_board = 23
        for x in range(clone_board.width):
            column_height = 0
            for y in range(clone_board.height):
                if (x, y) not in clone_board.cells:
                    column_height += 1
                if (x, y) in clone_board.cells:
                    columns.append(height_of_board - column_height)
                    break
        return columns
    
    def holes(self, clone_board):
        holes = 0
        for (x, y) in clone_board.cells:
            if (x, (y+1)) not in clone_board.cells and y != 23:
                holes += 1
        return holes
    
    def score_board(self, clone_board, board):
        line = self.complete_lines(clone_board, board)
        # line = self.lines_cleared(clone_board, board)
        bumps = self.bumpiness(clone_board)
        holes = self.holes(clone_board)
        height = sum(self.store_column_heights(clone_board))
        score = (line*0.76) + (height*-0.510066) + (bumps*-0.184483) + (holes*-0.35663)  - (max(self.store_column_heights(clone_board), default = 0))
        return score
        # return line*0.760666 - (max(height, default = 0)) - (sum(height)*0.5)

class SecondPlayer(Player):
    def __init__(self, seed=None):
        self.random = Random(seed)

    def choose_action(self, board):
        if board.falling.top == 0:
            bestscore = -999
            bestmove = []
            for xtarget in range(10):
                for xrotation in range(-2, 3):
                    for x2target in range(10):
                        score, moves = self.try_all_moves(board, xtarget, xrotation, x2target, 0)
                        if score > bestscore:
                            bestscore = score
                            bestmove = moves
        return bestmove

    def try_all_moves(self, board, xtarget, xrotation, x2target, x2rotation):
        clone_board = board.clone()
        rotation = 0
        moves = []
        while True:
            if clone_board.falling.left < xtarget:
                move = Direction.Right
                result = clone_board.move(move) 
            elif clone_board.falling.left > xtarget:
                move = Direction.Left
                result = clone_board.move(move) 
            elif rotation < xrotation:
                rotation += 1
                move = Rotation.Clockwise
                result = clone_board.rotate(move) 
            elif rotation > xrotation:
                rotation -= 1
                move = Rotation.Anticlockwise
                result = clone_board.rotate(move) 
            else:
                move = Direction.Drop
                result = clone_board.move(move) 
            moves.append(move)
            if result:
                break
        rotation = 0
        while True:
            if clone_board.falling.left < x2target:
                move = Direction.Right
                result = clone_board.move(move) 
            elif clone_board.falling.left > x2target:
                move = Direction.Left
                result = clone_board.move(move) 
            elif rotation < x2rotation:
                rotation += 1
                move = Rotation.Clockwise
                result = clone_board.rotate(move) 
            elif rotation > x2rotation:
                rotation -= 1
                move = Rotation.Anticlockwise
                result = clone_board.rotate(move) 
            else:
                move = Direction.Drop
                result = clone_board.move(move) 
            moves.append(move)
            if result:
                score = self.score_board(board, clone_board)
                return score, moves

    def score_board(self, board, clone_board):
        actual_board = self.create_actual_board(clone_board) 
        lines = self.complete_lines(clone_board, board)
        height = sum(self.store_column_heights(actual_board))        
        bumps = self.bumpiness(actual_board, clone_board)
        holes = self.holes(actual_board)
        score = (0.760666*lines) + (-0.510066 * height) + (-0.184483 * bumps) + (-0.35663 * holes)
        return score

    def create_actual_board(self, board):
        actual_board = [[0 for i in range(0, 10)] for k in range(0, 24)]
        for x, y in board.cells:
            actual_board[y][x] = 1
        return actual_board

    def complete_lines(self, clone_board, board):
        originalscore = clone_board.score
        newscore = board.score
        difference = originalscore - newscore
        return difference

    def store_column_heights(self, actual_board):
        columns = [0 for i in range(0, 10)]
        for x in range(0, 10):
            for y in range(0, 24):
                if actual_board[y][x] == 1:
                    columns[x] = 24 - y
                    break
        return columns
                
    def bumpiness(self, actual_board, clone_board):
        # height = self.store_column_heights(actual_board)
        # bumps = 0
        # col = [24, 24, 24, 24, 24, 24, 24, 24, 24, 24]
        # for x in range (0, 10):
        #     for y in range(0, 24):
        #         if col[x] > y and (x, y) in clone_board.cells:
        #             col[x] = y
        #             for num in range(10):
        #                 col[num] = 24 - col[num]
        # for i in range(0, 9):
        #     bumps += abs(col[i] - col[i+1])
        # return bumps
        bumps = 0
        height = self.store_column_heights(actual_board)
        for i in range(0, len(height) - 1):
            bumps += abs(height[i] - height[i+1])
        return bumps

    def holes(self, actual_board):
        holes = 0
        height = self.store_column_heights(actual_board)
        for x in range(0, 10):
            for y in range(1, 23):
                if actual_board[y][x] == 0 and height[x] > (23 - y):
                    holes += 1
        return holes

SelectedPlayer = SecondPlayer

    # def score_board(self):
    #     a = 0.510066
    #     b = 0.760666
    #     c = 0.35663
    #     d = 0.184483
    #     score = (a*aggregate_height)+(b*complete_lines)+(c*holes)+(d*bumpiness)
    #     return score

