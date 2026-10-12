from core import problem

PH = 4


def rand_arr(lo, hi, nlo=1, nhi=50):
    return lambda r: ([r.randint(lo, hi) for _ in range(r.randint(nlo, nhi))],)


@problem(phase=PH, title="Max and Min", returns="int_list", concepts=["single pass"],
         statement="""
         Return the largest and the smallest element of `arr`, in that order, using one loop
         and no built-in max/min/sort.

         **Constraints:** 1 ≤ arr.length ≤ 10^4, −10^9 ≤ arr[i] ≤ 10^9
         """,
         params=[("arr", "int[]")],
         tests=[([3, 1, 4, 1, 5],), ([7],), ([-5, -2, -9],), ([2, 2, 2],)],
         gen=rand_arr(-10**9, 10**9, 1, 10**4), gen_count=3,
         hints=["What should `max` start as? Is 0 a safe starting value?",
                "Start both max and min at arr[0].",
                "Loop from index 1 and update max and min separately."])
def max_min(arr):
    return [max(arr), min(arr)]


@problem(phase=PH, title="Evens, Odds and Sum", returns="long_list", concepts=["counters"],
         statement="""
         Return three values: how many elements are even, how many are odd, and the sum of all elements.

         **Constraints:** 0 ≤ arr.length ≤ 10^4, −10^6 ≤ arr[i] ≤ 10^6
         """,
         params=[("arr", "int[]")],
         tests=[([1, 2, 3, 4, 5],), ([],), ([-3, -4],), ([0],)],
         gen=rand_arr(-10**6, 10**6, 1, 10**4), gen_count=3,
         hints=["How many variables do you need to keep across the loop?",
                "Remember the negative-number trap with `%` from Phase 1.",
                {"java": "Use x % 2 == 0 for even. Keep the sum in a long: 10^4 values of size 10^6 do not fit in an int.",
                 "python": "Use x % 2 == 0 for even. The sum fits in an ordinary integer. For negatives, compare the remainder with 0, not 1.",
                 "javascript": "Use x % 2 === 0 for even. The sum stays exact in a normal number. For negatives, compare the remainder with 0, not 1."}])
def evens_odds_sum(arr):
    e = sum(1 for x in arr if x % 2 == 0)
    return [e, len(arr) - e, sum(arr)]


@problem(phase=PH, title="Linear Search", returns="int", concepts=["early return"],
         statement="""
         Return the index of the **first** occurrence of `target` in `arr`, or −1 if it is absent.

         **Constraints:** 0 ≤ arr.length ≤ 10^4
         """,
         params=[("arr", "int[]"), ("target", "int")],
         tests=[([4, 2, 7, 2], 2), ([4, 2, 7], 9), ([], 1), ([5], 5), ([1, 1, 1], 1), (list(range(10000)), 9999)],
         hints=["Once you find the target, do you need to keep looping?",
                "What should happen if the loop finishes without finding it?",
                "Return i inside the loop; return -1 after it."])
def linear_search(arr, target):
    return arr.index(target) if target in arr else -1


@problem(phase=PH, title="Concatenate Array", returns="int[]", concepts=["new arrays", "index mapping"],
         statement="""
         Return a new array of length `2n` where the first half and the second half are both copies of `arr`.

         **Constraints:** 1 ≤ arr.length ≤ 1000
         """,
         params=[("arr", "int[]")],
         tests=[([1, 2, 1],), ([5],), ([1, 3, 2, 1],), ([0, 0],)],
         gen=rand_arr(-100, 100, 1, 1000), gen_count=2,
         hints=["How big must the result array be?",
                "Where does arr[i] go in the result? Is there a second position too?",
                "ans[i] = arr[i] and ans[i + n] = arr[i]."],
         practice=("LeetCode 1929: Concatenation of Array", "https://leetcode.com/problems/concatenation-of-array/"))
def concat(arr):
    return arr + arr


@problem(phase=PH, title="Running Sum", returns="int[]", concepts=["prefix sums"],
         statement="""
         Return an array where element i is the sum of `arr[0]` to `arr[i]`.

         **Constraints:** 1 ≤ arr.length ≤ 1000, −10^6 ≤ arr[i] ≤ 10^6
         """,
         params=[("arr", "int[]")],
         tests=[([1, 2, 3, 4],), ([1, 1, 1, 1, 1],), ([3, 1, 2, 10, 1],), ([7],)],
         gen=rand_arr(-10**6, 10**6, 1, 1000), gen_count=2,
         hints=["How is the answer at i related to the answer at i − 1?",
                "Do you need a nested loop?",
                "ans[i] = ans[i - 1] + arr[i]."],
         practice=("LeetCode 1480: Running Sum of 1d Array", "https://leetcode.com/problems/running-sum-of-1d-array/"))
