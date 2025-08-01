from __future__ import annotations
"""
Ensure you have read the introduction and task 1 and understand what 
is prohibited in this task.
This includes:
The ban on inbuilt sort methods .sort() or sorted() in this task.
And ensure your treasure data structure is not banned.

"""
from abc import ABC, abstractmethod
from typing import List

from config import Tiles
from treasure import Treasure, generate_treasures
from data_structures.heap import MaxHeap
from data_structures.linked_list import LinkedList
from betterbst import BetterBST
from data_structures.bst import BSTInOrderIterator
from data_structures.linked_stack import LinkedStack


class Hollow(ABC):
    """
    DO NOT MODIFY THIS CLASS
    Mystical troves of treasure that can be found in the maze
    There are two types of hollows that can be found in the maze:
    - Spooky Hollows: Each of these hollows contains unique treasures that can be found nowhere else in the maze.
    - Mystical Hollows: These hollows contain a random assortment of treasures like the spooky hollow however all mystical hollows are connected, so if you remove a treasure from one mystical hollow, it will be removed from all other mystical hollows.
    """

    # DO NOT MODIFY THIS ABSTRACT CLASS
    """
    Initialises the treasures in this hollow
    """

    def __init__(self) -> None:
        self.treasures = self.gen_treasures()
        self.restructure_hollow()

    @staticmethod
    def gen_treasures() -> List[Treasure]:
        """
        This is done here, so we can replace it later on in the auto marker.
        This method contains the logic to generate treasures for the hollows.

        Returns:
            List[Treasure]: A list of treasures that can be found in the maze
        """
        return generate_treasures()

    @abstractmethod
    def restructure_hollow(self):
        pass

    @abstractmethod
    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        pass

    def __len__(self) -> int:
        """
        After the restructure_hollow method is called, the treasures attribute should be updated
        don't create an additional attribute to store the number of treasures in the hollow.
        """
        return len(self.treasures)


class SpookyHollow(Hollow):

    def restructure_hollow(self) -> None:
        """
        Re-arranges the treasures in the hollow from a list to a new
        data structure that is better suited for the get_optimal_treasure method.

        The new treasures data structure can't be an ArrayR or list variant (LinkedList, python list, sorted list, ...).
        No lists! Breaching this will count as a major error and lose up to 100% of the marks of the task!

        Returns:
            None - This method should update the treasures attribute of the hollow

        Complexity:
        Both the best and worst case complexity is O(nlogn) where n is the number of treasures in the hollow. This is because, the for loop used to 
        convert the treasure values into a tuple format has a complexity of O(n) since it iterates over n number of items in the list. The _init_ method
        of the better bst itself has a best and worst case complexity of O(nlogn). Therefore combining both these complexities gives us O(n + nlogn) which
        is simplified to O(nlogn)

            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: O(nlogn) where n is the number of treasures in the hollow
            Worst Case Complexity: O(nlogn) where n is the number of trasures in the hollow

        Complexity requirements for full marks:
            Best Case Complexity: O(n log n)
            Worst Case Complexity: O(n log n)
            Where n is the number of treasures in the hollow
        """
        numbers = [(treasure.value_to_weight_ratio, treasure) for treasure in self.treasures]
        self.treasures = BetterBST(numbers)

    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        """
        Removes the ideal treasure from the hollow 
        Takes the treasure which has the greatest value / weight ratio 
        that is less than or equal to the backpack_capacity of the player as
        we can't carry treasures that are heavier than our backpack capacity.

        Ensure there are only changes to the treasures contained in the hollow
        if there is a viable treasure to take. If there is a viable treasure
        only remove that treasure from the hollow, no other treasures should be removed.

        Returns:
            Treasure - the ideal treasure that the player should take.
            None - if all treasures are heavier than the backpack_capacity
            or the hollow is empty

        Complexity:
        The best-case complexity occurs when the treasure with the highest ratio is found using the get_maximal() method which has a complexity of
        O(logn) since the tree is always balanced, and the treasure found also has a weight lesser than the backpack capacity in which case we delete the item from the
        balanced bst which has a complexity of O(logn) because it is balanced, and then immediately return the item, hence we have a complexity of O(logn + logn) which simplifies to
        a final best-case complexity of O(logn).

        The worst-case complexity occurs when the treasure with the highest ratio is not found successfully using our single get_maximal() method because the
        treasure found has a weight greater than the backpack capacity, hence it cannot be carried. This would lead to the in-order traversal being carried out in order
        to get an ordered list of treasures and this has a complexity of O(n). The for loop to push the n number of items into a stack has a complexity of O(n) since the push()
        method is O(1) and we do this n times. The for loop to pop from the stack and append into a list has a complexity of O(n) since both pop() and append() have a complexity
        of O(1) and we do this n number of times. The for loop to check the treasures weight has a complexity of O(n) since the cost of comparison can be assumed to be O(1). Finally, the
        deletion of a node from a balanced bst has a complexity of O(logn). Therefore, we can combine all of these individual complexities to O(n + n + n + n + logn) which is simplified
        to a final worst-case complexity of O(n).
 
            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: O(logn) where n is the number of elements inside the balanced binary search tree
            Worst Case Complexity: O(n) where n is the number of elements inside the balanced binary search tree

        Complexity requirements for full marks:
            Best Case Complexity: O(log(n))
            Worst Case Complexity: O(n)
            n is the number of treasures in the hollow 
        """
        if self.treasures.is_empty():
            return None
            
        chosen_treasure = None
        empty_stack = LinkedStack()

        best_treasure = self.treasures.get_maximal(self.treasures.root)
        # print(best_treasure.item)
        if best_treasure.item.weight <= backpack_capacity:
            chosen_treasure = best_treasure.item
            del self.treasures[best_treasure.key]
            return chosen_treasure

        ordered_nodes = [(node.key, node.item) for node in self.treasures]

        for node in ordered_nodes:
            empty_stack.push(node)
            
        ordered_nodes = []

        for _ in range(len(empty_stack)):
            node = empty_stack.pop()
            ordered_nodes.append(node)
            
        for node in ordered_nodes:
            ratio, treasure = node
            if treasure.weight <= backpack_capacity:
                chosen_treasure = treasure
                treasure_to_delete = ratio
                break

        if chosen_treasure is None:
            return None

        del self.treasures[treasure_to_delete]

        return chosen_treasure

    def __str__(self) -> str:
        return Tiles.SPOOKY_HOLLOW.value

    def __repr__(self) -> str:
        return str(self)


