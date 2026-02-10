import numpy as np

class DomainError(Exception):
	"""Raised when input is outside the valid domain of the function."""
	pass

class ZeroDenominatorError(Exception):
	"""Raised when denominator is zero."""
	pass

class StepError(Exception):
	pass

class OddStepWarning(Exception):
	pass

def function_1(x_arr):
	"""
	   Computes the first example function:
	       f(x) = sqrt(1.5 * x + 1) / (1.2 * x + sqrt(3 * x^2 - 1.8))

	   Raises:
	       DomainError: if the argument is outside the valid domain (sqrt of negative).
	       ZeroDenominatorError: if the denominator is zero.

	   Args:
	       x_arr (array-like): Input array or value.

	   Returns:
	       np.ndarray: Function values corresponding to x_arr.
	   """

	x_arr = np.array(x_arr, dtype='float64')
	sqrt_expr1 = 1.5 * x_arr + 1
	sqrt_expr2 = 3 * x_arr ** 2 - 1.8

	if np.any(sqrt_expr1 < 0):
		raise DomainError
	if np.any(sqrt_expr2 < 0):
		raise DomainError
	if np.any(1.2 * x_arr + np.sqrt(sqrt_expr2) == 0):
		raise ZeroDenominatorError

	return np.sqrt(sqrt_expr1) / (1.2 * x_arr + np.sqrt(sqrt_expr2))

def function_2(x_arr):
	"""
	    Computes the second example function:
	        f(x) = sin(0.8 * x + 0.3) / (1.2 + cos(x^2 + 0.4))

	    Raises:
	        ZeroDenominatorError: if the denominator is zero.

	    Args:
	        x_arr (array-like): Input array or value.

	    Returns:
	        np.ndarray: Function values corresponding to x_arr.
	    """

	x_arr = np.array(x_arr, dtype='float64')

	if np.any(1.2 + np.cos(x_arr ** 2 + 0.4) == 0):
		raise ZeroDenominatorError

	return np.sin(0.8 * x_arr + 0.3)/(1.2 + np.cos(x_arr ** 2 + 0.4))

def validate_step(n):
	if not isinstance(n, int):
		raise StepError('Stride must be an integer')
	elif n < 1:
		raise StepError('Step must be at least 1')

def left_rectangle(func, a, b, n):
	"""
	    Computes the definite integral of a function using the left rectangle method.

	    Args:
	        func (callable): Function to integrate.
	        a (float): Lower limit of integration.
	        b (float): Upper limit of integration.
	        n (int): Number of points (subintervals = n-1).

	    Returns:
	        float: Approximation of the integral.
	    """

	validate_step(n)

	x_arr = np.linspace(a, b, n+1, dtype='float64')
	stride = x_arr[1] - x_arr[0]
	func_arr = func(x_arr[:-1])
	return np.round(np.sum(stride * func_arr),5)

def right_rectangle(func, a, b, n):
	"""
	    Computes the definite integral of a function using the right rectangle method.

	    Args:
	        func (callable): Function to integrate.
	        a (float): Lower limit of integration.
	        b (float): Upper limit of integration.
	        n (int): Number of points (subintervals = n-1).

	    Returns:
	        float: Approximation of the integral.
	    """
	validate_step(n)

	x_arr = np.linspace(a, b, n+1, dtype='float64')
	stride = x_arr[1] - x_arr[0]
	func_arr = func(x_arr[1:])
	return np.round(np.sum(stride * func_arr),5)

def trapezoidal(func, a, b, n):
	"""
    Computes the definite integral of a function using the trapezoidal rule.

    Args:
        func (callable): Function to integrate.
        a (float): Lower limit of integration.
        b (float): Upper limit of integration.
        n (int): Number of points (subintervals = n-1).

    Returns:
        float: Approximation of the integral.
    """
	validate_step(n)

	x_arr = np.linspace(a, b, n+1, dtype='float64')
	stride = x_arr[1] - x_arr[0]
	return np.round(np.sum((func(x_arr[:-1]) + func(x_arr[1:])) * stride /
	                      2), 5)