def running_sum(arr):
    out, s = [], 0
    for x in arr:
        s += x
        out.append(s)
    return out


@problem(phase=PH, title="Richest Customer", returns="int", concepts=["2D arrays", "row sums"],
         statement="""
         `accounts[i][j]` is the money customer i has in bank j. Return the wealth of the richest customer
         (the largest row sum).

         **Constraints:** 1 ≤ rows, cols ≤ 50, 1 ≤ accounts[i][j] ≤ 100
         """,
         params=[("accounts", "int[][]")],
         tests=[([[1, 2, 3], [3, 2, 1]],), ([[1, 5], [7, 3], [3, 5]],), ([[2, 8, 7], [7, 1, 3], [1, 9, 5]],), ([[42]],)],
         gen=lambda r: ([[r.randint(1, 100) for _ in range(c)] for c in [r.randint(1, 50)] for _ in range(r.randint(1, 50))],),
         gen_count=2,
         hints=["What does one row represent?",
                "Compute each row's total with an inner loop.",
                "Keep the best total seen so far across rows."],
         practice=("LeetCode 1672: Richest Customer Wealth", "https://leetcode.com/problems/richest-customer-wealth/"))
def richest(accounts):
    return max(sum(r) for r in accounts)


@problem(phase=PH, title="Greatest Candies", returns="bool_list", concepts=["two passes"],
         statement="""
         `candies[i]` is what kid i has. If you give kid i all `extra` candies, will they have the most
         (ties count)? Return true/false for every kid.

         **Constraints:** 2 ≤ candies.length ≤ 100, 1 ≤ candies[i], extra ≤ 100
         """,
         params=[("candies", "int[]"), ("extra", "int")],
         tests=[([2, 3, 5, 1, 3], 3), ([4, 2, 1, 1, 2], 1), ([12, 1, 12], 10), ([1, 1], 1), ([5, 5, 5, 1], 3)],
         hints=["What single value do you need to know before judging any kid?",
                "First loop: find the max. Second loop: compare.",
                "ans[i] = candies[i] + extra >= max."],
         practice=("LeetCode 1431: Kids With the Greatest Number of Candies",
                   "https://leetcode.com/problems/kids-with-the-greatest-number-of-candies/"))
def candies(candies, extra):
    m = max(candies)
    return [x + extra >= m for x in candies]


@problem(phase=PH, title="Highest Altitude", returns="int", concepts=["running value + best value"],
         statement="""
         A biker starts at altitude 0. `gain[i]` is the change in altitude between point i and i + 1.
         Return the highest altitude reached (including the start).

         **Constraints:** 1 ≤ gain.length ≤ 100, −100 ≤ gain[i] ≤ 100
         """,
         params=[("gain", "int[]")],
         tests=[([-5, 1, 5, 0, -7],), ([-4, -3, -2, -1, 4, 3, 2],), ([3],), ([-1],)],
         gen=rand_arr(-100, 100, 1, 100), gen_count=2,
         hints=["Which two values change as you walk the array?",
                "Should the best altitude start at 0 or at the first gain?",
                "Add gain[i] to the altitude. best is the larger of best and the altitude, and best starts at 0."],
         practice=("LeetCode 1732: Find the Highest Altitude", "https://leetcode.com/problems/find-the-highest-altitude/"))
def altitude(gain):
    best = alt = 0
    for g in gain:
        alt += g
        best = max(best, alt)
    return best


@problem(phase=PH, title="Even Digit Count", returns="int", concepts=["reuse a helper"],
         statement="""
         Return how many numbers in `nums` have an even number of digits.

         **Constraints:** 1 ≤ nums.length ≤ 500, 1 ≤ nums[i] ≤ 10^5
         """,
         params=[("nums", "int[]")],
         tests=[([12, 345, 2, 6, 7896],), ([555, 901, 482, 1771],), ([100000],), ([10, 99, 1000],)],
         gen=rand_arr(1, 10**5, 1, 500), gen_count=2,
         hints=["You wrote a digit counter in Phase 2. Can you make it a function?",
                "Call it for each element.",
                {"java": "count += (digitCount(x) % 2 == 0) ? 1 : 0.",
                 "python": "if the digit count is even: count += 1.",
                 "javascript": "count += digitCount(x) % 2 === 0 ? 1 : 0."}],
         practice=("LeetCode 1295: Find Numbers with Even Number of Digits",
                   "https://leetcode.com/problems/find-numbers-with-even-number-of-digits/"))
