# Decision tree operators
_OPERATORS = {
    "continuous.equal": lambda context, value: context == value,
    "enum.equal": lambda context, value: context == value,
    "continuous.greaterthan": lambda context, value: context > value,
    "continuous.greaterthanorequal": lambda context, value: context >= value,
    "continuous.lessthan": lambda context, value: context < value,
    "continuous.lessthanorequal": lambda context, value: context <= value,
}
