import math as mt
import PIL as pp
import cv2
import numpy as np


INSIDE = 0  
LEFT = 1  
RIGHT = 2 
BOTTOM = 4  
TOP = 8 
WIDTH = 1366
HEIGHT = 768
X0=1366//2
Y0=768//2
def brez(x1,y1,x2,y2):
    x = x1
    y = y1
    cord = []
    ycord = []
    dx = abs(x2-x1)
    dy = abs(y2-y1)
    sign_x = 1 if x2-x1>0 else -1 if x2-x1<0 else 0
    sign_y = 1 if y2-y1>0 else -1 if y2-y1<0 else 0
    if dy > dx:
        time = dx
        dx = dy
        dy = time
        swap = 1
    else : swap = 0
    e = 2 *dy - dx
    for i in range(dx):
        cord.append([x,y])
        cv2.circle(img,(x,y),2,(0,255,0),-1)
        while(e>0):
            if swap==1:
                x = x+sign_x
            else: y = y+sign_y
            e = e-2*dx
        if swap ==1:
            y=y+sign_y
        else: x=x+sign_x
        e = e+2*dy
    return cord
def zatravka(x,y,coord):
    stek = [[x,y]]
    border = coord
    paint =[]
    while len(stek)>0:
        xx,yy=stek.pop()
        if paint.count([xx,yy])==0:
            cv2.circle(img,(xx,yy),2,(0,255,0),-1)
            paint.extend([[xx,yy]])
        if paint.count([xx+1,yy])==0 and border.count([xx+1,yy])==0:
            stek.extend([[xx+1,yy]])
        if paint.count([xx,yy+1])==0 and border.count([xx,yy+1])==0:
            stek.extend([[xx,yy+1]])
        if paint.count([xx-1,yy])==0 and border.count([xx-1,yy])==0:
            stek.extend([[xx-1,yy]])
        if paint.count([xx,yy-1])==0 and border.count([xx,yy-1])==0:
            stek.extend([[xx,yy-1]])
    return paint  
def line_zatravka(pos_x,pos_y,coord):
    stek = [[pos_x,pos_y]]
    border= coord
    paint =[]
    while len(stek)>0:
        x,y = stek.pop()
        cv2.circle(img,(x,y),2,(0,255,0),-1)
        paint.extend([[x,y]])
        time_x = x
        x=x+1
        while border.count([x,y])==0:
            cv2.circle(img,(x,y),2,(0,255,0),-1)
            paint.extend([[x,y]])
            x=x+1
        x_r = x-1
        x=time_x
        x=x-1
        while border.count([x,y])==0:
            cv2.circle(img,(x,y),2,(0,255,0),-1)
            paint.extend([[x,y]])
            x=x-1
        x_l=x+1
        # поиск затравки на строку выше
        x=x_l
        y=y+1
        while x<=x_r:
            flag=0
            while paint.count([x,y])==0 and (border.count([x,y])==0 and x<x_r):
                if flag==0:
                    flag=1
                x=x+1
            if flag==1:
                if x==x_r and paint.count([x,y])==0 and border.count([x,y])==0:
                    stek.extend([[x,y]])
                else:stek.extend([[x-1,y]])
                flag=0
            x_in = x
            while paint.count([x,y])>0 or border.count([x,y])>0 and x<x_r:
                x=x+1
            if x==x_in:
                x=x+1
        x=x_l
        y=y-2
        while x<=x_r:
            flag=0
            while paint.count([x,y])==0 and (border.count([x,y])==0 and x<x_r):
                if flag==0:
                    flag=1
                x=x+1
            if flag==1:
                if x==x_r and paint.count([x,y])==0 and border.count([x,y])==0:
                    stek.extend([[x,y]])
                else:stek.extend([[x-1,y]])
                flag=0
            x_in = x
            while paint.count([x,y])>0 or border.count([x,y])>0 and x<x_r:
                x=x+1
            if x==x_in:
                x=x+1
    return paint