def even_digits(nums):
    return sum(1 for x in nums if len(str(x)) % 2 == 0)


@problem(phase=PH, title="Sign of the Product", returns="int", concepts=["counting instead of computing"],
         statement="""
         Return 1 if the product of all elements is positive, −1 if negative, 0 if zero.
         Do **not** multiply: the product would overflow.

         **Constraints:** 1 ≤ nums.length ≤ 1000, −100 ≤ nums[i] ≤ 100
         """,
         params=[("nums", "int[]")],
         tests=[([-1, -2, -3, -4, 3, 2, 1],), ([1, 5, 0, 2, -3],), ([-1, 1, -1, 1, -1],), ([100] * 1000,), ([-7],)],
         hints=["What decides the sign of a product?",
                "What single element makes the whole product zero?",
                "Return 0 on any zero; otherwise count negatives and check its parity."],
         practice=("LeetCode 1822: Sign of the Product of an Array",
                   "https://leetcode.com/problems/sign-of-the-product-of-an-array/"))
def sign_product(nums):
    if 0 in nums:
        return 0
    return -1 if sum(1 for x in nums if x < 0) % 2 else 1


@problem(phase=PH, title="Good Pairs", returns="int", concepts=["nested loops over pairs"],
         statement="""
         A pair (i, j) is good if `nums[i] == nums[j]` and i < j. Return the number of good pairs.

         **Constraints:** 1 ≤ nums.length ≤ 100, 1 ≤ nums[i] ≤ 100
         """,
         params=[("nums", "int[]")],
         tests=[([1, 2, 3, 1, 1, 3],), ([1, 1, 1, 1],), ([1, 2, 3],), ([5],)],
         gen=rand_arr(1, 5, 1, 100), gen_count=2,
         hints=["How do you visit every pair exactly once?",
                "Where should the inner loop start so that i < j?",
                "for i in 0..n-1, for j in i+1..n-1: count if equal."],
         practice=("LeetCode 1512: Number of Good Pairs", "https://leetcode.com/problems/number-of-good-pairs/"))
def good_pairs(nums):
    return sum(1 for i in range(len(nums)) for j in range(i + 1, len(nums)) if nums[i] == nums[j])


@problem(phase=PH, title="Smaller Than Current", returns="int[]", concepts=["nested loops"],
         statement="""
         For each `nums[i]`, count how many other numbers in the array are strictly smaller. Return the counts.

         **Constraints:** 2 ≤ nums.length ≤ 500, 0 ≤ nums[i] ≤ 100
         """,
         params=[("nums", "int[]")],
         tests=[([8, 1, 2, 2, 3],), ([6, 5, 4, 8],), ([7, 7, 7, 7],), ([0, 100],)],
         gen=rand_arr(0, 100, 2, 500), gen_count=2,
         hints=["For one element, how would you count by hand?",
                "Now repeat that for every element.",
                "ans[i] = count of j with nums[j] < nums[i]."],
         practice=("LeetCode 1365: How Many Numbers Are Smaller Than the Current Number",
                   "https://leetcode.com/problems/how-many-numbers-are-smaller-than-the-current-number/"))
def smaller_than(nums):
    return [sum(1 for y in nums if y < x) for x in nums]


@problem(phase=PH, title="Shuffle Halves", returns="int[]", concepts=["index mapping"],
         statement="""
         `nums` has 2n elements: x1 x2 … xn y1 y2 … yn. Return x1 y1 x2 y2 … xn yn.

         **Constraints:** 1 ≤ n ≤ 500
         """,
         params=[("nums", "int[]")],
         tests=[([2, 5, 1, 3, 4, 7],), ([1, 2, 3, 4, 4, 3, 2, 1],), ([1, 1, 2, 2],), ([9, 8],)],
         gen=lambda r: ([r.randint(1, 1000) for _ in range(2 * r.randint(1, 500))],), gen_count=2,
         hints=["Where is y1 in the input? Where does it go in the output?",
                "Loop i over 0..n−1. Which two values do you place each time?",
                "ans[2i] = nums[i]; ans[2i + 1] = nums[i + n]."],
         practice=("LeetCode 1470: Shuffle the Array", "https://leetcode.com/problems/shuffle-the-array/"))
