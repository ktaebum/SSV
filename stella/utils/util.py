"""
Some helper module
"""
from __future__ import print_function
from __future__ import division
from __future__ import absolute_import


#  Got from geeksforgeeks
def find_closest(arr, n, target, return_idx=False):
  if target <= arr[0]:
    if return_idx:
      return 0
    else:
      return arr[0]
  if target >= arr[n - 1]:
    if return_idx:
      return n - 1
    else:
      return arr[n - 1]

  # Doing binary search
  i = 0
  j = n
  mid = 0
  while i < j:
    mid = (i + j) // 2

    if (arr[mid] == target):
      if return_idx:
        return mid
      else:
        return arr[mid]

    # If target is less than array
    # element, then search in left
    if target < arr[mid]:

      # If target is greater than previous
      # to mid, return closest of two
      if (mid > 0 and target > arr[mid - 1]):
        if target - arr[mid - 1] >= arr[mid] - target:
          if return_idx:
            return mid
          else:
            return arr[mid]
        else:
          if return_idx:
            return mid - 1
          else:
            return arr[mid - 1]

      # Repeat for left half
      j = mid

    # If target is greater than mid
    else:
      if mid < n - 1 and target < arr[mid + 1]:
        if target - arr[mid] >= arr[mid + 1] - target:
          if return_idx:
            return mid + 1
          else:
            return arr[mid + 1]
        else:
          if return_idx:
            return mid
          else:
            return arr[mid]

      i = mid + 1
  # Only single element left after search
  if return_idx:
    return mid
  else:
    return arr[mid]
