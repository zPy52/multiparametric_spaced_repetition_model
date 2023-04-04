from threading import Thread

import utils.roc_core as core


if __name__ == '__main__':
	points = (0.5, 5.0, 10.0, 15.0, 20.0, 25.0, 30.0)
	thresholds = (0.1, 0.3, 0.5, 0.7, 0.9)

	ts = []
	for ac in points:
		for b in points:
			for threshold in thresholds:
				t = Thread(target=core.main, args=(ac, b, ac, threshold))
				ts.append(t)
				t.start()

			for t in ts:
				t.join()

			ts.clear()

	for t in ts:
		t.join()

	ts.clear()

	print(core.get_result())