"""
Constraints:
    1. The Die has 6 sides, each can be any integer
    2. The Die has to tip into an adjacent square. It cannot be rotated or translated
    3. The Die starts with a score of 0 and on the nth move its score increases by N * the face up value
    4. The Die is only allowed to move to a square if the value of the square equals the value of the die after moving
    5. The game ends when the Die is in the top right square. The answer is the sum of the unvisited squares.
"""
grid = [
    [57, 33, 132, 268, 492, 732],
    [81, 123, 240, 443, 353, 508],
    [186, 42, 195, 704, 452, 228],
    [-7, 2, 357, 452, 317, 395],
    [5, 23, -4, 592, 445, 620],
    [0, 77, 32, 403, 337, 452]
]
total_sum = sum([sum(grid[i]) for i in range(len(grid))])
init_front = ''
init_left = ''
init_right = ''
init_back = ''
init_top = ''
init_bottom = ''
path = set()
path.add((0, 0))
memo = {}


def solution(value, r, c, n, top, left, right, front, back, bottom):
    # === Base Cases === #
    if (value, r, c, n, top, left, right, front, back, bottom) in memo:
        return memo[(value, r, c, n, top, left, right, front, back, bottom)]

    if r not in range(0, 6) or c not in range(0, 6) or (value != grid[r][c]):
        memo[(value, r, c, n, top, left, right, front, back, bottom)] = False
        return False

    path.add((r, c))
    if r == 0 and c == 5:
        memo[(value, r, c, n, top, left, right, front, back, bottom)] = tuple(path)
        return tuple(path)

    # === Backtracking DFS Approach === #
    n = n + 1
    set_top, set_right, set_front, set_back, set_bottom = (False, False, False, False, False)

    # move up:
    if back == '':
        back = (grid[r - 1][c] - value) / n if r - 1 in range(0, 6) else -1
        set_back = True
    if solution(value + n * back, r - 1, c, n, top=back, left=left, right=right, front=top, back=bottom,
                bottom=front):
        memo[(value + n * back, r - 1, c, n, back, left, right, top, bottom, front)] = solution(
            value + n * back, r - 1, c, n, top=back, left=left, right=right, front=top, back=bottom, bottom=front)
        return memo[(value + n * back, r - 1, c, n, back, left, right, top, bottom, front)]
    back = '' if set_back else back

    # move down:
    if front == '':
        front = (grid[r + 1][c] - value) / n if r + 1 in range(0, 6) else -1
        set_front = True
    if solution(value + n * front, r + 1, c, n, top=front, left=left, right=right, front=bottom, back=top,
                bottom=back):
        memo[(value + n * front, r + 1, c, n, front, left, right, bottom, top, back)] = solution(
            value + n * front, r + 1, c, n, top=front, left=left, right=right, front=bottom, back=top, bottom=back)
        return memo[(value + n * front, r + 1, c, n, front, left, right, bottom, top, back)]
    front = '' if set_front else front

    # move left:
    if right == '':
        right = (grid[r][c - 1] - value) / n if c - 1 in range(0, 6) else -1
        set_right = True
    if solution(value + n * right, r, c - 1, n, top=right, left=top, right=bottom, front=front, back=back,
                bottom=left):
        memo[(value + n * right, r, c - 1, n, right, top, bottom, front, back, left)] = solution(
            value + n * right, r, c - 1, n, top=right, left=top, right=bottom, front=front, back=back, bottom=left)
        return memo[(value + n * right, r, c - 1, n, right, top, bottom, front, back, left)]
    right = '' if set_right else right

    # move right:
    if left == '':
        left = (grid[r][c + 1] - value) / n if c + 1 in range(0, 6) else -1
    if solution(value + n * left, r, c + 1, n, top=left, left=bottom, right=top, front=front, back=back,
                bottom=right):
        memo[(value + n * left, r, c + 1, n, left, bottom, top, front, back, right)] = solution(
            value + n * left, r, c + 1, n, top=left, left=bottom, right=top, front=front, back=back, bottom=right)
        return memo[(value + n * left, r, c + 1, n, left, bottom, top, front, back, right)]
    path.remove((r, c))
    return False


final_path = solution(0, 5, 0, 0, top=init_top, left=init_left, right=init_right, front=init_front, back=init_back,
                      bottom=init_bottom)
print('final answer:', total_sum - sum([grid[i[0]][i[1]] for i in final_path]))

