"""
Python translation of guiff0/fisrtApp — Java algorithms library.
Covers all modules listed in the repo README.
"""

from __future__ import annotations
from typing import Optional
import heapq, math, collections


# ─────────────────────────────────────────────────────────────────────────────
# ARRAYS
# ─────────────────────────────────────────────────────────────────────────────

def two_sum(nums: list[int], target: int) -> list[int]:
    """Return indices of two numbers that add to target."""
    seen: dict[int, int] = {}
    for i, n in enumerate(nums):
        complement = target - n
        if complement in seen:
            return [seen[complement], i]
        seen[n] = i
    return []


def max_subarray(nums: list[int]) -> int:
    """Kadane's algorithm — maximum subarray sum."""
    max_sum = cur = nums[0]
    for n in nums[1:]:
        cur = max(n, cur + n)
        max_sum = max(max_sum, cur)
    return max_sum


def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    """Merge all overlapping intervals."""
    intervals.sort()
    merged = [intervals[0]]
    for start, end in intervals[1:]:
        if start <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], end)
        else:
            merged.append([start, end])
    return merged


def min_rotated_array(nums: list[int]) -> int:
    """Find minimum in a rotated sorted array (binary search)."""
    lo, hi = 0, len(nums) - 1
    while lo < hi:
        mid = (lo + hi) // 2
        if nums[mid] > nums[hi]:
            lo = mid + 1
        else:
            hi = mid
    return nums[lo]


def trapping_rainwater(height: list[int]) -> int:
    """Two-pointer approach for trapping rainwater."""
    lo, hi = 0, len(height) - 1
    left_max = right_max = water = 0
    while lo <= hi:
        if height[lo] <= height[hi]:
            if height[lo] >= left_max:
                left_max = height[lo]
            else:
                water += left_max - height[lo]
            lo += 1
        else:
            if height[hi] >= right_max:
                right_max = height[hi]
            else:
                water += right_max - height[hi]
            hi -= 1
    return water


def three_sum(nums: list[int]) -> list[list[int]]:
    """All unique triplets that sum to zero."""
    nums.sort()
    result = []
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        lo, hi = i + 1, len(nums) - 1
        while lo < hi:
            s = nums[i] + nums[lo] + nums[hi]
            if s == 0:
                result.append([nums[i], nums[lo], nums[hi]])
                while lo < hi and nums[lo] == nums[lo + 1]:
                    lo += 1
                while lo < hi and nums[hi] == nums[hi - 1]:
                    hi -= 1
                lo += 1
                hi -= 1
            elif s < 0:
                lo += 1
            else:
                hi -= 1
    return result


def product_except_self(nums: list[int]) -> list[int]:
    """Product of every element except self — O(n), no division."""
    n = len(nums)
    out = [1] * n
    prefix = 1
    for i in range(n):
        out[i] = prefix
        prefix *= nums[i]
    suffix = 1
    for i in range(n - 1, -1, -1):
        out[i] *= suffix
        suffix *= nums[i]
    return out


def container_with_most_water(height: list[int]) -> int:
    """Two-pointer approach for container with most water."""
    lo, hi = 0, len(height) - 1
    max_water = 0
    while lo < hi:
        max_water = max(max_water, min(height[lo], height[hi]) * (hi - lo))
        if height[lo] < height[hi]:
            lo += 1
        else:
            hi -= 1
    return max_water


def remove_duplicates_sorted(nums: list[int]) -> int:
    """Remove duplicates in-place from sorted array; return new length."""
    if not nums:
        return 0
    k = 1
    for i in range(1, len(nums)):
        if nums[i] != nums[i - 1]:
            nums[k] = nums[i]
            k += 1
    return k


def rotate_array(nums: list[int], k: int) -> None:
    """Rotate array to the right by k steps (in-place, three-reverse trick)."""
    n = len(nums)
    k %= n
    nums.reverse()
    nums[:k] = nums[:k][::-1]
    nums[k:] = nums[k:][::-1]