def shuffle(nums):
    n = len(nums) // 2
    out = []
    for i in range(n):
        out += [nums[i], nums[i + n]]
    return out


@problem(phase=PH, title="Reverse In Place", returns="int[]", concepts=["two pointers", "swap"],
         statement="""
         Reverse `arr` **in place** (no second array) and return it.

         **Constraints:** 0 ≤ arr.length ≤ 10^4
         """,
         params=[("arr", "int[]")],
         tests=[([1, 2, 3, 4, 5],), ([1, 2],), ([],), ([9],)],
         gen=rand_arr(-1000, 1000, 1, 10**4), gen_count=2,
         hints=["Which element swaps with arr[0]? With arr[1]?",
                "When should the swapping stop?",
                {"java": "l = 0, r = n - 1; while l < r: swap, then l++ and r--.",
                 "python": "l, r = 0, len(arr) - 1; while l < r: swap, then l += 1 and r -= 1.",
                 "javascript": "l = 0, r = n - 1; while l < r: swap, then l++ and r--."}],
         practice=("LeetCode 344: Reverse String", "https://leetcode.com/problems/reverse-string/"))
def reverse_arr(arr):
    return arr[::-1]


@problem(phase=PH, title="Third Distinct Maximum", difficulty="medium", returns="long", concepts=["tracking top-k"],
         statement="""
         Return the third largest **distinct** number. If there are fewer than three distinct numbers, return the largest.
         Do not sort.

         **Constraints:** 1 ≤ nums.length ≤ 10^4, −2^31 ≤ nums[i] ≤ 2^31 − 1
         """,
         params=[("nums", "int[]")],
         tests=[([3, 2, 1],), ([1, 2],), ([2, 2, 3, 1],), ([1, 1, 1],), ([-2147483648, 1, 2],), ([5, 4, 4, 3, 3, 9],)],
         gen=rand_arr(-50, 50, 1, 10**4), gen_count=2,
         hints=["Start with the second-largest version: which two variables do you keep?",
                "When a new number beats `first`, what happens to `second` and `third`?",
                {"java": "Skip values equal to first, second or third. Use long, and Long.MIN_VALUE means empty.",
                 "python": "Skip values equal to first, second or third. Use None for empty, because every integer is a real value.",
                 "javascript": "Skip values equal to first, second or third. Use null for empty, because every number is a real value."}],
         practice=("LeetCode 414: Third Maximum Number", "https://leetcode.com/problems/third-maximum-number/"))
def third_max(nums):
    s = sorted(set(nums), reverse=True)
    return s[2] if len(s) >= 3 else s[0]


@problem(phase=PH, title="Max Consecutive Ones", returns="int", concepts=["streak counter"],
         statement="""
         `nums` contains only 0s and 1s. Return the length of the longest run of consecutive 1s.

         **Constraints:** 1 ≤ nums.length ≤ 10^5
         """,
         params=[("nums", "int[]")],
         tests=[([1, 1, 0, 1, 1, 1],), ([1, 0, 1, 1, 0, 1],), ([0],), ([1],), ([1] * 100000,)],
         gen=rand_arr(0, 1, 1, 10**5), gen_count=1,
         hints=["What should happen to the current streak when you see a 0?",
                "When do you update the best streak?",
                "If the value is 1, the streak grows by 1; otherwise the streak is 0. best is the larger of best and the streak."],
         practice=("LeetCode 485: Max Consecutive Ones", "https://leetcode.com/problems/max-consecutive-ones/"))
def max_ones(nums):
    best = cur = 0
    for x in nums:
        cur = cur + 1 if x == 1 else 0
        best = max(best, cur)
    return best


