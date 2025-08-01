from __future__ import annotations

from typing import List, Tuple, TypeVar

from data_structures.bst import BinarySearchTree
from algorithms.mergesort import mergesort

K = TypeVar('K')
I = TypeVar('I')


class BetterBST(BinarySearchTree[K, I]):
    def __init__(self, elements: List[Tuple[K, I]]) -> None:
        """
        Initialiser for the BetterBST class.
        We assume that the all the elements that will be inserted
        into the tree are contained within the elements list.

        As such you can assume the length of elements to be non-zero.
        The elements list will contain tuples of key, item pairs.

        First sort the elements list and then build a balanced tree from the sorted elements
        using the corresponding methods below.

        Args:
            elements(List[tuple[K, I]]): The elements to be inserted into the tree.

        Complexity:
        Both the best and worst case complexities are O(nlogn) because in both cases, the _init_ method is called which is O(1), then
        it calls the _sort_elements() methos which has a complexity of O(nlogn) and finally it also calls the _build_balanced_tree method which
        again has a complexity of O(nlogn). Therefore the final complexity is O(1 + nlogn + nlogn) which can be simplifies to O(nlogn).
        
            Best Case Complexity: O(nlogn) where n is the number of elements in the list
            Worst Case Complexity: O(nlogn) where n is the number of elements in the list
        """
        super().__init__()
        new_elements: List[Tuple[K, I]] = self.__sort_elements(elements)
        self.__build_balanced_tree(new_elements)

    def __sort_elements(self, elements: List[Tuple[K, I]]) -> List[Tuple[K, I]]:
        """
        Recall one of the drawbacks to using a binary search tree is that it can become unbalanced.
        If we know the elements ahead of time, we can sort them and then build a balanced tree.
        This will help us maintain the O(log n) complexity for searching, inserting, and deleting elements.

        Args:
            elements (List[Tuple[K, I]]): The elements we wish to sort.

        Returns:
            list(Tuple[K, I]]) - elements after being sorted.

        Complexity:
        Both the best and worst case complexities are O(nlogn), where n is the number of elements in the list, because in both cases, 
        we run a mergesort algorithm which itself has a complexity of O(nlogn) and in both cases we still need to recursively split the 
        list which has a complexity of O(logn) since each split halves the list. The merge() method then merges the sublists back together 
        and it does this n number of times, hence, it has a complexity of O(n). The merging process itself occurs at each of the logn level, 
        so, the final complexity combines the two into O(n * logn) leading to O(nlogn).

            Best Case Complexity: O(nlogn) where n is the number of elements in the list
            Worst Case Complexity: O(nlogn) where n is the number of elements in the list
        """
        return mergesort(elements, sort_key=lambda x : x[0])

    def __build_balanced_tree(self, elements: List[Tuple[K, I]]) -> None:
        """
        This method will build a balanced binary search tree from the sorted elements.

        Args:
            elements (List[Tuple[K, I]]): The elements we wish to use to build our balanced tree.

        Returns:
            None

        Complexity:
            (This is the actual complexity of your code, 
            remember to define all variables used.)
            Best Case Complexity: O(nlogn) where n is the number of elements in the list
            Worst Case Complexity: O(nlogn) where n is the number of elements in the list

        Justification:
        Both the best and worst case complexities are O(nlogn), where n is the number of elements in the list, because in both cases, 
        we still need to recursively split the list at the middle element and call the insert_aux() method which has a complexity of
        O(logn) since the tree is always balanced in this case. Since there are n elements, there will be n insertions into the bst, hence,
        the final complexity is O(n * logn) which simplifies to O(nlogn).

        Complexity requirements for full marks:
            Best Case Complexity: O(n * log(n))
            Worst Case Complexity: O(n * log(n))
            where n is the number of elements in the list.
        """
        self._build_balanced_tree_aux(elements, 0, len(elements) - 1, 0)
    
    def _build_balanced_tree_aux(self, elements, beginning_element, ending_element, current_depth):
        if beginning_element > ending_element:
            return
        middle_element = (beginning_element + ending_element) // 2
        key, item = elements[middle_element]
        if self.root is None:
            self.root = self.insert_aux(self.root, key, item, current_depth)
        else:
            self[key] = item
        self._build_balanced_tree_aux(elements, beginning_element, middle_element - 1, current_depth + 1)
        self._build_balanced_tree_aux(elements, middle_element + 1, ending_element, current_depth + 1)