# ─────────────────────────────────────────────────────────────────────────────
# STRINGS
# ─────────────────────────────────────────────────────────────────────────────

def anagram_check(s: str, t: str) -> bool:
    return collections.Counter(s) == collections.Counter(t)


def longest_substring_no_repeat(s: str) -> int:
    """Sliding window — longest substring without repeating characters."""
    char_index: dict[str, int] = {}
    best = start = 0
    for i, ch in enumerate(s):
        if ch in char_index and char_index[ch] >= start:
            start = char_index[ch] + 1
        char_index[ch] = i
        best = max(best, i - start + 1)
    return best


def longest_palindromic_substring(s: str) -> str:
    """Expand-around-center for longest palindromic substring."""
    def expand(l: int, r: int) -> str:
        while l >= 0 and r < len(s) and s[l] == s[r]:
            l -= 1
            r += 1
        return s[l + 1:r]

    best = ""
    for i in range(len(s)):
        for p in (expand(i, i), expand(i, i + 1)):
            if len(p) > len(best):
                best = p
    return best


def reverse_words(s: str) -> str:
    return " ".join(s.split()[::-1])


def atoi(s: str) -> int:
    """String to integer with sign and overflow handling."""
    s = s.lstrip()
    if not s:
        return 0
    sign = -1 if s[0] == '-' else 1
    s = s[1:] if s[0] in ('+', '-') else s
    num = 0
    for ch in s:
        if not ch.isdigit():
            break
        num = num * 10 + int(ch)
    result = sign * num
    INT_MIN, INT_MAX = -(2 ** 31), 2 ** 31 - 1
    return max(INT_MIN, min(INT_MAX, result))


def valid_palindrome(s: str) -> bool:
    filtered = [c.lower() for c in s if c.isalnum()]
    return filtered == filtered[::-1]


def count_and_say(n: int) -> str:
    result = "1"
    for _ in range(n - 1):
        nxt, i = "", 0
        while i < len(result):
            ch = result[i]
            count = 0
            while i < len(result) and result[i] == ch:
                i += 1
                count += 1
            nxt += str(count) + ch
        result = nxt
    return result


def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups: dict[tuple, list[str]] = collections.defaultdict(list)
    for s in strs:
        groups[tuple(sorted(s))].append(s)
    return list(groups.values())


def longest_common_prefix(strs: list[str]) -> str:
    if not strs:
        return ""
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
            if not prefix:
                return ""
    return prefix


def string_compression(chars: list[str]) -> int:
    """Compress list of chars in-place; return new length."""
    write = read = 0
    while read < len(chars):
        ch = chars[read]
        count = 0
        while read < len(chars) and chars[read] == ch:
            read += 1
            count += 1
        chars[write] = ch
        write += 1
        if count > 1:
            for digit in str(count):
                chars[write] = digit
                write += 1
    return write


# ─────────────────────────────────────────────────────────────────────────────
# LINKED LIST
# ─────────────────────────────────────────────────────────────────────────────

class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):
        self.val = val
        self.next = next


def reverse_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    prev = None
    curr = head
    while curr:
        nxt = curr.next
        curr.next = prev
        prev = curr
        curr = nxt
    return prev


def detect_cycle(head: Optional[ListNode]) -> bool:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next          # type: ignore[assignment]
        fast = fast.next.next
        if slow is fast:
            return True
    return False


def merge_two_sorted_lists(
    l1: Optional[ListNode], l2: Optional[ListNode]
) -> Optional[ListNode]:
    dummy = ListNode()
    curr = dummy
    while l1 and l2:
        if l1.val <= l2.val:
            curr.next = l1
            l1 = l1.next
        else:
            curr.next = l2
            l2 = l2.next
        curr = curr.next        # type: ignore[assignment]
    curr.next = l1 or l2
    return dummy.next


def middle_of_linked_list(head: Optional[ListNode]) -> Optional[ListNode]:
    slow = fast = head
    while fast and fast.next:
        slow = slow.next        # type: ignore[assignment]
        fast = fast.next.next
    return slow


