# EzEnrol 27/07/2022

import cv2
import time
import random

course_names = [["CS 300 L1", "CS 300 L2"],
                ["CS 331 L1", "CS 331 L2"],
                ["CS 382 L1", "CS 382 L2"],
                ["CS 202"],
                ["MATH 102"]]

course_times = [[["MW 11:00AM 12:15PM"], ["MW 12:30PM 1:45PM"]],
                [["TR 12:30PM 1:45PM"], ["MW 3:30PM 4:45PM"]],
                [["MW 12:30PM 1:45PM"], ["TR 12:30PM 1:45PM"]],
                [["MW 11:00AM 12:15PM"]],
                [["MW 10:00AM 11:15AM"]]]

print(course_times)

for i in range(len(course_times)):
    for j in range(len(course_times[i])):
        for k in range(len(course_times[i][j])):
            sep = course_times[i][j][k].split(' ')
            print(sep)
            for s in range(1, 3):
                if "PM" in sep[s] and sep[s][:2] != "12":
                    sep[s] = sep[s].replace("PM", "").replace(":", "")
                    sep[s] = str(int(sep[s]) + 1200)
                else:
                    sep[s] = sep[s].replace("PM", "").replace("AM", "").replace(":", "")
                    sep[s] = "0"*(4-len(sep[s])) + sep[s]
            print(sep)
            course_times[i][j][k] = "".join(sep)

print(course_times)

for i in range(2):
    for j in range(2):
        for k in range(2):
            for l in range(1):
                for m in range(2):
                    print(i, j, k, l, m)
def generate_schedules(course_names, current_schedule=[]):
    if len(course_names) == 0:
        return [tuple(current_schedule)]
    
    schedules = []
    for i in range(len(course_names[0])):
        new_schedule = current_schedule + [i]
        schedules.extend(generate_schedules(course_names[1:], new_schedule))
    
    return schedules

schedules = generate_schedules(course_names)
schedules_correct = []

for sched in range(len(schedules)):
    for clas in range(1, len(schedules[sched])):
        for prev in range(clas):
            current = course_times[clas][schedules[sched][clas]]
            old = course_times[prev][schedules[sched][prev]]
            print("current", current)
            print("old", old)

            clash = False

            for a in current:
                for aD in range(2):
                    currentDay = a[aD]
                    currentStart = int(a[-8:-4])
                    currentEnd = int(a[-4:])
                    for b in old:
                        for bD in range(2):
                            oldDay = b[bD]
                            oldStart = int(b[-8:-4])
                            oldEnd = int(b[-4:])

                            if currentDay == oldDay:
                                print(oldStart, oldEnd, currentStart, currentEnd)
                                if (oldStart-10 < currentStart <= oldEnd) or (oldStart <= currentEnd <= oldEnd):
                                    clash = True
                                    break
                if clash:
                    break
            if clash:
                break
        if clash:
            break
    if not clash:
        schedules_correct.append(schedules[sched])

print(schedules_correct)

schedules_correct = schedules[::]

print(len(schedules) - len(schedules_correct), "out of", len(schedules), "possible schedules have a clash!")

for sched in range(len(schedules_correct)):
    for clas in range(len(schedules_correct[sched])):
        print(course_names[clas][schedules_correct[sched][clas]], course_times[clas][schedules_correct[sched][clas]])
    print()

for sched in range(len(schedules_correct)):
    path = "template.png"
    image = cv2.imread(path)
    window_name = 'Image'
    for t in range(800, 2000, 100):
        s = "0" * (4 - len(str(t))) + str(t)
        start_point = (0, round(t / 2))
        end_point = (1220, round(t / 2))
        color = (230, 230, 230)
        thickness = 2
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
        start_point = (1220, round(t/2))
        end_point = (1380, round(t/2))
        color = (100, 100, 100)
        thickness = 2
        image = cv2.rectangle(image, start_point, end_point, color, thickness)
        text_point = (start_point[0], start_point[1]+15)
        image = cv2.putText(image, s, text_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        image = cv2.putText(image, f"Iteration No. {sched+1}", (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 2, (20, 20, 20), 4)

    for clas in range(len(schedules_correct[sched])):
        current = course_times[clas][schedules_correct[sched][clas]]
        for a in current:
            for aD in range(2):
                days = ['M','T','W','R','F','S','U']
                currentDay = days.index(a[aD])
                currentStart = int(a[-8:-4])
                currentEnd = int(a[-4:])

                start_point = (currentDay*200+3, round(currentStart/2))
                end_point = ((currentDay+1)*200-3, round(currentEnd/2))
                text_point = ((currentDay*200)+7, round(currentEnd/2)-20)
                text_point2 = ((currentDay*200)+7, round(currentEnd/2)-4)
                color = (30, 30, 100+40*clas)
                thickness = -1

                lbl = course_names[clas][schedules_correct[sched][clas]]

                image = cv2.rectangle(image, start_point, end_point, color, thickness)
                color = (255, 255, 255)
                image = cv2.putText(image, lbl, text_point, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1)

    # Displaying the image
    cv2.destroyAllWindows()
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    filename = f"out/{sched}.jpg"
    cv2.imwrite(filename, image
                )
    print("shown")