@problem(phase=PH, title="Sorted and Rotated", difficulty="medium", returns="bool", concepts=["counting drops"],
         statement="""
         Return `true` if `nums` could be a non-decreasing array rotated some number of times (including zero).
         Example: [3, 4, 5, 1, 2] is [1, 2, 3, 4, 5] rotated.

         **Constraints:** 1 ≤ nums.length ≤ 100
         """,
         params=[("nums", "int[]")],
         tests=[([3, 4, 5, 1, 2],), ([2, 1, 3, 4],), ([1, 2, 3],), ([1, 1, 1],), ([2, 1],), ([6, 10, 6],), ([1, 3, 2, 1],)],
         hints=["In a sorted array, how many places have nums[i] > nums[i+1]? In a rotated one?",
                "Should the last element be compared with the first?",
                "Count i where nums[i] > nums[(i+1) % n]. Valid if the count is at most 1."],
         practice=("LeetCode 1752: Check if Array Is Sorted and Rotated",
                   "https://leetcode.com/problems/check-if-array-is-sorted-and-rotated/"))
def sorted_rotated(nums):
    n = len(nums)
    return sum(1 for i in range(n) if nums[i] > nums[(i + 1) % n]) <= 1


@problem(phase=PH, title="Monotonic Array", returns="bool", concepts=["two flags"],
         statement="""
         Return `true` if `nums` is entirely non-increasing or entirely non-decreasing.

         **Constraints:** 1 ≤ nums.length ≤ 10^5
         """,
         params=[("nums", "int[]")],
         tests=[([1, 2, 2, 3],), ([6, 5, 4, 4],), ([1, 3, 2],), ([5],), ([2, 2, 2],), ([1, 1, 0, 1],)],
         hints=["Can you track two possibilities at once?",
                "Which pair breaks 'non-decreasing'? Which breaks 'non-increasing'?",
                "Start both flags true. For each neighbouring pair, clear the flag that pair breaks. The array is monotonic if either flag is still true."],
         practice=("LeetCode 896: Monotonic Array", "https://leetcode.com/problems/monotonic-array/"))
def monotonic(nums):
    inc = all(nums[i] <= nums[i + 1] for i in range(len(nums) - 1))
    dec = all(nums[i] >= nums[i + 1] for i in range(len(nums) - 1))
    return inc or dec


@problem(phase=PH, title="Plus One", returns="int[]", concepts=["carry"],
         statement="""
         `digits` stores a non-negative number, most significant digit first. Add one and return the new digits.

         **Constraints:** 1 ≤ digits.length ≤ 100, no leading zeros except the number 0 itself
         """,
         params=[("digits", "int[]")],
         tests=[([1, 2, 3],), ([4, 3, 2, 1],), ([9],), ([9, 9, 9],), ([0],), ([1, 9, 9],), ([9] * 100,)],
         hints=["Start from which end?",
                "When does the carry stop moving left?",
                "If every digit was 9, the result is one longer: 1 followed by zeros."],
         practice=("LeetCode 66: Plus One", "https://leetcode.com/problems/plus-one/"))
def plus_one(digits):
    return [int(c) for c in str(int("".join(map(str, digits))) + 1)]


@problem(phase=PH, title="Evens First", returns="int[]", concepts=["stable partition"],
         statement="""
         Return the array with all even numbers first and all odd numbers after, each group keeping its
         original order.

         **Constraints:** 1 ≤ nums.length ≤ 5000, 0 ≤ nums[i] ≤ 5000
         """,
         params=[("nums", "int[]")],
         tests=[([3, 1, 2, 4],), ([0],), ([1, 3, 5],), ([2, 4, 6],)],
         gen=rand_arr(0, 5000, 1, 5000), gen_count=2,
         hints=["How many passes over the array would make this easy?",
                "Fill a result array: first copy the evens, then the odds.",
                "Keep a write index k that moves forward across both passes."],
         practice=("LeetCode 905: Sort Array By Parity", "https://leetcode.com/problems/sort-array-by-parity/"))
def evens_first(nums):
    return [x for x in nums if x % 2 == 0] + [x for x in nums if x % 2]


@problem(phase=PH, title="Move Zeroes", returns="int[]", concepts=["write pointer"],
         statement="""
         Move all 0s to the end while keeping the order of the other elements. Do it in place and return the array.

         **Constraints:** 1 ≤ nums.length ≤ 10^4
         """,
         params=[("nums", "int[]")],
         tests=[([0, 1, 0, 3, 12],), ([0],), ([1, 2, 3],), ([0, 0, 1],)],
         gen=lambda r: ([r.choice([0, 0, r.randint(-100, 100)]) for _ in range(r.randint(1, 10**4))],), gen_count=2,
         hints=["Imagine copying only the non-zero numbers to the front. Where does each one go?",
                "After that copy, what is left to fill?",
                {"java": "k = 0; for each x != 0: nums[k++] = x; then fill the rest with 0.",
                 "python": "k = 0; for each x != 0: nums[k] = x; k += 1; then fill the rest with 0.",
                 "javascript": "k = 0; for each x !== 0: nums[k++] = x; then fill the rest with 0."}],
         practice=("LeetCode 283: Move Zeroes", "https://leetcode.com/problems/move-zeroes/"))
