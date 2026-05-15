"""
Test suite for algorithms.py
Mirrors the structure of guiff0/fisrtApp (Java → Python translation).

Run with:
    python -m pytest test_algorithms.py -v
  or:
    python -m unittest test_algorithms.py -v
"""

import collections
import math
import sys
import unittest

sys.path.insert(0, ".")
from algorithms import (
    # Arrays
    two_sum, max_subarray, merge_intervals, min_rotated_array,
    trapping_rainwater, three_sum, product_except_self,
    container_with_most_water, remove_duplicates_sorted, rotate_array,
    # Strings
    anagram_check, longest_substring_no_repeat, longest_palindromic_substring,
    reverse_words, atoi, valid_palindrome, count_and_say, group_anagrams,
    longest_common_prefix, string_compression,
    # Linked list
    ListNode, reverse_linked_list, detect_cycle, merge_two_sorted_lists,
    middle_of_linked_list, remove_nth_from_end,
    # Stack
    infix_to_postfix, next_greater_element, MinStack,
    largest_rectangle_histogram, reverse_first_k_queue,
    # Binary tree
    TreeNode, level_order_traversal, mirror_trees,
    lowest_common_ancestor_bst, serialize, deserialize, validate_bst,
    # Graphs
    topological_sort, detect_cycle_directed, number_of_islands,
    shortest_path_unweighted, bipartite_check,
    traveling_salesman, connected_cities_shortest_path,
    # Dynamic programming
    knapsack_01, longest_increasing_subsequence, coin_change_min_coins,
    word_break, climbing_stairs,
    # Greedy
    job_sequencing, minimum_platforms, activity_selection, min_cost_connect_ropes,
    # Heaps
    k_largest_elements, MedianFinder, merge_k_sorted_arrays,
    # Bit manipulation
    count_bits, missing_number, reverse_bits, xor_all_subsets, power_of_two,
    # Trie
    Trie, Autocomplete, LongestPrefixMatch,
    # Huffman
    huffman_encoding,
)


# ─── Linked-list helpers ─────────────────────────────────────────────────────

def make_list(vals: list[int]) -> ListNode | None:
    """Build a linked list from a Python list and return the head."""
    dummy = ListNode()
    cur = dummy
    for v in vals:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def to_python_list(head: ListNode | None) -> list[int]:
    """Flatten a linked list to a Python list."""
    result = []
    while head:
        result.append(head.val)
        head = head.next
    return result


def make_cycle(vals: list[int], pos: int) -> ListNode | None:
    """Build a linked list whose tail points back to node at index `pos`."""
    if not vals:
        return None
    nodes = [ListNode(v) for v in vals]
    for i in range(len(nodes) - 1):
        nodes[i].next = nodes[i + 1]
    if pos >= 0:
        nodes[-1].next = nodes[pos]
    return nodes[0]


# ─── Binary-tree helpers ─────────────────────────────────────────────────────

def make_bst(*vals: int) -> TreeNode | None:
    """Insert values one by one into a BST and return the root."""
    root = None

    def insert(node, v):
        if node is None:
            return TreeNode(v)
        if v < node.val:
            node.left = insert(node.left, v)
        else:
            node.right = insert(node.right, v)
        return node

    for v in vals:
        root = insert(root, v)
    return root


# ═════════════════════════════════════════════════════════════════════════════
# ARRAYS
# ═════════════════════════════════════════════════════════════════════════════