def computeCode(x, y):
    code = INSIDE
    if x < x_min:  # to the left of rectangle
        code |= LEFT
    elif x > x_max:  # to the right of rectangle
        code |= RIGHT
    if y < y_min:  # below the rectangle
        code |= BOTTOM
    elif y > y_max:  # above the rectangle
        code |= TOP
    return code       
def cohenSutherlandClip(x1, y1, x2, y2):
   
    code1 = computeCode(x1, y1)
    code2 = computeCode(x2, y2)
    accept = False
 
    while True:
 
        # If both endpoints lie within rectangle
        if code1 == 0 and code2 == 0:
            accept = True
            break
 
        # If both endpoints are outside rectangle
        elif (code1 & code2) != 0:
            break
 
        # Some segment lies within the rectangle
        else:
 
            # Line needs clipping
            # At least one of the points is outside,
            # select it
            x = 1.0
            y = 1.0
            if code1 != 0:
                code_out = code1
            else:
                code_out = code2
 
            # Find intersection point
            # using formulas y = y1 + slope * (x - x1),
            # x = x1 + (1 / slope) * (y - y1)
            if code_out & TOP:
                # Point is above the clip rectangle
                x = x1 + (x2 - x1) * (y_max - y1) / (y2 - y1)
                y = y_max
            elif code_out & BOTTOM:
                # Point is below the clip rectangle
                x = x1 + (x2 - x1) * (y_min - y1) / (y2 - y1)
                y = y_min
            elif code_out & RIGHT:
                # Point is to the right of the clip rectangle
                y = y1 + (y2 - y1) * (x_max - x1) / (x2 - x1)
                x = x_max
            elif code_out & LEFT:
                # Point is to the left of the clip rectangle
                y = y1 + (y2 - y1) * (x_min - x1) / (x2 - x1)
                x = x_min
 
            # Now intersection point (x, y) is found
            # We replace point outside clipping rectangle
            # by intersection point
            if code_out == code1:
                x1 = x
                y1 = y
                code1 = computeCode(x1, y1)
            else:
                x2 = x
                y2 = y
                code2 = computeCode(x2, y2)
 
    if accept:
        print("Line accepted from %.2f, %.2f to %.2f, %.2f" % (x1, y1, x2, y2))
        return x1 , y1, x2,y2
        # Here the user can add code to display the rectangle
        # along with the accepted (portion of) lines
    else:
        print("Line rejected")   
def draw(x):
    coord=[]
    coord.extend(x)
    flag = 0
    while(len(coord)>0):
        if(len(coord)==1):
            x1,y1=x2,y2
            x2,y2 = coord.pop()
            x2 = x2+X0
            if(y2<0):
                y2 = y2*-1
                y2 = y2+Y0
            else:
                y2 = Y0-y2
            brez(x1,y1,x2,y2)
            brez(first_x,first_y,x2,y2)
            continue
        if(flag==0):
            x1,y1 = coord.pop()
            x1 = x1+X0
            if(y1<0):
                y1 = y1*-1
                y1 = y1+Y0
            else:
                y1 = Y0-y1
            first_x,first_y=x1,y1
            x2,y2 =coord.pop()
            x2 = x2+X0
            if(y2<0):
                y2 = y2*-1
                y2 = y2+Y0
            else:
                y2 = Y0-y2
            brez(x1,y1,x2,y2)
            flag = 1
        else:
            x1,y1=x2,y2
            x2,y2 = coord.pop()
            x2 = x2+X0
            if(y2<0):
                y2 = y2*-1
                y2 = y2+Y0
            else:
                y2 = Y0-y2
            brez(x1,y1,x2,y2)
def matmult(m1,m2):
    r=[]
    m=[]
    for i in range(len(m1)):
        for j in range(len(m2[0])):
            sums=0
            for k in range(len(m2)):
                sums=sums+(m1[i][k]*m2[k][j])
            r.append(sums)
        m.append(r)
        r=[]
    return m
