'''
pip install pyvisa.
VISA is standard for interacting with instruments from a computer.
VISA uses SCPI commands which is even more common.
pyVISA essentially  uses SCPI (skippy!) commands (e.g "syst1:diod:hour?")
https://github.com/brae-pete/ObisTimer/blob/main/OBIS_TIMER.py

OBIS561, 150 mW, is COM22

'''
import pyvisa as visa
from threading import Timer

class ObisLaser():
    def __init__(self, port="/dev/tty.usbmodem143101"):
        self.resource_manager = visa.ResourceManager()
        self.obis = self.resource_manager.open_resource(port)
        self.turnoff=False

    def get_diode_hour(self):
        hour=self.obis.query("syst1:diod:hour?",0.1).split('\r')
        self.obis.read()
        return hour[0]

    def get_model(self):
        model=self.obis.query("*IDN?").split('\r')
        self.obis.read()
        return model[0]

    def get_mode(self):
        """Only returns two of the possible modes"""
        modes={"CWP":'Constant Power', "CWC":'Constant Current'}
        mode=self.obis.query("sour1:am:sour?",0.1).split('\r')
        self.obis.read()
        return modes[mode[0]]

    def get_status(self):
        status=self.obis.query("sour1:am:stat?",0.1).split('\r')
        self.obis.read()
        return status[0]

    def get_max_power_level(self):
        power=self.obis.query("sour1:pow:nom?",0.1).split('\r')
        self.obis.read()
        return power[0]

    def get_power_level(self):
        power=self.obis.query("sour1:pow:lev:imm:ampl?",0.1).split('\r')
        self.obis.read()
        return power[0]

    def get_wavelength(self):
        wavelength=self.obis.query("syst1:inf:wav?",0.1).split('\r')
        self.obis.read()

        return wavelength[0]

    def change_status(self, on=False):
        if on:
            command="ON"
        else:
            command = "OFF"
        self.obis.write("sour1:am:stat {}".format(command))
        self.obis.read()

    def set_power_level(self,level):
        """mW input and is converted to watts"""
        level=level/1000 # convert to watts
        max1=self.get_max_power_level()
        #self.obis.read()
        if eval(max1) < level:
            return ("ERROR: Too Power Level Too High!!")
        else:
            power=self.obis.write("sour1:pow:lev:imm:ampl {}".format(level))
            self.obis.read()
            return ("Change Succesful")

    def set_timer(self, minutes=60):
        seconds=minutes*60
        self.t=Timer(seconds, self.change_status)
        self.t.start()

    def gui_set_timer(self,minutes=60):
        seconds=minutes*60
        self.t=Timer(seconds,self.changeflag)
        self.t.start()

    def changeflag(self):
        self.turnoff=True

    def close(self):
        self.obis.close()



if (__name__ == "__main__"):
    # Obis Laser Testing.
    laser=ObisLaser()
    print(laser.get_wavelength)
    laser.close()
    print("Done")
    print("OBIS OFF & CLOSED")

