import cv2
import math as mt
def fill(stack_x,stack_y):
    x=stack_x
    y=stack_y
    

def draw_circle(x, y, r,q):
    stack_x = []
    stack_y = []
    disp_x = x
    disp_y = y
    x = 0
    y = r
    delta = (1-2*r)
    error = 0
    while y >= 0:
        stack_x.append(disp_x+x)
        stack_x.append(disp_x-x)
        stack_y.append(disp_y+y)
        stack_y.append(disp_y-y)
        cv2.circle(img,(disp_x+x,disp_y+y),2,(q[0]+x,q[1]-x,q[2]+y),-1)
        cv2.circle(img,(disp_x+x,disp_y-y),2,(q[0]+x,q[1]-x,q[2]+y),-1)
        cv2.circle(img,(disp_x-x,disp_y+y),2,(q[0]+x,q[1]-x,q[2]+y),-1)
        cv2.circle(img,(disp_x-x,disp_y-y),2,(q[0]+x,q[1]-x,q[2]+y),-1)
        
        error = 2 * (delta + y) - 1
        if ((delta < 0) and (error <=0)):
            x+=1
            delta = delta + (2*x+1)
            continue
        error = 2 * (delta - x) - 1
        if ((delta > 0) and (error > 0)):
            y -= 1
            delta = delta + (1 - 2 * y)
            continue
        x += 1
        delta = delta + (2 * (x - y))
        y -= 1
    return stack_x,stack_y

img = cv2.imread("1.jpg")

#for i in range(1,300):
   #draw_circle(500+i,500-i,100,[205,92,92])



fiil_point=[]

fil_point = draw_circle(400,400,300,[205,92,92])
print(fil_point[0])

cv2.imshow("Shapes",img)

cv2.waitKey(0)

cv2.imwrite("images/saved_by_opencv.jpg", img)