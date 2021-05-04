#!/usr/bin/env bash

set -eo pipefail

# Ensure we have the latest of the alternate branches
git fetch origin solution:solution
git fetch origin incorrect:incorrect

git tag -f starter-code ce91d3bc8547f5c29dcbbe129a53c19053479bce

function add_mark() {
	MARK=$(echo "$MARK + $1" | bc)
}

function run_test() {
    if pytest --timeout=120 --timeout-method=thread $1_test.py &> /dev/null
    then
        echo "$1 ==> passed all tests"
        return 0
    else
        echo "$1 ==> failed some tests"
        return 1
    fi
}

function run_test_new() {
    if [ ! -r $1_test.py ] || git diff -w --exit-code HEAD starter-code $1_test.py &> /dev/null
    then
        echo "$1 ==> tests the same as starter code"
        return 1
    else
        run_test $1
    fi
}

function check_coverage() {
    coverage run -m pytest $1_test.py &> /dev/null
    local COV=$(coverage report | grep "^$1\.py")
    if echo $COV | grep "100%" &> /dev/null
    then
        echo "Your implementation of $1 has 100% coverage with your tests"
        return 0
    else
        echo "Your implementation of $1 does NOT have 100% coverage with your tests"
        return 1
    fi
}

MARK=0

echo
echo "Running your tests against your implementation (sanity check)"
echo "============================================================="
echo

run_test bad_interview || true
run_test neighbours || true
run_test_new divisors && divisors="passed"
run_test_new inverse && inverse="passed"
run_test_new factors && factors="passed"
run_test_new permutations && permutations="passed"
run_test_new balanced && balanced="passed"

echo
echo "Checking coverage of your passing tests with your solution (0.2 marks for each 100%)"
echo "===================================================================================="
echo

[[ -v divisors ]] && check_coverage divisors && add_mark 0.2
[[ -v inverse ]] && check_coverage inverse && add_mark 0.2
[[ -v factors ]] && check_coverage factors && add_mark 0.2
[[ -v permutations ]] && check_coverage permutations && add_mark 0.2
[[ -v balanced ]] && check_coverage balanced && add_mark 0.2

unset bad_interview neighbours divisors inverse factors permutations balanced

echo
echo "Running our tests against your implementation (0.2 marks for each passing)"
echo "=========================================================================="
echo

git checkout solution bad_interview_test.py neighbours_test.py inverse_test.py divisors_test.py factors_test.py permutations_test.py balanced_test.py 2> /dev/null
run_test bad_interview && add_mark 0.2
run_test neighbours && add_mark 0.2
run_test divisors && add_mark 0.2
run_test inverse && add_mark 0.2
run_test factors && add_mark 0.2
run_test permutations && add_mark 0.2
run_test balanced && add_mark 0.2
git reset --hard HEAD &> /dev/null


echo
echo "Checking your tests pass against our working solution"
echo "====================================================="
echo

git checkout solution bad_interview.py neighbours.py inverse.py divisors.py factors.py permutations.py balanced.py 2> /dev/null
run_test_new divisors && divisors="passed"
run_test_new inverse && inverse="passed"
run_test_new factors && factors="passed"
run_test_new permutations && permutations="passed"
run_test_new balanced && balanced="passed"
git reset --hard HEAD &> /dev/null

echo
echo "Checking that, if your tests passed above, they fail against an incorrect solution (0.2 marks for each failure)"
echo "==============================================================================================================="
echo

git checkout incorrect inverse.py divisors.py factors.py permutations.py balanced.py 2> /dev/null
[[ -v divisors ]] && ! run_test divisors && add_mark 0.2
[[ -v inverse ]] && ! run_test inverse && add_mark 0.2
[[ -v factors ]] && ! run_test factors && add_mark 0.2
[[ -v permutations ]] && ! run_test permutations && add_mark 0.2
[[ -v balanced ]] && ! run_test balanced && add_mark 0.2
git reset --hard HEAD &> /dev/null

MARK=$(echo "if ($MARK > 2) 2 else $MARK" | bc)

echo
echo "Your mark is $MARK/2"

echo "$MARK" > recorded_mark