def move_zeroes(nums):
    nz = [x for x in nums if x != 0]
    return nz + [0] * (len(nums) - len(nz))


@problem(phase=PH, title="Remove Duplicates (Sorted)", returns="int[]", concepts=["write pointer"],
         statement="""
         `nums` is sorted. Keep each value once, in place, and return only the unique part.

         **Constraints:** 1 ≤ nums.length ≤ 3·10^4
         """,
         params=[("nums", "int[]")],
         tests=[([1, 1, 2],), ([0, 0, 1, 1, 1, 2, 2, 3, 3, 4],), ([5],), ([1, 2, 3],), ([7] * 100,)],
         gen=lambda r: (sorted(r.randint(-100, 100) for _ in range(r.randint(1, 3 * 10**4))),), gen_count=1,
         hints=["In a sorted array, where are the duplicates of a value?",
                "Compare each element with the last unique one you kept.",
                {"java": "k = 1; if nums[i] != nums[k - 1]: nums[k++] = nums[i]. Return the first k elements.",
                 "python": "k = 1; if nums[i] != nums[k - 1]: nums[k] = nums[i]; k += 1. Return the first k elements.",
                 "javascript": "k = 1; if nums[i] !== nums[k - 1]: nums[k++] = nums[i]. Return the first k elements."}],
         practice=("LeetCode 26: Remove Duplicates from Sorted Array",
                   "https://leetcode.com/problems/remove-duplicates-from-sorted-array/"))
def remove_dups(nums):
    out = []
    for x in nums:
        if not out or out[-1] != x:
            out.append(x)
    return out


@problem(phase=PH, title="Rotate Right", difficulty="medium", returns="int[]", concepts=["modulo on indexes"],
         statement="""
         Rotate `nums` to the right by `k` steps and return it. `k` can be larger than the length.

         **Constraints:** 1 ≤ nums.length ≤ 10^5, 0 ≤ k ≤ 10^9
         """,
         params=[("nums", "int[]"), ("k", "int")],
         tests=[([1, 2, 3, 4, 5, 6, 7], 3), ([-1, -100, 3, 99], 2), ([1], 5), ([1, 2], 0), ([1, 2, 3], 1000000000)],
         gen=lambda r: ([r.randint(-1000, 1000) for _ in range(r.randint(1, 10**5))], r.randint(0, 10**9)), gen_count=1,
         hints=["Rotating by n steps changes nothing. What does that say about large k?",
                "Where does nums[i] end up after rotating by k?",
                "k %= n; ans[(i + k) % n] = nums[i]. (Bonus: three reversals, no extra array.)"],
         practice=("LeetCode 189: Rotate Array", "https://leetcode.com/problems/rotate-array/"))
def rotate(nums, k):
    k %= len(nums)
    return nums[-k:] + nums[:-k] if k else nums


@problem(phase=PH, title="Missing Number", returns="int", concepts=["expected sum"],
         statement="""
         `nums` holds n distinct numbers from the range 0..n, so exactly one is missing. Return it.

         **Constraints:** 1 ≤ n ≤ 10^4
         """,
         params=[("nums", "int[]")],
         tests=[([3, 0, 1],), ([0, 1],), ([9, 6, 4, 2, 3, 5, 7, 0, 1],), ([0],), ([1],)],
         gen=lambda r: ((lambda n, m: [x for x in r.sample(range(n + 1), n + 1) if x != m])(r.randint(1, 10**4), 0),),
         gen_count=1,
         hints=["What would the sum be if nothing were missing?",
                "Compare that with the actual sum.",
                "missing = n(n+1)/2 − sum(nums)."],
         practice=("LeetCode 268: Missing Number", "https://leetcode.com/problems/missing-number/"))
def missing(nums):
    n = len(nums)
    return n * (n + 1) // 2 - sum(nums)


