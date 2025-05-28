#!/bin/python3

import math
import os
import random
import re
import sys


#
# Complete the 'getRegistrationStatus' function below.
#
# The function is expected to return a STRING_ARRAY.
# The function accepts following parameters:
#  1. STRING_ARRAY passwords
#  2. INTEGER k
#

def getRegistrationStatus(passwords, k):
    # Write your code here
    count = {}
    result = []

    for password in passwords:
        if password not in count:
            count[password] = 0

        if count[password] < k:
            result.append("ACCEPT")
            count[password] += 1
        else:
            result.append("REJECT")

    for status in result:
        return status


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    passwords_count = int(input().strip())

    passwords = []

    for _ in range(passwords_count):
        passwords_item = input()
        passwords.append(passwords_item)

    k = int(input().strip())

    result = getRegistrationStatus(passwords, k)

    fptr.write('\n'.join(result))
    fptr.write('\n')

    fptr.close()
