print("โปรแกรมคำนวณค่า BMI และแปลผลสุขภาพ")
kilogram = int(input("ค่าน้ำหนัก"))
height = int(input("ค่าส่วนสูง"))
BMI = kilogram /(height *height) 
Total =BMI 
print("\n หาค่าเฉลี่ยBMI =" , Total)

if BMI < 18.5:
    (print("น้ำหนักน้อย "))
elif 18.5 <BMI <22.9:
    (print("ปกติ"))
elif 23< BMI < 24.9:
    (print("น้ำหนักเกิน"))
else:
    (print("น้ำหนักเกิน"))

