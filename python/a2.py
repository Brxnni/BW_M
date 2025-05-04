from sys import set_int_max_str_digits
from math import factorial as f, floor # int = floor für positive zahlen aber egal

set_int_max_str_digits(int(1e6))

def shade_red(norm: float) -> str:
	return f"\033[38;2;{int(norm*255)};0;0m"

def lz(n: int) -> int:
	while n % 10 == 0:
		n //= 10

	return int(str(int(n)).rstrip("0")[-1])

BOLD = "\033[1m"
GREEN = "\033[92m"
BLUE = "\033[94m"
RED = "\033[91m"
END = "\033[0m"

def check_formula() -> None:
	for n in range(2, 61):
		m = floor(n/5)

		real_val = lz(f(n))
		form_val = lz(12**m * f(m) * f(n)/f(5*m))
		short_form_val = lz(2**m * f(m) * f(n)/f(5*m))

		equal = len(set([real_val, form_val, short_form_val]))
		equal = (GREEN+"Y" if equal else RED+"N") + END

		print(f"{n=} LZ(n!)={real_val} LZ(<form>)={form_val} LZ(<short>)={short_form_val} {equal}")

def all_digits() -> None:
	ago = { 2:0, 4:0, 6:0, 8:0 }
	n = 2
	for i in range(3, 10000):
		n *= i
		try: l = lz(n)
		except: break

		for k in ago.keys(): ago[k] += 1
		ago[l] = 0
		print(f"{BOLD}{BLUE}{i}{END}", " ".join(f"{BOLD}{GREEN}{k}{END}:{shade_red(v/20)}{v:<2}{END}" for k, v in ago.items()), end="\r")
	print()

def periodic() -> None:
	for n in range(1, 60):
		m = floor(n/5)
		J = f(n)/f(5*m)
		if n % 10 == 0: print("-"*20)
		print(f"{n=} {5*m=} LZ(J)={lz(J)}")

if __name__ == "__main__":
	all_digits()
