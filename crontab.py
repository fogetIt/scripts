# -*- coding: utf-8 -*-
# @Date:   2018-01-17 15:58:43
# @Last Modified time: 2018-01-17 15:58:45
import time
import sched


schedule = sched.scheduler(time.time, time.sleep)
interval = 24 * 60 * 60


def worker(delay):
    from server import main
    schedule.enter(delay, 1, main, ('test',))
    schedule.enter(delay, 2, worker, (interval, ))
    del main
    print("%s success %s" % ("\n" * 10, "\n" * 10))
    schedule.run()


if __name__ == "__main__":
    delay = 10
    schedule.enter(delay, 0, worker, (0, ))
    schedule.run()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '-s',
        '--script_name',
        help='script file name',
        type=str
    )
    args = parser.parse_args()
    main(args.script_name)