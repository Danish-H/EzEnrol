import pdfplumber
import os


print("EzEnroll Parser\n")

pdf_files = [file for file in os.listdir(os.getcwd()) if file.endswith(".pdf")]
if (len(pdf_files) == 0):
    print("No PDFs found!")
    exit()

print("Found", len(pdf_files), "potential schedule PDFs:")
for count, file in enumerate(pdf_files):
    print("["+str(count+1)+"]", file)
schedule = pdf_files[int(input("Select a PDF: "))-1]

split_x = [0, 130, 310, 370, 440, 510, 740, 910]
width = 910
for i in range(len(split_x)):
    split_x[i] = split_x[i]/width

all_content = []

with pdfplumber.open(schedule) as pdf:
    for i, page in enumerate(pdf.pages[:-2]):
        print("--------------- Page", i+1, "of", len(pdf.pages)-2, "---------------")

        width = page.width
        height = page.height

        bbox = []
        for j in range(len(split_x)-1):
            bbox.append((
                split_x[j]*float(width),    0*float(height),
                split_x[j+1]*float(width),  1*float(height))
            )
        
        course_names = page.crop(bbox=bbox[0]).extract_text_lines()[:-1]
        for j in range(len(course_names)):
            if course_names[j]["text"] == "Course Code":
                course_names = course_names[j+1:]
                break
        
        course_times = page.crop(bbox=bbox[-2]).extract_text_lines()
        for j in range(len(course_times)):
            if course_times[j]["text"] == "Days Start Time End Time":
                course_times = course_times[j+1:]
                break

        new_course_names = []
        
        for j in range(len(course_times)):
            y = course_times[j]["top"]
            for k in range(len(course_names)):
                if (course_names[k]["top"] <= y and (k == len(course_names)-1 or course_names[k+1]["top"] > y)):
                    new_course_names.append(course_names[k])
                    break

        for c in range(len(new_course_names)):
            print(new_course_names[c]["text"] + "," + course_times[c]["text"])
