# coding=utf-8
from utils import *
import bs4, re

gym_head = ["名称", "时间", "教师", "已选人数", "限额", "选课id"]
read_head = ["课程号", "名称", "教师", "类别", "限额", "已选", "选课id"]
public_discuss_head = ["名称", "学分", "时间", "教师", "限额", "已选", "备注", "选课id"]
open_head = ["名称", "学分", "年级", "时间", "教师", "限额", "已选", "选课id"]


def test_authorize() -> bool:  # test if login is successful
    soup = get("http://elite.nju.edu.cn/jiaowu/student/index.do")
    if soup.find(string=re.compile(r"选课")) != None:
        return True
    elif soup.find(string=re.compile(r"密码")) != None:
        return False
    else:
        print("Unknown error occured while testing authorization.")
        exit(-1)


def print_course(courseList: list, label: list):
    """
    print courseList with label(No. excluded)
    """
    print("序号", end="\t")
    for t in label:
        print(t, end="\t")
    print("")
    i = 1
    for entry in courseList:
        print(i, "\t", end="")
        i = i + 1
        for item in entry:
            print(item, end="\t")
        print("\n", end="")


def list_gym(hideInvalid=False) -> list:
    soup = post(
        "http://elite.nju.edu.cn/jiaowu/student/elective/courseList.do",
        {"method": "gymCourseList"},
    )
    courseList = []
    if len(soup.find_all("tbody")) != 0:
        for courseTag in soup.find_all("tbody")[0].find_all("tr"):
            detailList = []
            for detailTag in courseTag.find_all("td"):
                if len(detailTag.contents) > 1:
                    idStr = str(detailTag.contents[1])
                    try:
                        detailList.append(re.search(r"[0-9]+", idStr).group())
                    except AttributeError:
                        if hideInvalid:
                            continue
                        detailList.append("selected")
                else:
                    detail = str(detailTag.contents[0])
                    detail = re.sub(r"[ \xa0\r\n\t]", "", detail)
                    detailList.append(detail)
            if not hideInvalid or int(detailList[3]) < int(detailList[4]):
                courseList.append(detailList)
        print_course(courseList, gym_head)
    else:
        print("Nothing can be selected, probably because it has not started yet")
    return courseList


def list_read(hideInvalid=False) -> list:
    soup = post(
        "http://elite.nju.edu.cn/jiaowu/student/elective/courseList.do",
        {"method": "readRenewCourseList", "type": "7"},
    )
    courseList = []
    if len(soup.find_all("tbody")) != 0:
        for courseTag in soup.find_all("tbody")[0].find_all("tr"):
            detailList = []
            for detailTag in courseTag.find_all("td"):
                if not detailTag.contents:
                    detailList.append("cannot select")
                elif type(detailTag.contents[0]) == bs4.element.Tag:
                    idStr = str(detailTag)
                    try:
                        detailList.append(re.search(r"[0-9]+", idStr).group())
                    except AttributeError:
                        if hideInvalid:
                            continue
                        detailList.append("selected")
                else:
                    detail = str(detailTag.contents[0])
                    detail = re.sub(r"[ \xa0\r\n\t]", "", detail)
                    detailList.append(detail)
            if not hideInvalid or int(detailList[5]) < int(detailList[4]):
                courseList.append(detailList)
        print_course(courseList, read_head)
    else:
        print("Nothing can be selected, probably because it has not started yet")
    return courseList


def list_public_discuss(courseType: str, hideInvalid=False) -> list:
    soup = get(
        "http://elite.nju.edu.cn/jiaowu/student/elective/courseList.do?method=%sRenewCourseList&campus=%s校区"
        % (courseType, user.campus)
    )
    courseList = []
    if len(soup.find_all("table")) != 0:
        for courseTag in soup.find_all("table")[0].find_all("tr")[1:]:
            detailList = []
            for detailTag in courseTag.find_all("td")[2:]:
                if not detailTag.contents:
                    detailList.append("none")
                elif type(detailTag.contents[0]) == bs4.element.Tag:
                    idStr = str(detailTag)
                    try:
                        detailList.append(re.search(r"[0-9]+", idStr).group())
                    except AttributeError:
                        if hideInvalid:
                            continue
                        detailList.append("selected")
                else:
                    detail = str(detailTag.contents[0])
                    detail = re.sub(r"[ \xa0\r\n\t]", "", detail)
                    detailList.append(detail)
            if not hideInvalid or int(detailList[5]) < int(detailList[4]):
                courseList.append(detailList)
        print_course(courseList, public_discuss_head)
    else:
        print("Nothing can be selected, probably because it has not started yet")
    return courseList


def list_open(academy: str, hideInvalid=False) -> list:
    soup = get(
        "http://elite.nju.edu.cn/jiaowu/student/elective/courseList.do?method=openRenewCourse&campus=全部校区&academy="
        + academy
    )
    courseList = []
    if len(soup.find_all("table")) != 0:
        for courseTag in soup.find_all("table")[0].find_all("tr")[2:]:
            detailList = []
            for detailTag in courseTag.find_all("td")[2:]:
                if not detailTag.contents:
                    detailList.append("none")
                elif type(detailTag.contents[0]) == bs4.element.Tag:
                    idStr = str(detailTag)
                    try:
                        detailList.append(re.search(r"[0-9]+", idStr).group())
                    except AttributeError:
                        if hideInvalid:
                            continue
                        detailList.append("cannot select")
                else:
                    detail = str(detailTag.contents[0])
                    detail = re.sub(r"[ \xa0\r\n\t]", "", detail)
                    detailList.append(detail)
            if not hideInvalid or int(detailList[6]) < int(detailList[5]):
                courseList.append(detailList)
        print_course(courseList, public_discuss_head)
    else:
        print("Nothing can be selected, probably because it has not started yet")
    return courseList


def test():
    list_open("11")


if __name__ == "__main__":
    test()