def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n + 1):
        fast = fast.next        # type: ignore[assignment]
    while fast:
        fast = fast.next
        slow = slow.next        # type: ignore[assignment]
    slow.next = slow.next.next  # type: ignore[union-attr]
    return dummy.next


# ─────────────────────────────────────────────────────────────────────────────
# STACK
# ─────────────────────────────────────────────────────────────────────────────

def infix_to_postfix(expr: str) -> str:
    """Convert space-separated infix expression to postfix."""
    precedence = {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3}
    output: list[str] = []
    stack: list[str] = []
    for token in expr.split():
        if token.lstrip('-').isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while (stack and stack[-1] != '(' and
                   precedence.get(stack[-1], 0) >= precedence.get(token, 0)):
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())
    return " ".join(output)


def next_greater_element(nums: list[int]) -> list[int]:
    result = [-1] * len(nums)
    stack: list[int] = []
    for i, n in enumerate(nums):
        while stack and nums[stack[-1]] < n:
            result[stack.pop()] = n
        stack.append(i)
    return result


class MinStack:
    def __init__(self) -> None:
        self._stack: list[tuple[int, int]] = []  # (val, current_min)

    def push(self, val: int) -> None:
        cur_min = min(val, self._stack[-1][1]) if self._stack else val
        self._stack.append((val, cur_min))

    def pop(self) -> None:
        self._stack.pop()

    def top(self) -> int:
        return self._stack[-1][0]

    def get_min(self) -> int:
        return self._stack[-1][1]


def largest_rectangle_histogram(heights: list[int]) -> int:
    stack: list[tuple[int, int]] = []  # (index, height)
    max_area = 0
    for i, h in enumerate(heights + [0]):
        start = i
        while stack and stack[-1][1] > h:
            idx, ht = stack.pop()
            max_area = max(max_area, ht * (i - idx))
            start = idx
        stack.append((start, h))
    return max_area


def reverse_first_k_queue(q: collections.deque, k: int) -> collections.deque:
    stack = [q.popleft() for _ in range(k)]
    while stack:
        q.appendleft(stack.pop())
    for _ in range(len(q) - k):
        q.append(q.popleft())
    return q


# ─────────────────────────────────────────────────────────────────────────────
# BINARY TREE
# ─────────────────────────────────────────────────────────────────────────────

class TreeNode:
    def __init__(self, val: int = 0,
                 left: Optional["TreeNode"] = None,
                 right: Optional["TreeNode"] = None):
        self.val = val
        self.left = left
        self.right = right


def level_order_traversal(root: Optional[TreeNode]) -> list[list[int]]:
    if not root:
        return []
    result: list[list[int]] = []
    queue: collections.deque[TreeNode] = collections.deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        result.append(level)
    return result