@problem(phase=PH, title="Contains Duplicate", returns="bool", concepts=["nested loops"],
         statement="""
         Return `true` if any value appears at least twice.

         Nested loops are fine here; faster ideas come in DSA.

         **Constraints:** 1 ≤ nums.length ≤ 2000
         """,
         params=[("nums", "int[]")],
         tests=[([1, 2, 3, 1],), ([1, 2, 3, 4],), ([1, 1, 1, 3, 3, 4, 3, 2, 4, 2],), ([5],), (list(range(2000)),)],
         hints=["Which pairs do you need to compare?",
                "Can you stop early?",
                "Two loops with j > i; as soon as nums[i] == nums[j], you have found one."],
         practice=("LeetCode 217: Contains Duplicate", "https://leetcode.com/problems/contains-duplicate/"))
def contains_dup(nums):
    return len(set(nums)) != len(nums)


@problem(phase=PH, title="Two Sum (Brute Force)", returns="int_list", concepts=["nested loops over pairs"],
         statement="""
         Return the indexes `i j` (i < j) of the two numbers that add up to `target`. Exactly one answer exists.

         **Constraints:** 2 ≤ nums.length ≤ 2000
         """,
         params=[("nums", "int[]"), ("target", "int")],
         tests=[([2, 7, 11, 15], 9), ([3, 2, 4], 6), ([3, 3], 6), ([-1, -2, -3, -4, -5], -8), ([0, 4, 3, 0], 0)],
         hints=["Which pairs should you try?",
                "Make sure you never use the same index twice.",
                "for i, for j > i: if nums[i] + nums[j] == target return [i, j]."],
         practice=("LeetCode 1: Two Sum", "https://leetcode.com/problems/two-sum/"))
def two_sum(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]


@problem(phase=PH, title="Merge Sorted Arrays", difficulty="medium", returns="int[]", concepts=["two indexes"],
         statement="""
         Given two sorted arrays `a` and `b`, return one sorted array with all their elements.
         Do not just concatenate and sort.

         **Constraints:** 0 ≤ a.length, b.length ≤ 10^4
         """,
         params=[("a", "int[]"), ("b", "int[]")],
         tests=[([1, 2, 3], [2, 5, 6]), ([1], []), ([], [1]), ([4, 5, 6], [1, 2, 3]), ([1, 1], [1, 1])],
         gen=lambda r: (sorted(r.randint(-10**4, 10**4) for _ in range(r.randint(0, 10**4))),
                        sorted(r.randint(-10**4, 10**4) for _ in range(r.randint(1, 10**4)))), gen_count=1,
         hints=["Which two elements are candidates for the smallest remaining value?",
                "Keep one index into each array.",
                "Take the smaller of a[i] and b[j]; when one array runs out, copy the rest of the other."],
         practice=("LeetCode 88: Merge Sorted Array", "https://leetcode.com/problems/merge-sorted-array/"))
def merge(a, b):
    return sorted(a + b)


@problem(phase=PH, title="Pivot Index", difficulty="medium", returns="int", concepts=["total minus left"],
         statement="""
         Return the leftmost index where the sum of elements to its left equals the sum to its right, or −1.

         **Constraints:** 1 ≤ nums.length ≤ 10^4, −1000 ≤ nums[i] ≤ 1000
         """,
         params=[("nums", "int[]")],
         tests=[([1, 7, 3, 6, 5, 6],), ([1, 2, 3],), ([2, 1, -1],), ([0],), ([-1, -1, 0, 1, 1, 0],)],
         gen=rand_arr(-3, 3, 1, 10**4), gen_count=1,
         hints=["If you know the total and the left sum, what is the right sum?",
                "Compute the total once before the main loop.",
                "right = total − left − nums[i]; check, then left += nums[i]."],
         practice=("LeetCode 724: Find Pivot Index", "https://leetcode.com/problems/find-pivot-index/"))
def pivot(nums):
    total, left = sum(nums), 0
    for i, x in enumerate(nums):
        if left == total - left - x:
            return i
        left += x
    return -1


