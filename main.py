# coding=utf-8
from course import *
import sys

if user.keep_awake:
    import wakelock


def check_status(response):
    response = response.find_all("script")[0]
    if response.find(string=re.compile(r"失败")) != None:
        print("*** Failure!")
    elif response.find(string=re.compile(r"成功")) != None:
        print("*** Success!")
    else:
        print(response)


def select_course(courseType: str, id: str, additional=""):
    if courseType == "gym":
        response = post(
            "http://elite.nju.edu.cn/jiaowu/student/elective/selectCourse.do",
            {"method": "addGymSelect", "classId": id, "_": ""},
        )
    elif courseType == "read":
        response = post(
            "http://elite.nju.edu.cn/jiaowu/student/elective/courseList.do",
            {"method": "readRenewCourseSelect", "classid": id, "type": "7"},
        )
    elif courseType == "public" or courseType == "discuss":
        response = get(
            "http://elite.nju.edu.cn/jiaowu/student/elective/courseList.do?method=submit%sRenew&classId=%s&campus=%s校区"
            % (courseType.capitalize(), id, user.campus)
        )
    elif courseType == "open":
        assert additional
        response = get(
            "http://elite.nju.edu.cn/jiaowu/student/elective/courseList.do?method=submitOpenRenew&classId=%s&academy=%s"
            % (id, additional)
        )
    else:
        print("Internal error: unknown course type!")
        return
    check_status(response)


def rush_select(courseType: str, ids: list, interval: float, additional=""):
    while True:
        try:
            print(time.asctime(time.localtime(time.time())))
            for id in ids:
                select_course(courseType, id, additional)
            time.sleep(interval)
        except KeyboardInterrupt:
            return


def process_single(
    courseType: str,
    courseList: list,
    courseName: str,
    courseTime: str,
    teacher: str,
    additional="",
):
    if courseType == "gym":
        for entry in courseList:
            if (
                courseName in entry[0]
                and courseTime in entry[1]
                and teacher in entry[2]
            ):
                print("selecting course: " + entry[0] + " " + entry[1] + " " + entry[2])
                select_course(courseType, entry[5])
    elif courseType == "read":
        for entry in courseList:
            if courseName in entry[1] and teacher in entry[2]:
                print("selecting course: " + entry[3] + " " + entry[1] + " " + entry[2])
                select_course(courseType, entry[6])
    elif courseType == "open":
        for entry in courseList:
            if (
                courseName in entry[0]
                and courseTime in entry[3]
                and teacher in entry[4]
            ):
                print("selecting course: " + entry[0] + " " + entry[3] + " " + entry[4])
                select_course(courseType, entry[7], additional)
    else:
        for entry in courseList:
            if (
                courseName in entry[0]
                and courseTime in entry[2]
                and teacher in entry[3]
            ):
                print("selecting course: " + entry[0] + " " + entry[2] + " " + entry[3])
                select_course(courseType, entry[7])


def rush_batch(
    interval: float,
    courseType: str,
    courseName: list,
    courseTime: list,
    teacher: list,
    additional="",
):
    n = len(courseName)
    if courseType == "gym":
        print(
            "\033[33;1mWarning\033[0m: this function is not carefully tested; proceed anyway."
        )  # ]]
    while True:
        print(time.asctime(time.localtime(time.time())))
        try:
            if courseType == "gym":
                courseList = list_gym(True)
            elif courseType == "read":
                courseList = list_read(True)
            elif courseType == "open":
                courseList = list_open(additional, True)
            else:
                courseList = list_public_discuss(courseType, True)
            for i in range(n):
                process_single(
                    courseType,
                    courseList,
                    courseName[i],
                    courseTime[i],
                    teacher[i],
                    additional,
                )
            time.sleep(interval)
        except KeyboardInterrupt:
            break
        except Exception as e:  # ignore all other exceptions to keep running
            print(repr(e))
            # prevent from requesting too frequently upon exceptions
            time.sleep(0 if interval <= 1 else interval)


def run_cmd(argv, opt):
    argc = len(argv)
    if argv[0] == "print":
        if argv[1] == "gym" and argc == 2:
            print_course(list_gym("h" in opt), gym_head)
        elif argv[1] == "read" and argc == 2:
            print_course(list_read("h" in opt), read_head)
        elif (argv[1] == "public" or argv[1] == "discuss") and argc == 2:
            print_course(list_public_discuss(argv[1], "h" in opt), public_discuss_head)
        elif argv[1] == "open" and argc == 3:
            print_course(list_open(argv[2], "h" in opt), open_head)
        else:
            print("Invalid command.")
    elif argv[0] == "select" and argc > 3:
        # select <interval> <type> [academy] | <id> ...
        additional = ""
        if argv[2] == "open":
            additional = argv[3]
            del argv[3]
        rush_select(argv[2], argv[3:], float(argv[1]), additional)
    elif argv[0] == "rush" and argc > 2:
        # rush <interval> <type> [academy] | <name> <time> <teacher> ...
        additional = ""
        if argv[2] == "open":
            additional = argv[3]
            del argv[3]
        names = []
        times = []
        teachers = []
        for i in range(argc // 3 - 1):
            names.append(argv[3 * i + 3])
            times.append(argv[3 * i + 4])
            teachers.append(argv[3 * i + 5])
        rush_batch(float(argv[1]), argv[2], names, times, teachers, additional)
    else:
        print("Invalid command.")


def main():
    if not user.debug and not test_authorize():
        print("Authorization failed, probabaly due to invalid cookie.")
        exit(-1)
    if user.keep_awake:
        wakelock.set(30.0)
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as file:
            line = file.readline()
        if line[-1] == "\n":
            line = line[:-1]
        argv, opt = process_cmd(line.split(" "))
        run_cmd(argv, opt)
    else:
        while True:
            argv, opt = get_cmd_stdin()
            run_cmd(argv, opt)


if __name__ == "__main__":
    main()