def mirror_trees(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
    if not p and not q:
        return True
    if not p or not q or p.val != q.val:
        return False
    return mirror_trees(p.left, q.right) and mirror_trees(p.right, q.left)


def lowest_common_ancestor_bst(
    root: Optional[TreeNode], p: TreeNode, q: TreeNode
) -> Optional[TreeNode]:
    while root:
        if p.val < root.val and q.val < root.val:
            root = root.left
        elif p.val > root.val and q.val > root.val:
            root = root.right
        else:
            return root
    return None


def serialize(root: Optional[TreeNode]) -> str:
    if not root:
        return "null"
    return f"{root.val},{serialize(root.left)},{serialize(root.right)}"


def deserialize(data: str) -> Optional[TreeNode]:
    vals = iter(data.split(","))

    def build() -> Optional[TreeNode]:
        v = next(vals)
        if v == "null":
            return None
        node = TreeNode(int(v))
        node.left = build()
        node.right = build()
        return node

    return build()


def validate_bst(
    root: Optional[TreeNode],
    lo: float = -math.inf,
    hi: float = math.inf,
) -> bool:
    if not root:
        return True
    if not (lo < root.val < hi):
        return False
    return validate_bst(root.left, lo, root.val) and validate_bst(root.right, root.val, hi)


# ─────────────────────────────────────────────────────────────────────────────
# GRAPHS
# ─────────────────────────────────────────────────────────────────────────────

def topological_sort(num_vertices: int, edges: list[tuple[int, int]]) -> list[int]:
    """Kahn's BFS-based topological sort. Returns [] if a cycle is detected."""
    graph: list[list[int]] = [[] for _ in range(num_vertices)]
    in_degree = [0] * num_vertices
    for u, v in edges:
        graph[u].append(v)
        in_degree[v] += 1
    queue: collections.deque[int] = collections.deque(
        i for i in range(num_vertices) if in_degree[i] == 0
    )
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nb in graph[node]:
            in_degree[nb] -= 1
            if in_degree[nb] == 0:
                queue.append(nb)
    return order if len(order) == num_vertices else []


def detect_cycle_directed(num_vertices: int, edges: list[tuple[int, int]]) -> bool:
    """DFS with three-colour marking (white/gray/black)."""
    graph: list[list[int]] = [[] for _ in range(num_vertices)]
    for u, v in edges:
        graph[u].append(v)
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * num_vertices

    def dfs(node: int) -> bool:
        color[node] = GRAY
        for nb in graph[node]:
            if color[nb] == GRAY:
                return True
            if color[nb] == WHITE and dfs(nb):
                return True
        color[node] = BLACK
        return False

    return any(color[i] == WHITE and dfs(i) for i in range(num_vertices))


def number_of_islands(grid: list[list[str]]) -> int:
    """DFS flood-fill — modifies grid in place."""
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])

    def dfs(r: int, c: int) -> None:
        if r < 0 or r >= rows or c < 0 or c >= cols or grid[r][c] != '1':
            return
        grid[r][c] = '0'
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            dfs(r + dr, c + dc)

    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '1':
                dfs(r, c)
                count += 1
    return count


def shortest_path_unweighted(graph: list[list[int]], src: int) -> list[int]:
    """BFS shortest path distances in an unweighted graph (-1 = unreachable)."""
    dist = [-1] * len(graph)
    dist[src] = 0
    queue: collections.deque[int] = collections.deque([src])
    while queue:
        node = queue.popleft()
        for nb in graph[node]:
            if dist[nb] == -1:
                dist[nb] = dist[node] + 1
                queue.append(nb)
    return dist


def bipartite_check(graph: list[list[int]]) -> bool:
    """BFS two-colouring check for bipartiteness."""
    color = [-1] * len(graph)
    for start in range(len(graph)):
        if color[start] != -1:
            continue
        color[start] = 0
        queue: collections.deque[int] = collections.deque([start])
        while queue:
            node = queue.popleft()
            for nb in graph[node]:
                if color[nb] == -1:
                    color[nb] = 1 - color[node]
                    queue.append(nb)
                elif color[nb] == color[node]:
                    return False
    return True


def traveling_salesman(dist: list[list[int]]) -> int:
    """DP + Bitmask TSP — exact solution, practical up to ~20 cities."""
    n = len(dist)
    FULL = (1 << n) - 1
    dp = [[math.inf] * n for _ in range(1 << n)]
    dp[1][0] = 0
    for mask in range(1 << n):
        for u in range(n):
            if not (mask >> u & 1) or dp[mask][u] == math.inf:
                continue
            for v in range(n):
                if mask >> v & 1:
                    continue
                new_mask = mask | (1 << v)
                dp[new_mask][v] = min(dp[new_mask][v], dp[mask][u] + dist[u][v])
    return int(min(dp[FULL][v] + dist[v][0] for v in range(1, n)))


