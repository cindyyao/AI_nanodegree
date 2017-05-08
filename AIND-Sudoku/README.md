# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: For each unit, find all naked twins within unit. For each naked twins, eliminate both values of the twins from all other boxes within the same unit. The logic behind this algorithm is that, if any value from the naked twins is assign to other boxes, both boxes of naked twins have to take the other (same) value, which is impossible. So values from naked twins have to be assigned to one of the naked twins box. This constraint could speed up the algorithm by reducing the number of possibilities. In depth first search, time complexity has a positive correlation with the number of subtrees, especially for nodes closed to the root.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?  
A: Besides columns, rows and 3x3 squares, the two diagonals are also considered as units and added to the unitlist. In addition to the constraint we have in the normal Sudoku, there is another constraint that each number from 1-9 must appear exactly once in the main diagonal. Thus, the possibility space of a diagonal sudoku problem is smaller than a corresponding normal sudoku problem, so that it's less likely to find a solution for a diagonal sudoku problem.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solution.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.900nw

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py


### Submission
Before submitting your solution to a reviewer, you are required to submit your project to Udacity's Project Assistant, which will provide some initial feedback.  

The setup is simple.  If you have not installed the client tool already, then you may do so with the command `pip install udacity-pa`.  

To submit your code to the project assistant, run `udacity submit` from within the top-level directory of this project.  You will be prompted for a username and password.  If you login using google or facebook, visit [this link](https://project-assistant.udacity.com/auth_tokens/jwt_login for alternate login instructions.

This process will create a zipfile in your top-level directory named sudoku-<id>.zip.  This is the file that you should submit to the Udacity reviews system.

