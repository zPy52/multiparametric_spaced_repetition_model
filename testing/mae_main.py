from threading import Thread
import utils.mae_core as core


if __name__ == '__main__':
	points = (0.5, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0)

	ts = []
	for ac in points:
		for b in points:
			if len(ts) > 3:
				for t in ts:
					t.join()

				ts.clear()

				print('Clean!')

			t = Thread(target=core.main, args=(ac, b, ac))
			ts.append(t)
			t.start()

	print('Nearly finished!')

	for t in ts:
		t.join()

	ts.clear()

	print(core.get_result())