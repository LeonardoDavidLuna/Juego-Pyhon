#!/usr/bin/python
import smbus
import math
import time
# Register
power_mgmt_1 = 0x6b
power_mgmt_2 = 0x6c
 
def read_byte(reg):
    return bus.read_byte_data(address, reg)
 
def read_word(reg):
    h = bus.read_byte_data(address, reg)
    l = bus.read_byte_data(address, reg+1)
    value = (h << 8) + l
    return value
 
def read_word_2c(reg):
    val = read_word(reg)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
 
def dist(a,b):
    return math.sqrt((a*a)+(b*b))
 
def get_y_rotation(x,y,z):
    radians = math.atan2(x, dist(y,z))
    return -math.degrees(radians)
 
def get_x_rotation(x,y,z):
    radians = math.atan2(y, dist(x,z))
    return math.degrees(radians)

def get_z_rotation(x,y,z):
    radians = math.atan2(y, dist(z,x))
    return math.degrees(radians)
while True:
    bus = smbus.SMBus(1) # bus = smbus.SMBus(0) fuer Revision 1
    address = 0x68       # via i2cdetect
     
    # Aktivieren, um das Modul ansprechen zu koennen
    bus.write_byte_data(address, power_mgmt_1, 0)
     
    #print "Gyroskop"
    #print "--------"

    gyroskop_xout = read_word_2c(0x43)
    gyroskop_yout = read_word_2c(0x45)
    gyroskop_zout = read_word_2c(0x47)
     
    #print "gyroskop_xout: ", ("%5d" % gyroskop_xout), " skaliert: ", (gyroskop_xout / 131)
    #print "gyroskop_yout: ", ("%5d" % gyroskop_yout), " skaliert: ", (gyroskop_yout / 131)
    #print "gyroskop_zout: ", ("%5d" % gyroskop_zout), " skaliert: ", (gyroskop_zout / 131)
     
    #print
    #print "Beschleunigungssensor"
    #print "---------------------"
     
    x = read_word_2c(0x3b)
    y = read_word_2c(0x3d)
    z = read_word_2c(0x3f)
     
    x2 = x / 16384.0
    y2 = y / 16384.0
    z2 = z / 16384.0
     
    print "x: ", ("%6d" % x), " skaliert: ", x2
    print "y: ", ("%6d" % y), " skaliert: ", y2
    print "z: ", ("%6d" % z), " skaliert: ", z2

    #f=open("angulos.txt","w")

    #f.write(""+str(get_x_rotation(x2, y2, z2)))
    #f.write("\n"+str(get_y_rotation(x2, y2, z2)))
    #f.write("\n"+str(get_z_rotation(x2, y2, z2)))
    #f.close()
    #time.sleep(0.1)
    #print "X Rotation: " , get_x_rotation(x2, y2, z2)
    #print "Y Rotation: " , get_y_rotation(x2, y2, z2)#!/usr/bin/python
