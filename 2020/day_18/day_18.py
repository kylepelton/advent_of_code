import operator

def part_one():
    def solve_problem(problem, idx):
        # Recursively solves problems (and subproblems) starting at the given index.
        # We store the running result and the next operator to use. By defaulting
        # these to 0 and addition, it's as though we add 0 + problem to the
        # start of each problem, which has no effect except to simplify our logic
        result = 0
        op = operator.add
        # Keep going until the end of the problem
        while idx < len(problem):
            if problem[idx].isdigit():
                # Found an operand. Apply the operator on the operand to the
                # running result
                result = op(result, int(problem[idx]))
            elif problem[idx] == "+":
                # Next operator is addition
                op = operator.add
            elif problem[idx] == "*":
                # Next operator is multiplication
                op = operator.mul
            elif problem[idx] == "(":
                # Start of a subproblem. Recursively solve it then apply it to
                # the running result
                subresult, idx = solve_problem(problem, idx + 1)
                result = op(result, subresult)
            elif problem[idx] == ")":
                # End of a subproblem. Return it and the last index we read
                # while solving this subproblem
                return result, idx
            idx += 1
        return result, idx
    # Tokenize each problem
    problems = []
    with open("input.txt") as f:
        for line in f:
            problems.append(line.strip().replace("(", "( ").replace(")", " )").split())
    # Return the sum of all problems
    running_sum = sum(solve_problem(problem, 0)[0] for problem in problems)
    print("Part One:")
    print("Sum of Problems:", running_sum)

def part_two():
    def solve_problem(problem, idx):
        # Recursively solves problems (and subproblems) starting at the given index.
        # We store the running result and the next operator to use. By defaulting
        # these to 0 and addition, it's as though we add 0 + problem to the
        # start of each problem, which has no effect except to simplify our logic
        result = 0
        op = operator.add
        # Keep going until the end of the problem
        while idx < len(problem):
            if problem[idx].isdigit():
                # Found an operand. Apply the operator on the operand to the
                # running result
                result = op(result, int(problem[idx]))
            elif problem[idx] == "+":
                # Next operator is addition
                op = operator.add
            elif problem[idx] == "*":
                # Next operator is multiplication
                # Since addition has higher priority, solve any additions to
                # the right first, then apply the multiplication, then return
                # this result. By returning the result at this step, you handle
                # the case that you were in the middle of a subproblem and the
                # call to solve_problem() ended by finding that subproblem's
                # closing brace ")".
                op = operator.mul
                subresult, idx = solve_problem(problem, idx + 1)
                result = op(result, subresult)
                return result, idx
            elif problem[idx] == "(":
                # Start of a subproblem. Recursively solve it then apply it to
                # the running result
                subresult, idx = solve_problem(problem, idx + 1)
                result = op(result, subresult)
            elif problem[idx] == ")":
                # End of a subproblem. Return it and the last index we read
                # while solving this subproblem
                return result, idx
            idx += 1
        return result, idx
    # Tokenize each problem
    problems = []
    with open("input.txt") as f:
        for line in f:
            problems.append(line.strip().replace("(", "( ").replace(")", " )").split())
    # Return the sum of all problems
    running_sum = sum(solve_problem(problem, 0)[0] for problem in problems)
    print("Part Two:")
    print("Sum of Problems:", running_sum)

def main():
    part_one()
    part_two()

if __name__ == "__main__":
    main()
