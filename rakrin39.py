print("โปรแกรมคำนวณคะแนนรวม \n")
mathematics= int(input("คะแนนวิชาคณิตศาสตร์") )
science= int(input("คะแนนวิชาวิทยาศาสตร์") )
thai = int(input("คะแนนวิชาภาษาไทย") )
total_point = (science +mathematics + thai)
average = total_point /3
if average <60:
    print("ดีเยี่ยม")
elif average <80:
    print("ดีมาก")
elif average <40:
    print("ผ่าน")
print(" by mook 4/4" )
print(" thank you")


