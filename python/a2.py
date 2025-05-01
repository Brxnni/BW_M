from math import factorial, floor
def lz(n): return int(str(int(n)).rstrip("0")[-1])

GREEN = "\033[92m"
RED = "\033[91m"
END = "\033[0m"

for n in range(2, 61):
	m = floor(n/5)
	print(n, m*5)

	real_val = lz(factorial(n))
	form_val = lz(12**m * factorial(m) * factorial(n)/factorial(5*m))
	short_form_val = lz(2**m * factorial(m) * factorial(n)/factorial(5*m))

	equal = len(set([real_val, form_val, short_form_val]))
	equal = (GREEN+"Y" if equal else "RED"+"N") + END

	print(f"{n=} LZ(n!)={real_val} LZ(<form>)={form_val} LZ(<short>)={short_form_val} {equal}")
