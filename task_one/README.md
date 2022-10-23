
# Table of Contents

1.  [Usage](#orgce48cbe)
2.  [Approach](#orgd6d5d64)

Spent too long on this - got too interested in exploring the solution, and making it tidy.


<a id="orgce48cbe"></a>

# Usage

    cd task_one
    python3.8 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pytest -vv test_password_evaluator.py
    python -m password_evaluator [PASSWORD] [PATH]


<a id="orgd6d5d64"></a>

# Approach

1.  Test for each condition
2.  Apply operation to rectify each failed condition

It still isn&rsquo;t quite right - I haven&rsquo;t found the right structure of operations, and changing the order of operations changes the required number of operations. I haven&rsquo;t found a way to guarantee a minimum number of steps and correctness.

