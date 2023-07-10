# EzEnrol 27/07/2022

import cv2
import time
import random

# How to enter classes:
# 
# course_names = [
#    <list of sections for course 1>,
#    <list of sections for course 2>,
#    ...
# ]
#
# course_times = [
#    [
#       <list of times for section 1 of course 1>,
#       <list of times for section 2 of course 1>,
#       ...
#    ],
#    [
#       <list of times for section 1 of course 2>,
#       <list of times for section 2 of course 2>,
#       ...
#    ],
# ]
# 
# If a timing only represents one day, repeat the letter for that day twice e.g. "FF" for Friday

padding = 10 # Required between classes in minutes

course_names = [
    [
        "CS 202"
    ],
    [
        "CS 310 L1",
        "CS 310 L2"
    ],
    [
        "CS 340 L1",
        "CS 340 L2"
    ],
    [
        "CS 370 L1",
        "CS 370 L2"
    ],
    [
        "MATH 102"
    ]
]

course_times = [
    [
        ["TR 11:00AM 12:15PM"], # We can add more times for this section such as a lab e.g. ["MW 11:00AM 12:15PM", "FF 1:00PM 2:00PM"]
    ],
    [
        ["MW 2:30PM 3:45PM"],
        ["MW 9:30AM 10:45AM"]
    ],
    [
        ["MW 11:00AM 12:15PM"],
        ["TR 12:30PM 1:45PM"]
    ],
    [
        ["MW 2:30PM 3:45PM"],
        ["MW 12:30PM 1:45PM"]
    ],
    [
        ["TR 8:00AM 9:15AM"]
    ]
]

# Convert timings to readable format
print("Converting course times:")
print("e.g.", course_times[0], "to:", end=" ")

for i in range(len(course_times)):
    for j in range(len(course_times[i])):
        for k in range(len(course_times[i][j])):
            sep = course_times[i][j][k].split(' ')
            for s in range(1, 3):
                if "PM" in sep[s] and sep[s][:2] != "12":
                    sep[s] = sep[s].replace("PM", "").replace(":", "")
                    sep[s] = str(int(sep[s]) + 1200)
                else:
                    sep[s] = sep[s].replace("PM", "").replace("AM", "").replace(":", "")
                    sep[s] = "0"*(4-len(sep[s])) + sep[s]
            course_times[i][j][k] = "".join(sep)

print(course_times[0], "\n")


# Generate all possible schedules
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


# Delete clashes
for sched in range(len(schedules)):
    for clas in range(1, len(schedules[sched])):
        for prev in range(clas):
            current = course_times[clas][schedules[sched][clas]]
            old = course_times[prev][schedules[sched][prev]]
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
                                if (oldStart-padding < currentStart <= oldEnd+padding) or (oldStart-padding <= currentEnd <= oldEnd+padding):
                                    clash = True
                                    break
                if clash: break
            if clash: break
        if clash: break
    if not clash:
        schedules_correct.append(schedules[sched])

print(len(schedules) - len(schedules_correct), "out of", len(schedules), "possible schedules have a clash!\n")

for sched in range(len(schedules_correct)):
    print("Schedule", sched+1)
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

                currentStart = currentStart//100*100 + round((currentStart%100)/60*100)
                currentEnd = currentEnd//100*100 + round((currentEnd%100)/60*100)

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
    print("Showing Schedule", sched+1, "of", len(schedules_correct), "possible schedules.")
    cv2.imshow(window_name, image)
    cv2.waitKey(0)
    filename = f"out/{sched+1}.jpg"
    cv2.imwrite(filename, image)
