from math import factorial as f, floor
def lz(n): return int(str(int(n)).rstrip("0")[-1])

BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
END = "\033[0m"

def check_form():
	for n in range(2, 61):
		m = floor(n/5)
		print(n, m*5)

		real_val = lz(f(n))
		form_val = lz(12**m * f(m) * f(n)/f(5*m))
		short_form_val = lz(2**m * f(m) * f(n)/f(5*m))

		equal = len(set([real_val, form_val, short_form_val]))
		equal = (GREEN+"Y" if equal else RED+"N") + END

		print(f"{n=} LZ(n!)={real_val} LZ(<form>)={form_val} LZ(<short>)={short_form_val} {equal}")

def all_digits():
	ago = { 2:0, 4:0, 6:0, 8:0 }
	n = 2
	while True:
		try: l = lz(f(n))
		except: break

		for k in ago.keys(): ago[k] += 1
		ago[l] = 0
		print(f"{BOLD}{RED}{n}{END}", " ".join(f"{BOLD}{GREEN}{k}{END}:{v:<2}" for k, v in ago.items()))
		n += 1

def periodic():
	for n in range(1, 60):
		m = floor(n/5)
		J = f(n)/f(5*m)
		print(f"{n=} {5*m=} LZ(J)={lz(J)}")

if __name__ == "__main__": check_form()
