
from machine import I2C, Pin, SPI
import max7219 as mx
import ds1307, bcd
from time import sleep
#from time import localtime- for use with internal rtc

i2c = I2C(Pin(5), Pin(4))
spi = SPI(1, baudrate=10000000, polarity=0, phase=0)

display = mx.Matrix8x8(spi, Pin(15), 1)
ds = ds1307.DS1307(i2c)


def get_time():
  return ds.datetime() #localtime() for internal rtc
  
def display_time():
  
  #led matrix time array
  time_matrix = [('7', [7, 6, 5, 4]),
          ('6', [7, 6, 5, 4]),
          ('5', [7, 6, 5, 4]),
          ('4', [7, 6, 5, 4])]
  #led matrix date array
  date_matrix = {'3':[3, 2, 1, 0],
          '2':[3, 2, 1, 0],
          '1':[3, 2, 1, 0],
          '0':[3, 2, 1, 0]}
  
  bcd_time = TimeToBCD(get_time())
  time = bcd_time.get_time()
  date = bcd_time.get_date()

  #[("xxxx", "xxxx"), ("xxxx", "xxxx")] => [("xxxx"), ("xxxx"), ("xxxx"), ("xxxx")]
  time = [y for x in time for y in x]
  date = [y for x in date for y in x]
  
  for i in range(4):
    for j in range(4):
      pixel = (int(date_matrix[i][0]), date_matrix[i][1][j], int(date[i][j]))
      x, y, brightness = pixel
      
      display.pixel(x, y, brightness)
      display.show()

  for i in range(4):
    for j in range(4):
      pixel = (int(time_matrix[i][0]), time_matrix[i][1][j], int(time[i][j]))
      x, y, brightness = pixel
      
      display.pixel(x, y, brightness)
      display.show()
    
class TimeToBCD:
  

  def __init__(self, time):
    self.datetime = time #(yy, mm, dd, wday, hh, mm, ss, mill_s)
    
    self.month = self.datetime[1]
    self.day = self.datetime[2]
    self.hour = self.datetime[4]
    self.min = self.datetime[5]
    
    #convert to BCD
    self.month = self.to_BCD(self.month)
    self.day = self.to_BCD(self.day)
    self.hour= self.to_BCD(self.hour)
    self.min = self.to_BCD(self.min)
    
  def to_BCD(self, intValue):
    bcd_repr = bcd.BCDConversion(intValue)
    return bcd_repr
    
  def get_time(self):
    return (self.hour, self.min)
    
  def get_date(self):
    return (self.month, self.day)
    
    
display_time()
#display.pixel(y,x,1)