def connected_cities_shortest_path(
    n: int, edges: list[tuple[int, int, int]], src: int
) -> list[float]:
    """Dijkstra — shortest distances from src to every city."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, w in edges:
        graph[u].append((w, v))
        graph[v].append((w, u))
    dist = [math.inf] * n
    dist[src] = 0
    pq: list[tuple[float, int]] = [(0.0, src)]
    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for w, v in graph[u]:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                heapq.heappush(pq, (dist[v], v))
    return dist


# ─────────────────────────────────────────────────────────────────────────────
# DYNAMIC PROGRAMMING
# ─────────────────────────────────────────────────────────────────────────────

def knapsack_01(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(capacity + 1):
            dp[i][w] = dp[i - 1][w]
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
    return dp[n][capacity]


def longest_increasing_subsequence(nums: list[int]) -> int:
    """O(n log n) patience-sorting LIS."""
    tails: list[int] = []
    for n in nums:
        lo, hi = 0, len(tails)
        while lo < hi:
            mid = (lo + hi) // 2
            if tails[mid] < n:
                lo = mid + 1
            else:
                hi = mid
        if lo == len(tails):
            tails.append(n)
        else:
            tails[lo] = n
    return len(tails)


def coin_change_min_coins(coins: list[int], amount: int) -> int:
    dp = [math.inf] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for i in range(coin, amount + 1):
            dp[i] = min(dp[i], dp[i - coin] + 1)
    return int(dp[amount]) if dp[amount] != math.inf else -1


def word_break(s: str, word_dict: list[str]) -> bool:
    words = set(word_dict)
    dp = [False] * (len(s) + 1)
    dp[0] = True
    for i in range(1, len(s) + 1):
        for j in range(i):
            if dp[j] and s[j:i] in words:
                dp[i] = True
                break
    return dp[len(s)]


def climbing_stairs(n: int) -> int:
    if n <= 2:
        return n
    a, b = 1, 2
    for _ in range(3, n + 1):
        a, b = b, a + b
    return b


# ─────────────────────────────────────────────────────────────────────────────
# GREEDY
# ─────────────────────────────────────────────────────────────────────────────

def job_sequencing(jobs: list[tuple[int, int, int]]) -> tuple[int, int]:
    """jobs = [(id, deadline, profit)]. Returns (jobs_done, total_profit)."""
    jobs_sorted = sorted(jobs, key=lambda j: -j[2])
    max_deadline = max(j[1] for j in jobs_sorted)
    slot = [-1] * (max_deadline + 1)
    count = profit = 0
    for job_id, deadline, job_profit in jobs_sorted:
        for t in range(min(deadline, max_deadline), 0, -1):
            if slot[t] == -1:
                slot[t] = job_id
                count += 1
                profit += job_profit
                break
    return count, profit


def minimum_platforms(arrivals: list[int], departures: list[int]) -> int:
    arrivals = sorted(arrivals)
    departures = sorted(departures)
    platforms = max_platforms = 0
    i = j = 0
    while i < len(arrivals):
        if arrivals[i] <= departures[j]:
            platforms += 1
            i += 1
        else:
            platforms -= 1
            j += 1
        max_platforms = max(max_platforms, platforms)
    return max_platforms


def activity_selection(start: list[int], finish: list[int]) -> list[int]:
    activities = sorted(range(len(start)), key=lambda i: finish[i])
    selected = [activities[0]]
    last_finish = finish[activities[0]]
    for i in activities[1:]:
        if start[i] >= last_finish:
            selected.append(i)
            last_finish = finish[i]
    return selected


def min_cost_connect_ropes(ropes: list[int]) -> int:
    h = ropes[:]
    heapq.heapify(h)
    total = 0
    while len(h) > 1:
        a = heapq.heappop(h)
        b = heapq.heappop(h)
        total += a + b
        heapq.heappush(h, a + b)
    return total


# ─────────────────────────────────────────────────────────────────────────────
# HEAPS
# ─────────────────────────────────────────────────────────────────────────────

def k_largest_elements(nums: list[int], k: int) -> list[int]:
    return heapq.nlargest(k, nums)


class MedianFinder:
    def __init__(self) -> None:
        self._lo: list[int] = []   # max-heap (values stored negated)
        self._hi: list[int] = []   # min-heap

    def add_num(self, num: int) -> None:
        heapq.heappush(self._lo, -num)
        heapq.heappush(self._hi, -heapq.heappop(self._lo))
        if len(self._hi) > len(self._lo):
            heapq.heappush(self._lo, -heapq.heappop(self._hi))

    def find_median(self) -> float:
        if len(self._lo) > len(self._hi):
            return float(-self._lo[0])
        return (-self._lo[0] + self._hi[0]) / 2.0


def merge_k_sorted_arrays(arrays: list[list[int]]) -> list[int]:
    result: list[int] = []
    pq: list[tuple[int, int, int]] = []
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(pq, (arr[0], i, 0))
    while pq:
        val, i, j = heapq.heappop(pq)
        result.append(val)
        if j + 1 < len(arrays[i]):
            heapq.heappush(pq, (arrays[i][j + 1], i, j + 1))
    return result


# ─────────────────────────────────────────────────────────────────────────────
# BIT MANIPULATION
# ─────────────────────────────────────────────────────────────────────────────

def count_bits(n: int) -> list[int]:
    """dp[i] = number of 1-bits in i, for 0 .. n."""
    dp = [0] * (n + 1)
    for i in range(1, n + 1):
        dp[i] = dp[i >> 1] + (i & 1)
    return dp


def missing_number(nums: list[int]) -> int:
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)


def reverse_bits(n: int) -> int:
    result = 0
    for _ in range(32):
        result = (result << 1) | (n & 1)
        n >>= 1
    return result


def xor_all_subsets(nums: list[int]) -> int:
    """XOR of XOR of every subset equals XOR of all elements (when len > 1)."""
    if len(nums) == 1:
        return nums[0]
    result = 0
    for n in nums:
        result ^= n
    return result


def power_of_two(n: int) -> bool:
    return n > 0 and (n & (n - 1)) == 0


# ─────────────────────────────────────────────────────────────────────────────
# TRIE
# ─────────────────────────────────────────────────────────────────────────────

class TrieNode:
    def __init__(self) -> None:
        self.children: dict[str, "TrieNode"] = {}
        self.is_end = False


class Trie:
    def __init__(self) -> None:
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        node = self.root
        for ch in word:
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            node = node.children[ch]
        return True


class Autocomplete(Trie):
    def suggestions(self, prefix: str) -> list[str]:
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return []
            node = node.children[ch]
        results: list[str] = []
        self._dfs(node, list(prefix), results)
        return results

    def _dfs(self, node: TrieNode, path: list[str], results: list[str]) -> None:
        if node.is_end:
            results.append("".join(path))
        for ch, child in node.children.items():
            path.append(ch)
            self._dfs(child, path, results)
            path.pop()


class LongestPrefixMatch(Trie):
    def longest_prefix(self, query: str) -> str:
        node = self.root
        prefix: list[str] = []
        for ch in query:
            if ch not in node.children:
                break
            node = node.children[ch]
            prefix.append(ch)
            if node.is_end:
                return "".join(prefix)
        return "".join(prefix)


# ─────────────────────────────────────────────────────────────────────────────
# HUFFMAN ENCODING
# ─────────────────────────────────────────────────────────────────────────────

class _HuffmanNode:
    def __init__(self, char: Optional[str], freq: int,
                 left: Optional["_HuffmanNode"] = None,
                 right: Optional["_HuffmanNode"] = None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other: "_HuffmanNode") -> bool:
        return self.freq < other.freq


def huffman_encoding(text: str) -> dict[str, str]:
    """Return a Huffman code table for each character in text."""
    freq = collections.Counter(text)
    pq: list[_HuffmanNode] = [_HuffmanNode(ch, f) for ch, f in freq.items()]
    heapq.heapify(pq)
    while len(pq) > 1:
        l = heapq.heappop(pq)
        r = heapq.heappop(pq)
        heapq.heappush(pq, _HuffmanNode(None, l.freq + r.freq, l, r))
    codes: dict[str, str] = {}

    def build(node: Optional[_HuffmanNode], code: str) -> None:
        if node is None:
            return
        if node.char is not None:
            codes[node.char] = code or "0"
            return
        build(node.left, code + "0")
        build(node.right, code + "1")

    build(pq[0], "")
    return codes
