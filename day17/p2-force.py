def find_a(program):
    # start at zero
    last_results = {0}
    reverse_program = list(reversed(program))
    for value in reverse_program:
        new_results = set()

        for prev_a in last_results:
            for i in range(0, 8):
                a = prev_a * 8 + i  # get next grouping and add 1
                b = a % 8
                b = b ^ 1
                c = a >> b
                b = b ^ 5
                b = b ^ c
                if b % 8 == value:
                    new_results.add(a)
        last_results = (
            new_results  # replace with next result to find the next possible a
        )

    return min(last_results)


program = [2, 4, 1, 1, 7, 5, 1, 5, 4, 3, 0, 3, 5, 5, 3, 0]

print(find_a(program))
