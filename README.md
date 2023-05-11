# Digits Puzzle Calculator
Calculator for the New York Times Digits Puzzle using depth-first search. By default, the optimal solution (i.e., least number of steps and simplest arithmetic) is returned, but all other found solutions may be displayed as well.

While the calculator works with an arbitary number of integer parameters, runtime becomes extremely long with seven or more inputs, so I wouldn't recommend going above six.

## Parameters
```
-g/--goal   : A single integer specifying the goal number.
-i/--inputs : A space-delimited list of possible input numbers.
-a/--all    : Display all possible solutions to stdout.
```

## Issues
- Many redundant solutions are returned, even though they technically differ operation order
- Insufficient pruning for high amounts of inputs