@problem(phase=PH, title="Best Day to Trade", returns="int", concepts=["minimum so far"],
         statement="""
         `prices[i]` is a stock price on day i. Buy once and sell once later. Return the maximum profit (0 if none).

         **Constraints:** 1 ≤ prices.length ≤ 10^5, 0 ≤ prices[i] ≤ 10^4
         """,
         params=[("prices", "int[]")],
         tests=[([7, 1, 5, 3, 6, 4],), ([7, 6, 4, 3, 1],), ([5],), ([1, 2],), ([2, 4, 1, 3],)],
         gen=rand_arr(0, 10**4, 1, 10**5), gen_count=1,
         hints=["If you sell on day i, what is the best day to have bought?",
                "Can you remember the cheapest price seen so far as you walk forward?",
                "Remember the cheapest price so far. The best profit is the larger of the current best and (this price minus that cheapest price)."],
         practice=("LeetCode 121: Best Time to Buy and Sell Stock",
                   "https://leetcode.com/problems/best-time-to-buy-and-sell-stock/"))
def stock(prices):
    best, lo = 0, prices[0]
    for p in prices:
        lo = min(lo, p)
        best = max(best, p - lo)
    return best


@problem(phase=PH, title="Transpose Matrix", returns="int[][]", concepts=["2D index swap"],
         statement="""
         Return the transpose of `matrix` (rows become columns). The matrix need not be square.

         **Constraints:** 1 ≤ rows, cols ≤ 100
         """,
         params=[("matrix", "int[][]")],
         tests=[([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), ([[1, 2, 3], [4, 5, 6]],), ([[5]],), ([[1], [2], [3]],)],
         gen=lambda r: ([[r.randint(-99, 99) for _ in range(c)] for c in [r.randint(1, 100)] for _ in range(r.randint(1, 100))],),
         gen_count=1,
         hints=["If the input is 2×3, what size is the output?",
                "Where does matrix[i][j] go?",
                {"java": "ans = new int[cols][rows]; ans[j][i] = matrix[i][j].",
                 "python": "ans = [[0] * rows for _ in range(cols)]; ans[j][i] = matrix[i][j]. Build each row on its own.",
                 "javascript": "ans = Array.from({ length: cols }, () => new Array(rows).fill(0)); ans[j][i] = matrix[i][j]."}],
         practice=("LeetCode 867: Transpose Matrix", "https://leetcode.com/problems/transpose-matrix/"))
def transpose(matrix):
    return [list(r) for r in zip(*matrix)]


@problem(phase=PH, title="Diagonal Sum", returns="int", concepts=["2D indexes"],
         statement="""
         Return the sum of both diagonals of a square matrix. Count the centre cell only once.

         **Constraints:** 1 ≤ n ≤ 100
         """,
         params=[("mat", "int[][]")],
         tests=[([[1, 2, 3], [4, 5, 6], [7, 8, 9]],), ([[1, 1, 1, 1]] * 4,), ([[5]],), ([[1, 2], [3, 4]],)],
         gen=lambda r: ((lambda n: [[r.randint(1, 100) for _ in range(n)] for _ in range(n)])(r.randint(1, 100)),),
         gen_count=1,
         hints=["Which (i, j) pairs are on the main diagonal? On the other one?",
                "Do you need two nested loops?",
                "Add mat[i][i] and mat[i][n−1−i]; if n is odd subtract the centre once."],
         practice=("LeetCode 1572: Matrix Diagonal Sum", "https://leetcode.com/problems/matrix-diagonal-sum/"))
def diag_sum(mat):
    n = len(mat)
    s = sum(mat[i][i] + mat[i][n - 1 - i] for i in range(n))
    return s - (mat[n // 2][n // 2] if n % 2 else 0)


@problem(phase=PH, title="Flip the Image", returns="int[][]", concepts=["row operations"],
         statement="""
         For a binary matrix, reverse every row, then invert every bit (0 ↔ 1). Return the result.

         **Constraints:** 1 ≤ n ≤ 20 (square)
         """,
         params=[("image", "int[][]")],
         tests=[([[1, 1, 0], [1, 0, 1], [0, 0, 0]],), ([[1, 1, 0, 0], [1, 0, 0, 1], [0, 1, 1, 1], [1, 0, 1, 0]],), ([[0]],)],
         gen=lambda r: ((lambda n: [[r.randint(0, 1) for _ in range(n)] for _ in range(n)])(r.randint(1, 20)),),
         gen_count=2,
         hints=["Do the two steps separately first.",
                "How do you invert a bit with arithmetic?",
                "Reverse each row with two pointers, then set x = 1 − x."],
         practice=("LeetCode 832: Flipping an Image", "https://leetcode.com/problems/flipping-an-image/"))
def flip(image):
    return [[1 - x for x in reversed(r)] for r in image]
