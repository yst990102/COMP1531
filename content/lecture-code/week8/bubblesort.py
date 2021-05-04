from hypothesis import given, strategies, Verbosity, settings

def bubblesort(numbers):
    numbers = numbers.copy()
    for _ in range(len(numbers) - 1):
        for i in range(len(numbers) - 1):
            if numbers[i] > numbers[i+1]:
                numbers[i], numbers[i+1] = numbers[i+1], numbers[i]
    return numbers

@given(strategies.lists(strategies.integers()))
@settings(verbosity=Verbosity.verbose)
def test_length(nums):
    assert len(bubblesort(nums)) == len(nums)

@given(strategies.lists(strategies.integers()))
@settings(verbosity=Verbosity.verbose)
def test_idempotence(nums):
    assert bubblesort(nums) == bubblesort(bubblesort(nums))

def is_sorted(nums):
    for i in range(len(nums) - 1):
        if nums[i] > nums[i+1]:
            return False
    return True

@given(strategies.lists(strategies.integers()))
def test_sorted(nums):
    assert is_sorted(bubblesort(nums))

def is_permutation(nums1, nums2):
    d1 = {}
    for n in nums1:
        if n in d1:
            d1[n] += 1
        else:
            d1[n] = 1
    d2 = {}
    for n in nums2:
        if n in d2:
            d2[n] += 1
        else:
            d2[n] = 1
    return d1 == d2

@given(strategies.lists(strategies.integers()))
def test_permutation(nums):
    assert is_permutation(nums, bubblesort(nums))