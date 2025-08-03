# Labyrinth Explorer System

Welcome to the **Labyrinth Explorer System**, an interactive Python project designed to simulate maze exploration with treasure hunting. This project demonstrates the use of advanced data structures and algorithms to:
- Navigate complex mazes with obstacles and multiple exits
- Find valid paths using a recursive depth-first search (DFS)
- Manage and restructure treasure collections inside Spooky and Mystical Hollows
- Optimize treasure selection based on value-to-weight ratios
- Handle dynamic treasure removal and backpack capacity constraints
- Solve the knapsack problem

## Features
- **Recursive Maze Navigation:**
  - Implements Depth-First Search with backtracking to find valid escape paths
  - Supports multiple exits and avoids walls and obstacles
- **Treasure Management System:**
  - Spooky Hollows: Independent treasure caches with unique items
  - Mystical Hollows: Shared treasure pools across multiple locations in the maze
  - Automatic greedy selection of treasures based on the value-to-weight ratio that fits in the backpack
- **Custom Data Structures**
  - Balanced Binary Search Trees (BetterBST) for efficient storage and lookups. Functions similarly to an AVL tree
  - Non-list-based data structures for hollows to optimize treasure retrieval such as a Max Heap
  - MazeCell objects track position, state, and hollow contents
- **Time Complexity-Aware Design:**
  - DFS ensures valid traversal without infinite loops
  - Efficient treasure selection with optimal complexity for best and worst cases
  - Backtracking avoids redundant path computations

## Project Structure
- maze.py #Maze traversal, recursive DFS, pathfinding, and treasure collection functionality
- hollows.py #Implements SpookyHollow and MysticalHollow classes for treasure placement and management
- betterbst.py #Balanced BST for efficient element storage and lookup
- treasure.py #Defines the Treasure class with value, weight, and ratio computation all randomly generated
- random_gen.py #Randomly generates attributes for each treasure created
- config.py #Defines all constants used in the project
- data structures/
  - bst.py #Binary Search Tree implementation
  - linked_stack.py #Linked Stack implementation
  - heap.py #Max heap implementation
  - linked_list.py #Linked List implementation
- algorithms/
  - mergesort.py #Code for merge sort
  - quicksort.py #Code for quick sort
  - binary_search.py #Code for binary search

## Concepts Covered
- Abstract Data Types (ADTs)
- Recursive Depth-First Search (DFS) and Backtracking
- Greedy Algorithms for Optimal Treasure Selection
- Balanced Binary Search Tree Construction
- Time Complexity-Conscious Design
- Custom Data Structure Implementation
- Max Heap functionality

## How To Run
- Clone the repo by clicking the green 'Code' button, and then copy the HTTPS link of the repository
- Open Visual Studio Code, navigate to the source control section and click clone repository
- Paste the copied link into this box and hit enter
- Select the location where you want to store the folder/repository and click 'Open'
- The repository will be cloned, giving you access to the simulator

## Testing
- To use the test files, simply run this command in the terminal and just hit enter if you want to run all tests or you can specify the test number to run a specific one: python run_tests.py
- Each test file checks to see if parts of the program are functioning properly
- Print statements can be added to assist in debugging

# Learning Objectives
This project demonstrates the practical application of algorithms and data structures in solving a pathfinding and resource management problem, reinforcing:
- Recursive traversal and backtracking
- Efficient data handling and custom ADTs
- Greedy algorithms for decision making
- Performance-conscious Python programming