def transform(crd,ind):
    coord=[]
    coord.extend(crd)
    for i in coord:
        i.extend([1])
    if ind==1:
        res = matmult(coord,[[2,0,0],
                             [0,2,0],
                             [0,0,1]])
        for i in res:
            i.pop()   
        return(res)
    
    if ind ==2:
        res = matmult(coord,[[-1,0,0],
                             [0,-1,0],
                             [0,0,1]])
        for i in res:
            i.pop()   
        return(res)
    
    if ind ==3:
        res = matmult(coord,[[1,2,0],
                             [0,1,0],
                             [0,0,1]])
        for i in res:
            i.pop()   
        return(res)
    
    if ind ==4:
        res = matmult(coord,[[1,2,0],
                             [2,1,0],
                             [0,0,1]])
        for i in res:
            i.pop()   
        return(res)

    if ind==5:
        res = matmult(coord,[[mt.cos(mt.radians(45)),mt.sin(mt.radians(45)),0],
                             [-mt.sin(mt.radians(45)),mt.cos(mt.radians(45)),0],
                             [0,0,1]])
        for i in res:
            i.pop()
        res = [[int(i) for i in j] for j in res]   
        return(res)

    if ind ==6:
        res = matmult(coord,[[1,0,0],
                             [0,1,0],
                             [0,40,1]])
        for i in res:
            i.pop()   
        return(res)
    
    if ind ==7:
        check = []
        last = []
    
        res = matmult(coord,[[1,0,0.001],
                             [0,1,0.001],
                             [100,100,1]])
        
        for i in res:
            check.append(i.pop())

        for i in range(len(res)):
            for j in range(len(res[i])):
                last.append(int( res[i][j]/check[i]))
        
        res =[]

        for i in range(len(last)-1):
            if(i%2==0):
                res.extend([[last[i],last[i+1]]])
        print(res)
        return(res)

    

img = cv2.imread("1.jpg")


#==== Все что связано с заливкой =====
# coord =brez(100,750,70,100)
# coord.extend(brez(100,750,100,200))
# coord.extend(brez(100,200,200,70))
# coord.extend(brez(200,70,70,100))
# coord.sort()
# brez(100,100,110,110) координаты для заливки
#zatravka(100,100,coord)
#res = line_zatravka(100,100,coord)
#==== Все что связано с заливкой =====

#=== Все что связано с отсечением ====
# coord = brez(500,100,1000,100)
# coord.extend(brez(500,300,1000,300))
# coord.extend(brez(500,100,500,300))
# coord.extend(brez(1000,100,1000,300))
# x_max,y_max = coord.pop()
# y_max+=1
# x_min,y_min = coord[0]
#brez(550,150,900,250)
#x1,y1,x2,y2 = cohenSutherlandClip(550,150,900,250)
#brez(x1,y1,x2,y2)
#brez(450,150,550,150)
#x1,y1,x2,y2 = cohenSutherlandClip(450,150,550,150)
#brez(int(x1),int(y1),int(x2),int(y2))
#brez(450,150,900,350)
#x1,y1,x2,y2 = cohenSutherlandClip(450,150,900,350)
#brez(int(x1),int(y1),int(x2),int(y2))


# ==== Всче что связано с преобразованием ====
res = transform([[10,10],
                 [10,100],
                 [100,100],
                 [100,10]],1)
brez(0,Y0,WIDTH,Y0)
brez(X0,0,X0,HEIGHT)
draw([[10,10],[10,100],[100,100],[100,10]])
res =draw(transform([[10,10],
                   [10,100],
                   [100,100],
                   [100,10]],7))
# print(res)
# ==== Всче что связано с преобразованием ====




# show image
cv2.imshow("Shapes", img) # Window name -> Shapes

# wait for key before closing the window
cv2.waitKey(0)

# save image
cv2.imwrite("images/saved_by_opencv.jpg", img)