class MysticalHollow(Hollow):

    def restructure_hollow(self):
        """
        Re-arranges the treasures in the hollow from a list to a new
        data structure that is better suited for the get_optimal_treasure method.

        The new treasures data structure can't be an ArrayR or list variant (LinkedList, python list, sorted list, ...).
        No lists! Breaching this will count as a major error and lose up to 100% of the marks of the task! 

        Returns:
            None - This method should update the treasures attribute of the hollow

        Complexity:
        Both the best and worst case complexity is O(n) because we call the _init_ method for max heap which has a best and worst case complexity
        of O(n) and the heapify method also has a best and worst case complexity of O(n). Therefore, we can combine this to form a complexity of O(n + n)
        which is simplified to a final complexity of O(n).

            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: O(n) where n is the number of treasures in the hollow
            Worst Case Complexity: O(n) where n is the number of treasures in the hollow

        Complexity requirements for full marks:
            Best Case Complexity: O(n)
            Worst Case Complexity: O(n)
            Where n is the number of treasures in the hollow
        """
        self.heap = MaxHeap(len(self.treasures))
        self.heap = self.heap.heapify(self.treasures)

    def get_optimal_treasure(self, backpack_capacity: int) -> Treasure | None:
        """
        Removes the ideal treasure from the hollow 
        Takes the treasure which has the greatest value / weight ratio 
        that is less than or equal to the backpack_capacity of the player as
        we can't carry treasures that are heavier than our backpack capacity.

        Ensure there are only changes to the treasures contained in the hollow
        if there is a viable treasure to take. If there is a viable treasure
        only remove that treasure from the hollow, no other treasures should be removed.

        Returns:
            Treasure - the ideal treasure that the player should take.
            None - if all treasures are heavier than the backpack_capacity
            or the hollow is empty

        Complexity:
        The best-case complexity occurs when in the first iteration of the treasure with the highest ratio is found and it also has a weight
        that is lesser than the backpack capacity so it breaks out of the loop immediately. In this case since we only go through one iteration 
        of the while loop it has a complexity of O(1) and since we call the get_max() method, which has a best and worst case complexity of O(logn), 
        the whole while loop has a total complexity of O(logn). The for loop will have a complexity of O(1) because it would be empty since no items needed
        to be temporarily stored into it. Therefore, the final best-case complexity is O(logn + 1) which simplifies to O(logn).

        The worst-case complexity occurs when almost all the treasures that were called by the get_max method, had a weight greater than the backpack capacity
        meaning that the while loop had to go though n-1 iterations and each time it had to call the get_max method which has complexity of O(logn) for best and worst
        case. Hence, the while loop has a complexity of O(n * logn) which simplfies to O(nlogn). The for loop will have had to go through n-1 iterations to add back all the invalid
        treasures back into the max heap leading to a complexity of O(nlogn) where we go through n iterations and the worst-case of add is O(logn) where the element added has to rise all the
        way up to the root. Therefore, we have a complexity of O(nlogn + nlogn) which can be simplified to a final worst-case complexity of O(nlogn).

            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: O(logn) where n is the number of elements in the max heap
            Worst Case Complexity: O(nlogn) where n is the number of elements in the max heap

        Complexity requirements for full marks:
            Best Case Complexity: O(log n)
            Worst Case Complexity: O(n log n)
            Where n is the number of treasures in the hollow
        """
        if self.heap == 0:
            return None
        
        temporary_linked_list = LinkedList(len(self.treasures))
        chosen_treasure = None

        while len(self.heap) > 0:
            treasure = self.heap.get_max()
            if treasure.weight <= backpack_capacity:
                chosen_treasure = treasure
                break
            else:
                temporary_linked_list.append(treasure)

        for treasure in temporary_linked_list:
            self.heap.add(treasure)

        if chosen_treasure is None:
            return None
        return chosen_treasure
    
    def __str__(self) -> str:
        return Tiles.MYSTICAL_HOLLOW.value

    def __repr__(self) -> str:
        return str(self)