class TestTwoSum(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(two_sum([2, 7, 11, 15], 9), [0, 1])

    def test_non_adjacent(self):
        self.assertEqual(two_sum([3, 2, 4], 6), [1, 2])

    def test_duplicate_values(self):
        self.assertEqual(two_sum([3, 3], 6), [0, 1])

    def test_negative_numbers(self):
        self.assertEqual(two_sum([-3, 4, 3, 90], 0), [0, 2])

    def test_no_solution(self):
        self.assertEqual(two_sum([1, 2, 3], 100), [])


class TestMaxSubarray(unittest.TestCase):
    def test_mixed(self):
        self.assertEqual(max_subarray([-2, 1, -3, 4, -1, 2, 1, -5, 4]), 6)

    def test_all_positive(self):
        self.assertEqual(max_subarray([1, 2, 3, 4]), 10)

    def test_all_negative(self):
        self.assertEqual(max_subarray([-3, -1, -2]), -1)

    def test_single_element(self):
        self.assertEqual(max_subarray([5]), 5)

    def test_large_negative_start(self):
        self.assertEqual(max_subarray([-100, 1, 2, 3]), 6)


class TestMergeIntervals(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            merge_intervals([[1, 3], [2, 6], [8, 10], [15, 18]]),
            [[1, 6], [8, 10], [15, 18]],
        )

    def test_touching_intervals(self):
        self.assertEqual(merge_intervals([[1, 4], [4, 5]]), [[1, 5]])

    def test_contained_interval(self):
        self.assertEqual(merge_intervals([[1, 10], [2, 3]]), [[1, 10]])

    def test_no_overlap(self):
        self.assertEqual(merge_intervals([[1, 2], [3, 4]]), [[1, 2], [3, 4]])

    def test_single(self):
        self.assertEqual(merge_intervals([[5, 7]]), [[5, 7]])


class TestMinRotatedArray(unittest.TestCase):
    def test_rotated(self):
        self.assertEqual(min_rotated_array([3, 4, 5, 1, 2]), 1)

    def test_rotated_once(self):
        self.assertEqual(min_rotated_array([2, 1]), 1)

    def test_not_rotated(self):
        self.assertEqual(min_rotated_array([1, 2, 3, 4, 5]), 1)

    def test_single(self):
        self.assertEqual(min_rotated_array([7]), 7)

    def test_two_elements(self):
        self.assertEqual(min_rotated_array([3, 1]), 1)


class TestTrappingRainwater(unittest.TestCase):
    def test_classic(self):
        self.assertEqual(trapping_rainwater([0, 1, 0, 2, 1, 0, 1, 3, 2, 1, 2, 1]), 6)

    def test_symmetric(self):
        self.assertEqual(trapping_rainwater([4, 2, 0, 3, 2, 5]), 9)

    def test_no_water(self):
        self.assertEqual(trapping_rainwater([1, 2, 3]), 0)

    def test_flat(self):
        self.assertEqual(trapping_rainwater([0, 0, 0]), 0)

    def test_valley(self):
        self.assertEqual(trapping_rainwater([3, 0, 3]), 3)


class TestThreeSum(unittest.TestCase):
    def test_basic(self):
        result = three_sum([-1, 0, 1, 2, -1, -4])
        self.assertIn([-1, -1, 2], result)
        self.assertIn([-1, 0, 1], result)

    def test_all_zeros(self):
        self.assertEqual(three_sum([0, 0, 0]), [[0, 0, 0]])

    def test_no_triplet(self):
        self.assertEqual(three_sum([1, 2, 3]), [])

    def test_duplicates_handled(self):
        result = three_sum([-2, 0, 0, 2, 2])
        self.assertEqual(result, [[-2, 0, 2]])


class TestProductExceptSelf(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(product_except_self([1, 2, 3, 4]), [24, 12, 8, 6])

    def test_with_zero(self):
        self.assertEqual(product_except_self([0, 1, 2, 3]), [6, 0, 0, 0])

    def test_two_zeros(self):
        self.assertEqual(product_except_self([0, 0, 2]), [0, 0, 0])

    def test_two_elements(self):
        self.assertEqual(product_except_self([3, 4]), [4, 3])


class TestContainerWithMostWater(unittest.TestCase):
    def test_classic(self):
        self.assertEqual(container_with_most_water([1, 8, 6, 2, 5, 4, 8, 3, 7]), 49)

    def test_equal_heights(self):
        self.assertEqual(container_with_most_water([4, 4]), 4)

    def test_ascending(self):
        self.assertEqual(container_with_most_water([1, 2, 3, 4, 5]), 6)

    def test_two_elements(self):
        self.assertEqual(container_with_most_water([1, 1]), 1)


class TestRemoveDuplicatesSorted(unittest.TestCase):
    def test_basic(self):
        nums = [1, 1, 2]
        k = remove_duplicates_sorted(nums)
        self.assertEqual(k, 2)
        self.assertEqual(nums[:k], [1, 2])

    def test_no_duplicates(self):
        nums = [1, 2, 3]
        self.assertEqual(remove_duplicates_sorted(nums), 3)

    def test_all_same(self):
        nums = [5, 5, 5, 5]
        k = remove_duplicates_sorted(nums)
        self.assertEqual(k, 1)
        self.assertEqual(nums[0], 5)

    def test_empty(self):
        self.assertEqual(remove_duplicates_sorted([]), 0)


class TestRotateArray(unittest.TestCase):
    def test_basic(self):
        nums = [1, 2, 3, 4, 5, 6, 7]
        rotate_array(nums, 3)
        self.assertEqual(nums, [5, 6, 7, 1, 2, 3, 4])

    def test_k_larger_than_n(self):
        nums = [1, 2, 3]
        rotate_array(nums, 4)        # 4 % 3 == 1
        self.assertEqual(nums, [3, 1, 2])

    def test_k_zero(self):
        nums = [1, 2, 3]
        rotate_array(nums, 0)
        self.assertEqual(nums, [1, 2, 3])

    def test_single_element(self):
        nums = [42]
        rotate_array(nums, 99)
        self.assertEqual(nums, [42])


# ═════════════════════════════════════════════════════════════════════════════
# STRINGS
# ═════════════════════════════════════════════════════════════════════════════

class TestAnagramCheck(unittest.TestCase):
    def test_anagram(self):
        self.assertTrue(anagram_check("anagram", "nagaram"))

    def test_not_anagram(self):
        self.assertFalse(anagram_check("rat", "car"))

    def test_different_lengths(self):
        self.assertFalse(anagram_check("ab", "abc"))

    def test_empty_strings(self):
        self.assertTrue(anagram_check("", ""))


class TestLongestSubstringNoRepeat(unittest.TestCase):
    def test_classic(self):
        self.assertEqual(longest_substring_no_repeat("abcabcbb"), 3)

    def test_all_same(self):
        self.assertEqual(longest_substring_no_repeat("bbbbb"), 1)

    def test_pwwkew(self):
        self.assertEqual(longest_substring_no_repeat("pwwkew"), 3)

    def test_empty(self):
        self.assertEqual(longest_substring_no_repeat(""), 0)

    def test_all_unique(self):
        self.assertEqual(longest_substring_no_repeat("abcde"), 5)


class TestLongestPalindromicSubstring(unittest.TestCase):
    def test_odd_palindrome(self):
        result = longest_palindromic_substring("babad")
        self.assertIn(result, ("bab", "aba"))

    def test_even_palindrome(self):
        self.assertEqual(longest_palindromic_substring("cbbd"), "bb")

    def test_entire_string(self):
        self.assertEqual(longest_palindromic_substring("racecar"), "racecar")

    def test_single_char(self):
        self.assertEqual(longest_palindromic_substring("a"), "a")

    def test_no_palindrome_longer_than_1(self):
        result = longest_palindromic_substring("abcd")
        self.assertEqual(len(result), 1)


class TestReverseWords(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(reverse_words("the sky is blue"), "blue is sky the")

    def test_extra_spaces(self):
        self.assertEqual(reverse_words("  hello world  "), "world hello")

    def test_single_word(self):
        self.assertEqual(reverse_words("word"), "word")

    def test_two_words(self):
        self.assertEqual(reverse_words("a b"), "b a")


class TestAtoi(unittest.TestCase):
    def test_positive(self):
        self.assertEqual(atoi("42"), 42)

    def test_negative(self):
        self.assertEqual(atoi("   -42"), -42)

    def test_trailing_chars(self):
        self.assertEqual(atoi("4193 with words"), 4193)

    def test_words_first(self):
        self.assertEqual(atoi("words and 987"), 0)

    def test_overflow_positive(self):
        self.assertEqual(atoi("99999999999"), 2**31 - 1)

    def test_overflow_negative(self):
        self.assertEqual(atoi("-99999999999"), -(2**31))

    def test_empty(self):
        self.assertEqual(atoi(""), 0)

    def test_plus_sign(self):
        self.assertEqual(atoi("+100"), 100)


class TestValidPalindrome(unittest.TestCase):
    def test_classic(self):
        self.assertTrue(valid_palindrome("A man, a plan, a canal: Panama"))

    def test_not_palindrome(self):
        self.assertFalse(valid_palindrome("race a car"))

    def test_empty(self):
        self.assertTrue(valid_palindrome(""))

    def test_single_char(self):
        self.assertTrue(valid_palindrome("a"))

    def test_digits(self):
        self.assertTrue(valid_palindrome("12321"))


class TestCountAndSay(unittest.TestCase):
    def test_n1(self):
        self.assertEqual(count_and_say(1), "1")

    def test_n2(self):
        self.assertEqual(count_and_say(2), "11")

    def test_n3(self):
        self.assertEqual(count_and_say(3), "21")

    def test_n4(self):
        self.assertEqual(count_and_say(4), "1211")

    def test_n5(self):
        self.assertEqual(count_and_say(5), "111221")


class TestGroupAnagrams(unittest.TestCase):
    def test_basic(self):
        result = group_anagrams(["eat", "tea", "tan", "ate", "nat", "bat"])
        groups = [sorted(g) for g in result]
        self.assertIn(["ate", "eat", "tea"], groups)
        self.assertIn(["nat", "tan"], groups)
        self.assertIn(["bat"], groups)

    def test_empty_string(self):
        result = group_anagrams([""])
        self.assertEqual(result, [[""]])

    def test_single_char(self):
        result = group_anagrams(["a"])
        self.assertEqual(result, [["a"]])


class TestLongestCommonPrefix(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(longest_common_prefix(["flower", "flow", "flight"]), "fl")

    def test_no_common(self):
        self.assertEqual(longest_common_prefix(["dog", "racecar", "car"]), "")

    def test_full_match(self):
        self.assertEqual(longest_common_prefix(["abc", "abc", "abc"]), "abc")

    def test_empty_list(self):
        self.assertEqual(longest_common_prefix([]), "")

    def test_single_element(self):
        self.assertEqual(longest_common_prefix(["alone"]), "alone")


class TestStringCompression(unittest.TestCase):
    def test_basic(self):
        chars = ["a", "a", "b", "b", "c", "c", "c"]
        k = string_compression(chars)
        self.assertEqual(k, 6)
        self.assertEqual(chars[:k], ["a", "2", "b", "2", "c", "3"])

    def test_no_compression(self):
        chars = ["a", "b", "c"]
        k = string_compression(chars)
        self.assertEqual(k, 3)
        self.assertEqual(chars[:k], ["a", "b", "c"])

    def test_long_run(self):
        chars = ["a"] * 12
        k = string_compression(chars)
        self.assertEqual(k, 3)
        self.assertEqual(chars[:k], ["a", "1", "2"])


# ═════════════════════════════════════════════════════════════════════════════
# LINKED LIST
# ═════════════════════════════════════════════════════════════════════════════

class TestReverseLinkedList(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(to_python_list(reverse_linked_list(make_list([1, 2, 3, 4, 5]))), [5, 4, 3, 2, 1])

    def test_single(self):
        self.assertEqual(to_python_list(reverse_linked_list(make_list([1]))), [1])

    def test_two_nodes(self):
        self.assertEqual(to_python_list(reverse_linked_list(make_list([1, 2]))), [2, 1])

    def test_empty(self):
        self.assertIsNone(reverse_linked_list(None))


class TestDetectCycle(unittest.TestCase):
    def test_no_cycle(self):
        self.assertFalse(detect_cycle(make_list([1, 2, 3])))

    def test_cycle_at_0(self):
        self.assertTrue(detect_cycle(make_cycle([3, 2, 0, -4], 1)))

    def test_cycle_self(self):
        self.assertTrue(detect_cycle(make_cycle([1, 2], 0)))

    def test_empty(self):
        self.assertFalse(detect_cycle(None))


class TestMergeTwoSortedLists(unittest.TestCase):
    def test_basic(self):
        result = merge_two_sorted_lists(make_list([1, 2, 4]), make_list([1, 3, 4]))
        self.assertEqual(to_python_list(result), [1, 1, 2, 3, 4, 4])

    def test_one_empty(self):
        result = merge_two_sorted_lists(None, make_list([1, 2]))
        self.assertEqual(to_python_list(result), [1, 2])

    def test_both_empty(self):
        self.assertIsNone(merge_two_sorted_lists(None, None))

    def test_disjoint(self):
        result = merge_two_sorted_lists(make_list([1, 2, 3]), make_list([4, 5, 6]))
        self.assertEqual(to_python_list(result), [1, 2, 3, 4, 5, 6])


class TestMiddleOfLinkedList(unittest.TestCase):
    def test_odd_length(self):
        self.assertEqual(middle_of_linked_list(make_list([1, 2, 3, 4, 5])).val, 3)

    def test_even_length(self):
        # For even length, returns second middle
        self.assertEqual(middle_of_linked_list(make_list([1, 2, 3, 4])).val, 3)

    def test_single(self):
        self.assertEqual(middle_of_linked_list(make_list([1])).val, 1)


class TestRemoveNthFromEnd(unittest.TestCase):
    def test_basic(self):
        result = remove_nth_from_end(make_list([1, 2, 3, 4, 5]), 2)
        self.assertEqual(to_python_list(result), [1, 2, 3, 5])

    def test_remove_head(self):
        result = remove_nth_from_end(make_list([1, 2]), 2)
        self.assertEqual(to_python_list(result), [2])

    def test_remove_tail(self):
        result = remove_nth_from_end(make_list([1, 2, 3]), 1)
        self.assertEqual(to_python_list(result), [1, 2])

    def test_single_node(self):
        result = remove_nth_from_end(make_list([1]), 1)
        self.assertIsNone(result)


# ═════════════════════════════════════════════════════════════════════════════
# STACK
# ═════════════════════════════════════════════════════════════════════════════

class TestInfixToPostfix(unittest.TestCase):
    def test_simple_add(self):
        self.assertEqual(infix_to_postfix("3 + 4"), "3 4 +")

    def test_precedence(self):
        self.assertEqual(infix_to_postfix("3 + 4 * 2"), "3 4 2 * +")

    def test_parentheses(self):
        self.assertEqual(infix_to_postfix("( 3 + 4 ) * 2"), "3 4 + 2 *")

    def test_complex(self):
        result = infix_to_postfix("5 + ( ( 1 + 2 ) * 4 ) - 3")
        self.assertEqual(result, "5 1 2 + 4 * + 3 -")


class TestNextGreaterElement(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(next_greater_element([4, 1, 2]), [-1, 2, -1])

    def test_descending(self):
        self.assertEqual(next_greater_element([5, 4, 3, 2, 1]), [-1, -1, -1, -1, -1])

    def test_ascending(self):
        self.assertEqual(next_greater_element([1, 2, 3, 4]), [2, 3, 4, -1])

    def test_with_duplicates(self):
        self.assertEqual(next_greater_element([2, 1, 2, 4, 3]), [4, 2, 4, -1, -1])


class TestMinStack(unittest.TestCase):
    def test_basic(self):
        ms = MinStack()
        ms.push(-2)
        ms.push(0)
        ms.push(-3)
        self.assertEqual(ms.get_min(), -3)
        ms.pop()
        self.assertEqual(ms.top(), 0)
        self.assertEqual(ms.get_min(), -2)

    def test_push_pop_sequence(self):
        ms = MinStack()
        ms.push(5)
        ms.push(3)
        ms.push(7)
        self.assertEqual(ms.get_min(), 3)
        ms.pop()
        self.assertEqual(ms.get_min(), 3)
        ms.pop()
        self.assertEqual(ms.get_min(), 5)

    def test_min_after_reinsert(self):
        ms = MinStack()
        ms.push(1)
        ms.push(2)
        ms.pop()
        self.assertEqual(ms.get_min(), 1)


class TestLargestRectangleHistogram(unittest.TestCase):
    def test_classic(self):
        self.assertEqual(largest_rectangle_histogram([2, 1, 5, 6, 2, 3]), 10)

    def test_uniform(self):
        self.assertEqual(largest_rectangle_histogram([2, 2, 2, 2]), 8)

    def test_single(self):
        self.assertEqual(largest_rectangle_histogram([5]), 5)

    def test_ascending(self):
        self.assertEqual(largest_rectangle_histogram([1, 2, 3, 4, 5]), 9)

    def test_descending(self):
        self.assertEqual(largest_rectangle_histogram([5, 4, 3, 2, 1]), 9)


class TestReverseFirstKQueue(unittest.TestCase):
    def test_basic(self):
        q = collections.deque([1, 2, 3, 4, 5])
        result = reverse_first_k_queue(q, 3)
        self.assertEqual(list(result), [3, 2, 1, 4, 5])

    def test_entire_queue(self):
        q = collections.deque([1, 2, 3])
        result = reverse_first_k_queue(q, 3)
        self.assertEqual(list(result), [3, 2, 1])

    def test_k_one(self):
        q = collections.deque([1, 2, 3])
        result = reverse_first_k_queue(q, 1)
        self.assertEqual(list(result), [1, 2, 3])


# ═════════════════════════════════════════════════════════════════════════════
# BINARY TREE
# ═════════════════════════════════════════════════════════════════════════════

class TestLevelOrderTraversal(unittest.TestCase):
    def test_basic(self):
        root = TreeNode(3, TreeNode(9), TreeNode(20, TreeNode(15), TreeNode(7)))
        self.assertEqual(level_order_traversal(root), [[3], [9, 20], [15, 7]])

    def test_single_node(self):
        self.assertEqual(level_order_traversal(TreeNode(1)), [[1]])

    def test_empty(self):
        self.assertEqual(level_order_traversal(None), [])

    def test_left_skewed(self):
        root = TreeNode(1, TreeNode(2, TreeNode(3)))
        self.assertEqual(level_order_traversal(root), [[1], [2], [3]])


class TestMirrorTrees(unittest.TestCase):
    def test_mirror(self):
        p = TreeNode(1, TreeNode(2), TreeNode(3))
        q = TreeNode(1, TreeNode(3), TreeNode(2))
        self.assertTrue(mirror_trees(p, q))

    def test_not_mirror(self):
        p = TreeNode(1, TreeNode(2))
        q = TreeNode(1, TreeNode(2))
        self.assertFalse(mirror_trees(p, q))

    def test_both_none(self):
        self.assertTrue(mirror_trees(None, None))

    def test_one_none(self):
        self.assertFalse(mirror_trees(TreeNode(1), None))


class TestLowestCommonAncestorBST(unittest.TestCase):
    def _bst(self):
        return make_bst(6, 2, 8, 0, 4, 7, 9, 3, 5)

    def test_lca_deep(self):
        root = self._bst()
        p = TreeNode(2)
        q = TreeNode(4)
        self.assertEqual(lowest_common_ancestor_bst(root, p, q).val, 2)

    def test_lca_root(self):
        root = self._bst()
        p = TreeNode(2)
        q = TreeNode(8)
        self.assertEqual(lowest_common_ancestor_bst(root, p, q).val, 6)

    def test_one_is_ancestor(self):
        root = self._bst()
        p = TreeNode(2)
        q = TreeNode(3)
        self.assertEqual(lowest_common_ancestor_bst(root, p, q).val, 2)


class TestSerializeDeserialize(unittest.TestCase):
    def _roundtrip(self, root):
        return deserialize(serialize(root))

    def test_basic(self):
        root = TreeNode(1, TreeNode(2), TreeNode(3, TreeNode(4), TreeNode(5)))
        result = self._roundtrip(root)
        self.assertEqual(level_order_traversal(result), level_order_traversal(root))

    def test_single_node(self):
        result = self._roundtrip(TreeNode(42))
        self.assertEqual(result.val, 42)

    def test_empty(self):
        self.assertIsNone(self._roundtrip(None))

    def test_left_skewed(self):
        root = TreeNode(1, TreeNode(2, TreeNode(3)))
        result = self._roundtrip(root)
        self.assertEqual(level_order_traversal(result), [[1], [2], [3]])


class TestValidateBST(unittest.TestCase):
    def test_valid(self):
        root = make_bst(5, 3, 7, 1, 4)
        self.assertTrue(validate_bst(root))

    def test_invalid(self):
        root = TreeNode(5, TreeNode(3), TreeNode(7))
        root.left.right = TreeNode(6)   # 6 > 5, violates BST
        self.assertFalse(validate_bst(root))

    def test_single_node(self):
        self.assertTrue(validate_bst(TreeNode(1)))

    def test_empty(self):
        self.assertTrue(validate_bst(None))


# ═════════════════════════════════════════════════════════════════════════════
# GRAPHS
# ═════════════════════════════════════════════════════════════════════════════

class TestTopologicalSort(unittest.TestCase):
    def test_linear(self):
        order = topological_sort(4, [(0, 1), (1, 2), (2, 3)])
        self.assertEqual(order, [0, 1, 2, 3])

    def test_branching(self):
        order = topological_sort(6, [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)])
        # Verify each dependency comes after its prerequisite
        pos = {v: i for i, v in enumerate(order)}
        for u, v in [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]:
            self.assertLess(pos[u], pos[v])

    def test_cycle_returns_empty(self):
        self.assertEqual(topological_sort(3, [(0, 1), (1, 2), (2, 0)]), [])

    def test_no_edges(self):
        self.assertEqual(len(topological_sort(3, [])), 3)


class TestDetectCycleDirected(unittest.TestCase):
    def test_has_cycle(self):
        self.assertTrue(detect_cycle_directed(3, [(0, 1), (1, 2), (2, 0)]))

    def test_no_cycle(self):
        self.assertFalse(detect_cycle_directed(4, [(0, 1), (1, 2), (2, 3)]))

    def test_self_loop(self):
        self.assertTrue(detect_cycle_directed(2, [(0, 1), (1, 1)]))

    def test_disconnected_no_cycle(self):
        self.assertFalse(detect_cycle_directed(4, [(0, 1), (2, 3)]))


class TestNumberOfIslands(unittest.TestCase):
    def test_basic(self):
        grid = [["1","1","1","1","0"],
                ["1","1","0","1","0"],
                ["1","1","0","0","0"],
                ["0","0","0","0","0"]]
        self.assertEqual(number_of_islands(grid), 1)

    def test_multiple_islands(self):
        grid = [["1","1","0","0","0"],
                ["1","1","0","0","0"],
                ["0","0","1","0","0"],
                ["0","0","0","1","1"]]
        self.assertEqual(number_of_islands(grid), 3)

    def test_no_islands(self):
        self.assertEqual(number_of_islands([["0","0"],["0","0"]]), 0)

    def test_all_land(self):
        self.assertEqual(number_of_islands([["1","1"],["1","1"]]), 1)

    def test_diagonal_not_connected(self):
        grid = [["1","0"],["0","1"]]
        self.assertEqual(number_of_islands(grid), 2)


class TestShortestPathUnweighted(unittest.TestCase):
    def _graph(self):
        # 0-1-2-3, with 0-2 shortcut
        g = [[] for _ in range(4)]
        for u, v in [(0, 1), (1, 2), (2, 3), (0, 2)]:
            g[u].append(v)
            g[v].append(u)
        return g

    def test_distances_from_0(self):
        d = shortest_path_unweighted(self._graph(), 0)
        self.assertEqual(d, [0, 1, 1, 2])

    def test_unreachable(self):
        g = [[1], [0], [3], [2]]   # two disconnected pairs
        d = shortest_path_unweighted(g, 0)
        self.assertEqual(d[2], -1)
        self.assertEqual(d[3], -1)

    def test_source_to_itself(self):
        g = [[1], [0]]
        d = shortest_path_unweighted(g, 0)
        self.assertEqual(d[0], 0)


class TestBipartiteCheck(unittest.TestCase):
    def test_bipartite_cycle_of_4(self):
        g = [[1, 3], [0, 2], [1, 3], [0, 2]]
        self.assertTrue(bipartite_check(g))

    def test_not_bipartite_triangle(self):
        g = [[1, 2], [0, 2], [0, 1]]
        self.assertFalse(bipartite_check(g))

    def test_bipartite_path(self):
        g = [[1], [0, 2], [1]]
        self.assertTrue(bipartite_check(g))

    def test_disconnected_bipartite(self):
        g = [[1], [0], [3], [2]]
        self.assertTrue(bipartite_check(g))


class TestTravelingSalesman(unittest.TestCase):
    def test_3_cities(self):
        dist = [[0, 10, 15], [10, 0, 35], [15, 35, 0]]
        self.assertEqual(traveling_salesman(dist), 60)

    def test_4_cities(self):
        dist = [
            [0, 20, 42, 25],
            [20,  0, 30, 34],
            [42, 30,  0, 10],
            [25, 34, 10,  0],
        ]
        self.assertEqual(traveling_salesman(dist), 85)

    def test_symmetric(self):
        dist = [[0, 1, 1], [1, 0, 1], [1, 1, 0]]
        self.assertEqual(traveling_salesman(dist), 3)


class TestConnectedCitiesShortestPath(unittest.TestCase):
    def test_basic(self):
        edges = [(0, 1, 4), (0, 2, 1), (2, 1, 2), (1, 3, 1)]
        dist = connected_cities_shortest_path(4, edges, 0)
        self.assertEqual(dist[0], 0)
        self.assertEqual(dist[1], 3)   # 0->2->1
        self.assertEqual(dist[2], 1)
        self.assertEqual(dist[3], 4)

    def test_unreachable(self):
        edges = [(0, 1, 5)]
        dist = connected_cities_shortest_path(3, edges, 0)
        self.assertEqual(dist[2], math.inf)

    def test_direct_path(self):
        edges = [(0, 1, 7), (0, 2, 3), (2, 1, 2)]
        dist = connected_cities_shortest_path(3, edges, 0)
        self.assertEqual(dist[1], 5)   # 0->2->1 is shorter


# ═════════════════════════════════════════════════════════════════════════════
# DYNAMIC PROGRAMMING
# ═════════════════════════════════════════════════════════════════════════════

class TestKnapsack01(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(knapsack_01([1, 3, 4, 5], [1, 4, 5, 7], 7), 9)

    def test_zero_capacity(self):
        self.assertEqual(knapsack_01([1, 2], [10, 20], 0), 0)

    def test_one_item_fits(self):
        self.assertEqual(knapsack_01([3], [5], 5), 5)

    def test_one_item_too_heavy(self):
        self.assertEqual(knapsack_01([10], [5], 5), 0)

    def test_all_items_fit(self):
        self.assertEqual(knapsack_01([1, 2, 3], [6, 10, 12], 10), 28)


class TestLongestIncreasingSubsequence(unittest.TestCase):
    def test_classic(self):
        self.assertEqual(longest_increasing_subsequence([10, 9, 2, 5, 3, 7, 101, 18]), 4)

    def test_all_increasing(self):
        self.assertEqual(longest_increasing_subsequence([1, 2, 3, 4, 5]), 5)

    def test_all_decreasing(self):
        self.assertEqual(longest_increasing_subsequence([5, 4, 3, 2, 1]), 1)

    def test_single(self):
        self.assertEqual(longest_increasing_subsequence([7]), 1)

    def test_duplicates(self):
        self.assertEqual(longest_increasing_subsequence([2, 2, 2, 2]), 1)


class TestCoinChangeMinCoins(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(coin_change_min_coins([1, 5, 11], 15), 3)

    def test_impossible(self):
        self.assertEqual(coin_change_min_coins([2], 3), -1)

    def test_zero_amount(self):
        self.assertEqual(coin_change_min_coins([1, 2, 5], 0), 0)

    def test_single_coin(self):
        self.assertEqual(coin_change_min_coins([5], 25), 5)

    def test_classic(self):
        self.assertEqual(coin_change_min_coins([1, 2, 5], 11), 3)


class TestWordBreak(unittest.TestCase):
    def test_true(self):
        self.assertTrue(word_break("leetcode", ["leet", "code"]))

    def test_false(self):
        self.assertFalse(word_break("catsandog", ["cats", "dog", "sand", "an", "cat"]))

    def test_repeated_word(self):
        self.assertTrue(word_break("applepenapple", ["apple", "pen"]))

    def test_empty_string(self):
        self.assertTrue(word_break("", ["a", "b"]))

    def test_single_char(self):
        self.assertTrue(word_break("a", ["a"]))


class TestClimbingStairs(unittest.TestCase):
    def test_n1(self):
        self.assertEqual(climbing_stairs(1), 1)

    def test_n2(self):
        self.assertEqual(climbing_stairs(2), 2)

    def test_n5(self):
        self.assertEqual(climbing_stairs(5), 8)

    def test_n10(self):
        self.assertEqual(climbing_stairs(10), 89)

    def test_fibonacci_property(self):
        # climbing_stairs(n) == fib(n+1)
        self.assertEqual(climbing_stairs(6), 13)


# ═════════════════════════════════════════════════════════════════════════════
# GREEDY
# ═════════════════════════════════════════════════════════════════════════════

class TestJobSequencing(unittest.TestCase):
    def test_basic(self):
        jobs = [(1, 2, 100), (2, 1, 19), (3, 2, 27), (4, 1, 25), (5, 3, 15)]
        count, profit = job_sequencing(jobs)
        self.assertEqual(count, 3)
        self.assertEqual(profit, 142)

    def test_single_job(self):
        count, profit = job_sequencing([(1, 1, 50)])
        self.assertEqual(count, 1)
        self.assertEqual(profit, 50)

    def test_all_same_deadline(self):
        jobs = [(1, 1, 10), (2, 1, 20), (3, 1, 30)]
        count, profit = job_sequencing(jobs)
        self.assertEqual(count, 1)
        self.assertEqual(profit, 30)


class TestMinimumPlatforms(unittest.TestCase):
    def test_basic(self):
        arrivals =   [900, 940, 950, 1100, 1500, 1800]
        departures = [910, 1200, 1120, 1130, 1900, 2000]
        self.assertEqual(minimum_platforms(arrivals, departures), 3)

    def test_no_overlap(self):
        self.assertEqual(minimum_platforms([100, 300], [200, 400]), 1)

    def test_all_overlap(self):
        self.assertEqual(minimum_platforms([100, 100, 100], [200, 200, 200]), 3)

    def test_single_train(self):
        self.assertEqual(minimum_platforms([600], [900]), 1)


class TestActivitySelection(unittest.TestCase):
    def test_basic(self):
        start  = [1, 3, 0, 5, 8, 5]
        finish = [2, 4, 6, 7, 9, 9]
        selected = activity_selection(start, finish)
        # Classic greedy result: activities 0, 1, 3, 4
        self.assertEqual(len(selected), 4)
        # Verify no two selected activities overlap
        for i in range(len(selected) - 1):
            self.assertGreaterEqual(start[selected[i + 1]], finish[selected[i]])

    def test_no_overlap(self):
        selected = activity_selection([1, 3, 5], [2, 4, 6])
        self.assertEqual(len(selected), 3)

    def test_all_overlap(self):
        selected = activity_selection([1, 1, 1], [10, 10, 10])
        self.assertEqual(len(selected), 1)


class TestMinCostConnectRopes(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(min_cost_connect_ropes([4, 3, 2, 6]), 29)

    def test_two_ropes(self):
        self.assertEqual(min_cost_connect_ropes([1, 2]), 3)

    def test_single_rope(self):
        self.assertEqual(min_cost_connect_ropes([5]), 0)

    def test_equal_ropes(self):
        self.assertEqual(min_cost_connect_ropes([1, 1, 1, 1]), 8)


# ═════════════════════════════════════════════════════════════════════════════
# HEAPS
# ═════════════════════════════════════════════════════════════════════════════

class TestKLargestElements(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(k_largest_elements([3, 1, 4, 1, 5, 9, 2, 6], 3), [9, 6, 5])

    def test_k_equals_n(self):
        self.assertEqual(sorted(k_largest_elements([3, 1, 2], 3), reverse=True), [3, 2, 1])

    def test_k_one(self):
        self.assertEqual(k_largest_elements([5, 3, 1], 1), [5])

    def test_with_negatives(self):
        self.assertEqual(k_largest_elements([-1, -2, -3], 2), [-1, -2])


class TestMedianFinder(unittest.TestCase):
    def test_odd_count(self):
        mf = MedianFinder()
        for n in [1, 2, 3]:
            mf.add_num(n)
        self.assertEqual(mf.find_median(), 2.0)

    def test_even_count(self):
        mf = MedianFinder()
        mf.add_num(1)
        mf.add_num(2)
        self.assertEqual(mf.find_median(), 1.5)

    def test_streaming(self):
        mf = MedianFinder()
        mf.add_num(5)
        self.assertEqual(mf.find_median(), 5.0)
        mf.add_num(3)
        self.assertEqual(mf.find_median(), 4.0)
        mf.add_num(8)
        self.assertEqual(mf.find_median(), 5.0)

    def test_duplicates(self):
        mf = MedianFinder()
        for n in [2, 2, 2]:
            mf.add_num(n)
        self.assertEqual(mf.find_median(), 2.0)


class TestMergeKSortedArrays(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(
            merge_k_sorted_arrays([[1, 4, 7], [2, 5, 8], [3, 6, 9]]),
            list(range(1, 10)),
        )

    def test_single_array(self):
        self.assertEqual(merge_k_sorted_arrays([[1, 2, 3]]), [1, 2, 3])

    def test_with_empty_array(self):
        self.assertEqual(merge_k_sorted_arrays([[1, 3], [], [2, 4]]), [1, 2, 3, 4])

    def test_arrays_of_different_lengths(self):
        self.assertEqual(merge_k_sorted_arrays([[1], [2, 3, 4]]), [1, 2, 3, 4])


# ═════════════════════════════════════════════════════════════════════════════
# BIT MANIPULATION
# ═════════════════════════════════════════════════════════════════════════════

class TestCountBits(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(count_bits(5), [0, 1, 1, 2, 1, 2])

    def test_zero(self):
        self.assertEqual(count_bits(0), [0])

    def test_power_of_two(self):
        # Powers of two have exactly one 1-bit
        result = count_bits(8)
        self.assertEqual(result[8], 1)

    def test_all_ones(self):
        self.assertEqual(count_bits(7)[-1], 3)  # 7 = 0b111


class TestMissingNumber(unittest.TestCase):
    def test_basic(self):
        self.assertEqual(missing_number([3, 0, 1]), 2)

    def test_missing_last(self):
        self.assertEqual(missing_number([0, 1, 2]), 3)

    def test_missing_first(self):
        self.assertEqual(missing_number([1, 2, 3]), 0)

    def test_single_element(self):
        self.assertEqual(missing_number([1]), 0)
        self.assertEqual(missing_number([0]), 1)


class TestReverseBits(unittest.TestCase):
    def test_known_value(self):
        # 43261596  = 0b00000010100101000001111010011100
        # reversed  = 0b00111001011110000010100101000000
        self.assertEqual(reverse_bits(43261596), 964176192)

    def test_zero(self):
        self.assertEqual(reverse_bits(0), 0)

    def test_max_uint32(self):
        self.assertEqual(reverse_bits(0xFFFFFFFF), 0xFFFFFFFF)

    def test_involution(self):
        n = 12345
        self.assertEqual(reverse_bits(reverse_bits(n)), n)


class TestXorAllSubsets(unittest.TestCase):
    def test_single(self):
        self.assertEqual(xor_all_subsets([5]), 5)

    def test_two_elements(self):
        self.assertEqual(xor_all_subsets([1, 2]), 3)

    def test_cancels(self):
        # XOR of [a, a] == 0
        self.assertEqual(xor_all_subsets([7, 7]), 0)

    def test_multiple(self):
        self.assertEqual(xor_all_subsets([1, 2, 3]), 0)  # 1^2^3 == 0


class TestPowerOfTwo(unittest.TestCase):
    def test_powers(self):
        for exp in range(0, 16):
            self.assertTrue(power_of_two(2 ** exp))

    def test_non_powers(self):
        for n in [0, 3, 5, 6, 7, 9, 10, 12, 14, 15]:
            self.assertFalse(power_of_two(n))

    def test_negative(self):
        self.assertFalse(power_of_two(-4))


# ═════════════════════════════════════════════════════════════════════════════
# TRIE
# ═════════════════════════════════════════════════════════════════════════════

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        for w in ["apple", "app", "apt", "banana"]:
            self.trie.insert(w)

    def test_search_existing(self):
        self.assertTrue(self.trie.search("apple"))
        self.assertTrue(self.trie.search("app"))

    def test_search_missing(self):
        self.assertFalse(self.trie.search("ap"))
        self.assertFalse(self.trie.search("apples"))

    def test_starts_with(self):
        self.assertTrue(self.trie.starts_with("ap"))
        self.assertTrue(self.trie.starts_with("ban"))

    def test_starts_with_missing(self):
        self.assertFalse(self.trie.starts_with("xyz"))

    def test_empty_prefix(self):
        self.assertTrue(self.trie.starts_with(""))

    def test_insert_and_search(self):
        self.trie.insert("cherry")
        self.assertTrue(self.trie.search("cherry"))
        self.assertFalse(self.trie.search("cherr"))


class TestAutocomplete(unittest.TestCase):
    def setUp(self):
        self.ac = Autocomplete()
        for w in ["apple", "app", "application", "apt", "banana"]:
            self.ac.insert(w)

    def test_prefix_app(self):
        self.assertEqual(sorted(self.ac.suggestions("app")), ["app", "apple", "application"])

    def test_prefix_ap(self):
        self.assertEqual(sorted(self.ac.suggestions("ap")), ["app", "apple", "application", "apt"])

    def test_no_match(self):
        self.assertEqual(self.ac.suggestions("xyz"), [])

    def test_full_word(self):
        self.assertEqual(self.ac.suggestions("apple"), ["apple"])

    def test_empty_prefix(self):
        results = self.ac.suggestions("")
        self.assertEqual(sorted(results), ["app", "apple", "application", "apt", "banana"])


class TestLongestPrefixMatch(unittest.TestCase):
    def setUp(self):
        self.lpm = LongestPrefixMatch()
        for w in ["app", "apple", "ap", "application"]:
            self.lpm.insert(w)

    def test_finds_shortest_match(self):
        # "ap" is the shortest registered prefix of "application"
        self.assertEqual(self.lpm.longest_prefix("application"), "ap")

    def test_exact_match(self):
        self.assertEqual(self.lpm.longest_prefix("app"), "app")

    def test_no_match(self):
        self.assertEqual(self.lpm.longest_prefix("xyz"), "")

    def test_partial_match(self):
        self.assertEqual(self.lpm.longest_prefix("apt"), "ap")


# ═════════════════════════════════════════════════════════════════════════════
# HUFFMAN ENCODING
# ═════════════════════════════════════════════════════════════════════════════

class TestHuffmanEncoding(unittest.TestCase):
    def test_all_chars_present(self):
        codes = huffman_encoding("abracadabra")
        for ch in "abcdr":
            self.assertIn(ch, codes)

    def test_unique_codes(self):
        codes = huffman_encoding("abcde")
        values = list(codes.values())
        self.assertEqual(len(values), len(set(values)))

    def test_prefix_free(self):
        codes = huffman_encoding("aabbccdd")
        code_list = list(codes.values())
        for i, c1 in enumerate(code_list):
            for j, c2 in enumerate(code_list):
                if i != j:
                    self.assertFalse(c2.startswith(c1),
                                     f"'{c1}' is a prefix of '{c2}' — not prefix-free")

    def test_single_char(self):
        codes = huffman_encoding("aaaa")
        self.assertIn("a", codes)
        self.assertEqual(codes["a"], "0")

    def test_weighted_frequency(self):
        # More frequent character must get a shorter or equal-length code
        codes = huffman_encoding("aaaaab")
        self.assertLessEqual(len(codes["a"]), len(codes["b"]))

    def test_decode_roundtrip(self):
        text = "hello huffman"
        codes = huffman_encoding(text)
        encoded = "".join(codes[ch] for ch in text)
        # Build reverse map to decode
        reverse = {v: k for k, v in codes.items()}
        decoded, buf = "", ""
        for bit in encoded:
            buf += bit
            if buf in reverse:
                decoded += reverse[buf]
                buf = ""
        self.assertEqual(decoded, text)


# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    unittest.main(verbosity=2)
