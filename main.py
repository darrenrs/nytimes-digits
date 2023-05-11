import copy
import argparse
import time
import math
from tabulate import tabulate

class DigitProblem:
  def __init__(self, objective: int, inputs: list[int], operation_history: list[str]=[]):
    self.objective = objective
    self.inputs = inputs
    self.operation_history = operation_history
    self.solutions = []
  
  def __str__(self):
    return f"New problem has an objective of {self.objective},\ninputs {self.inputs},\noperation history {self.operation_history}.\n"

  def solve(self):
    for i in self.inputs:
      if i == self.objective:
        return self.operation_history

    if len(self.inputs) == 1:
      # no solution
      return None

    for n, i in enumerate(self.inputs):
      for o, j in enumerate(self.inputs):
        # skip duplicate runs
        if o <= n:
          continue
        
        if i < j:
          # first number is less than second number
          children = [
            i + j,
            i * j,
            j - i
          ]

          operations = [
            f"{i} + {j} = {i + j}",
            f"{i} * {j} = {i * j}",
            f"{j} - {i} = {j - i}"
          ]

          if j // i == j / i and i > 1:
            # only divide if divisible and no denominator of 1
            children.append(j // i)
            operations.append(f"{j} / {i} = {j // i}")
          
          if i == 1 or j == 1:
            # only multiply if no 1 multiplier (redundant)
            children.pop(1)
            operations.pop(1)
        elif j < i:
          # second number is less than first number
          children = [
            j + i,
            j * i,
            i - j
          ]

          operations = [
            f"{j} + {i} = {j + i}",
            f"{j} * {i} = {j * i}",
            f"{i} - {j} = {i - j}"
          ]

          if i // j == i / j and j > 1:
            children.append(i // j)
            operations.append(f"{i} / {j} = {i // j}")
          
          if i == 1 or j == 1:
            # only multiply if no 1 multiplier (redundant)
            children.pop(1)
            operations.pop(1)
        else:
          # two numbers are equal
          children = [
            i + j,
            i * j,
            i // j
          ]

          operations = [
            f"{i} + {j} = {i + j}",
            f"{i} * {j} = {i * j}",
            f"{i} / {j} = {i // j}"
          ]
          
          if i == 1 or j == 1:
            # only multiply if no 1 multiplier (redundant)
            children.pop(1)
            operations.pop(1)
        
        for p, q in zip(children, operations):
          child = copy.deepcopy(self.inputs)

          if n > o:
            child.pop(n)
            child.pop(o)
          else:
            # alter pop order so that later index always gets popped first
            child.pop(o)
            child.pop(n)
          
          child.append(p)

          operation_history = copy.deepcopy(self.operation_history)
          operation_history.append(q)
          subproblem = DigitProblem(self.objective, child, operation_history)

          solution = subproblem.solve()

          if solution:
            if type(solution[0]) == list:
              self.solutions.append(solution[0])
              for z in solution:
                self.solutions.append(z)
            else:
              self.solutions.append(solution)
    
    return self.solutions

def get_complexity(s, l):
  operation_complexity = 0

  for i in s:
    if '*' in i or '/' in i:
      operation_complexity += 2
    else:
      operation_complexity += 1
  
  base_complexity = len(s) ** operation_complexity
  adjusted_complexity = math.log10(base_complexity) * 10

  star_rtg = adjusted_complexity / (math.log10(((l-1) ** (2*(l-1)))) * 10)

  return math.floor(star_rtg * 100) / 10

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='NYTimes Digit Solver')

  parser.add_argument('-g', '--goal', required=True, type=int, help='Goal number')
  parser.add_argument('-i', '--inputs', required=True, nargs='+', type=int, help='List of numbers that can be used')
  parser.add_argument('-a', '--all', help='Display EVERY possible solution (even semantic duplicates)', action="store_true")

  args = parser.parse_args()
  
  start = time.time()

  dp = DigitProblem(args.goal, args.inputs)
  xo = dp.solve()
  xs = [', '.join(z) for z in xo]

  x = list(set(xs))

  end = time.time()

  final_solutions = []

  for n, i in enumerate(x):
    final_solutions.append([n+1, get_complexity(i.split(','), len(args.inputs)), i])
  
  final_solutions = sorted(final_solutions, key=lambda x: x[1])

  print(f"Found  {len(x)}  solutions in {end-start:.3f}s.")
  if len(x) > 0:
    print(f"Optimal solution: {final_solutions[0][2]}.")
    
    if args.all:
      print(tabulate(final_solutions, headers=['ID', 'Complexity', 'Solution'], tablefmt='fancy_grid'))