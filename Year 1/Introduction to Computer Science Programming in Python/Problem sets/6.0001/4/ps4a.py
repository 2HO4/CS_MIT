# Problem Set 4A
# Name: <your name here>
# Collaborators:
# Time Spent: x:xx

def get_permutations(sequence):
    '''
    Enumerate all permutations of a given string

    sequence (string): an arbitrary string to permute. Assume that it is a
    non-empty string.  

    You MUST use recursion for this part. Non-recursive solutions will not be
    accepted.

    Returns: a list of all permutations of sequence

    Example:
    >>> get_permutations('abc')
    ['abc', 'acb', 'bac', 'bca', 'cab', 'cba']

    Note: depending on your implementation, you may return the permutations in
    a different order than what is listed here.
    '''

    if len(sequence) == 1:
        return [sequence]

    else:
        ans = []
        for i in range(len(sequence)):
            for j in get_permutations(sequence[:i]+sequence[i+1:]):
                ans.append(sequence[i]+j)

    return ans


if __name__ == '__main__':
    #    #EXAMPLE
    #    example_input = 'abc'
    #    print('Input:', example_input)
    #    print('Expected Output:', ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'])
    #    print('Actual Output:', get_permutations(example_input))

    #    # Put three example test cases here (for your sanity, limit your inputs
    #    to be three characters or fewer as you will have n! permutations for a
    #    sequence of length n)

    input_1 = 'abcd'
    input_2 = 'xyz'
    input_3 = '2405'

    expect_1 = [
        'abcd', 'abdc', 'acbd', 'acdb', 'adbc', 'adcb', 'bacd', 'badc',
        'bcad', 'bcda', 'bdac', 'bdca', 'cabd', 'cadb', 'cbad', 'cbda',
        'cdab', 'cdba', 'dabc', 'dacb', 'dbac', 'dbca', 'dcab', 'dcba'
    ]

    expect_2 = [
        'xyz', 'xzy', 'yxz', 'yzx', 'zxy', 'zyx'
    ]

    expect_3 = [
        '2405', '2450', '2045', '2054', '2540', '2504', '4205', '4250',
        '4025', '4052', '4520', '4502', '0245', '0254', '0425', '0452',
        '0524', '0542', '5240', '5204', '5420', '5402', '5024', '5042'
    ]

    # 1st test
    print('1st Test\'s Input:', input_1, '\n')
    print('Expected Output:\n', expect_1, '\n')
    print('Actual Output\n:', get_permutations(input_1),  '\n')
    print('RESULT:', 'correct' if expect_1 == get_permutations(input_1) else 'wrong')
    print('---------------\n')

    # 2nd test
    print('2nd Test\'s Input:', input_2, '\n')
    print('Expected Output:\n', expect_2, '\n')
    print('Actual Output:\n', get_permutations(input_2), '\n')
    print('RESULT:', 'correct' if expect_2 == get_permutations(input_2) else 'wrong')
    print('---------------\n')

    # 3rd test
    print('3rd Test\'s Input:', input_3, '\n')
    print('Expected Output:\n', expect_3, '\n')
    print('Actual Output:\n', get_permutations(input_3), '\n')
    print('RESULT:', 'correct' if expect_3 == get_permutations(input_3) else 'wrong')
    print('---------------\n')

