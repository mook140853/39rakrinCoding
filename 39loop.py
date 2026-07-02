import random
secret_number =random . randint(1,100)
count = 0
while True: 

    guess = int(input("ทายตัวเลขของคุณ")) 
    count += 1

    if guess > secret_number:

        print("มากไป ลองใหม่อีกคร้ง")

    elif guess < secret_number:

        print("น้อยไป ลองใหม่อิกครั้ง")

    else:

        print( "ถูกต้อง คุณทายถูก")
        
        break