def simpson_rule(func, a, b, n):
	"""
	    Computes the definite integral of a function using Simpson's rule.

	    Notes:
	        - n should be odd (even number of subintervals).
	        - Uses 1/3 Simpson formula for each pair of subintervals.

	    Args:
	        func (callable): Function to integrate.
	        a (float): Lower limit of integration.
	        b (float): Upper limit of integration.
	        n (int): Number of points (subintervals = n-1).

	    Returns:
	        float: Approximation of the integral.
	    """
	validate_step(n)
	if not n % 2 == 0:
		raise OddStepWarning('Simpson rule is only implemented for'
		                      ' even number of subintervals.')


	x_arr = np.linspace(a, b, n+1, dtype='float64')
	stride = x_arr[1] - x_arr[0]
	func_arr = func(x_arr)
	add_sum = np.sum(4 * func_arr[1:-1:2])
	even_sum = np.sum(2 * func_arr[2:-1:2])
	return np.round(((func_arr[0] + add_sum + even_sum + func_arr[-1]) *
	        stride / 3), 5)


def integrals_span(func, a, b, n):
	"""
	   Returns the absolute difference between the maximum and minimum integral
	   approximations computed by left/right rectangles, trapezoidal, and
	   Simpson methods.

	   This is a helper function used by `find_common_step`.
	"""

	methods_results = np.array([
		left_rectangle(func, a, b, n),
		right_rectangle(func, a, b, n),
		trapezoidal(func, a, b, n),
		simpson_rule(func, a, b, n),
	])
	return np.trunc(np.max(methods_results) * 1000) / 1000 - np.trunc(np.min(
		methods_results) * 1000) / 1000

# Долго думал над классным супер-пупер оптимальным алгосом, наверное
# надо применить бинарный поиск
def find_common_step(func, a, b, n_start):
	"""
	    Finds the minimal even number of subintervals `n` such that the integral approximations
	    from left/right rectangles, trapezoidal, and Simpson methods agree within a given precision.

	    Args:
	        func (callable): Function to integrate.
	        a (float): Lower limit of integration.
	        b (float): Upper limit of integration.
	        n_start (int): Initial number of subintervals to start the search.

	    Returns:
	        int: Minimal number of subintervals `n` meeting the precision criterion.

	    Raises:
	        StepError: If `n_start` is not a positive integer.
	        OddStepWarning: If `n_start` is not even (Simpson requires even number of subintervals).
	"""
	validate_step(n_start)
	if not n_start % 2 == 0:
		raise OddStepWarning('To compare methods we need Simpson, which '
			'is only implemented for even number of subintervals.')

	n = n_start
	if integrals_span(func, a, b, n) == 0:
		good_n = n
		n -= 2
		while n >= 2:
			if integrals_span(func, a, b, n) > 0:
				break
			good_n = n
			n -= 2
		return good_n

	bad_n = n
	while True:
		n = n ** 2
		if integrals_span(func, a, b, n) == 0:
			good_n = n
			break
		bad_n = n

	# Осталось найти n_min между good_n и bad_n:
	n_values = np.arange(bad_n, good_n, 2, dtype='int64')
	low = 0
	high = len(n_values) - 1

	while low <= high:
		mid = (low + high) // 2
		guess = n_values[mid]
		if integrals_span(func, a, b, int(guess)) == 0:
			high = mid - 1
		else:
			low = mid + 1
	return n_values[high + 1]


def convergence_rate(method):
	"""Returns the convergence order of a numerical integration method.

	    Args:
	        method (callable): left_rectangle, right_rectangle, trapezoidal, or simpson_rule.

	    Raises:
	        ValueError: If the method is unknown.

	    Returns:
	        int: Convergence order (2, 3, or 4).
	"""

	if method == left_rectangle or method == right_rectangle:
		return 2
	elif method == trapezoidal:
		return 3
	elif method == simpson_rule:
		return 4
	else:
		raise ValueError("Unknown integration method")

def runge_rule(method, func, a, b, n_start, tolerance):
	"""Integrates a function using the Runge rule with automatic error control.

	    Args:
	        method (callable): Integration function.
	        func (callable): Function to integrate.
	        a (float): Lower limit.
	        b (float): Upper limit.
	        n_start (int): Initial number of subintervals.
	        tolerance (float): Desired error tolerance.

	    Returns:
	        tuple: (I_n, I_2n, n) — integral approximations and number of subintervals.
	"""

	if n_start < 1:
		raise StepError("n must be >= 1")

	n = n_start
	p = convergence_rate(method)

	max_iter = 100
	iter_count = 0

	while True:
		I_n = method(func, a, b, n)
		I_2n = method(func, a, b, 2*n)
		error_estimate = np.abs((I_n - I_2n) / (2 ** p -1))

		if error_estimate < tolerance:
			break
		if iter_count > max_iter:
			raise RuntimeError('Runge method did not converge.')

		n = 2*n
		iter_count += 1

	return {'I_n': I_n, 'I_2n': I_2n, 'n': n}
