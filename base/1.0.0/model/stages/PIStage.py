class PIstage(Stage):

    def __init__(self, parent=None):
        super().__init__(parent)

        ''' Physik Instrumente Specific Code    '''
        from pipython import GCSDevice, pitools
        self.pitools = pitools

        ''' Setting up the PI stages '''
        #self.pi = self.cfg.pi_parameters
        self.controllername = self.cfg.controllername
        self.pi_stages = self.cfg.stages
        self.refmode = self.cfg.refmode
        self.serialnum = self.cfg.serialnum
        self.pidevice = GCSDevice(self.controllername)
        self.pidevice.ConnectUSB(serialnum=self.serialnum)
        self.pitools.startup(self.pidevice, stages=list(self.pi_stages), refmodes=list(self.refmode))
        self.block_till_controller_is_ready()
        self.startfocus = self.cfg.startfocus
        # Move the Focusing Stage to the Start Position
        self.pidevice.MOV(5, self.startfocus / 1000)

    def __del__(self):
        try:
            '''Close the PI connection'''
            self.pidevice.unload()
            print('Stage disconnected')
        except:
            print('Error while disconnecting the PI stage')

    def report_position(self):
        positions = self.pidevice.qPOS(self.pidevice.axes)
        self.x_pos = round(positions['1'] * 1000, 2)
        self.y_pos = round(positions['2'] * 1000, 2)
        self.z_pos = round(positions['3'] * 1000, 2)
        self.f_pos = round(positions['5'] * 1000, 2)
        self.theta_pos = positions['4']
        self.create_position_dict()

        self.int_x_pos = self.x_pos + self.int_x_pos_offset
        self.int_y_pos = self.y_pos + self.int_y_pos_offset
        self.int_z_pos = self.z_pos + self.int_z_pos_offset
        self.int_f_pos = self.f_pos + self.int_f_pos_offset
        self.int_theta_pos = self.theta_pos + self.int_theta_pos_offset
        self.create_internal_position_dict()

        print(self.int_position_dict)

    def move_relative(self, dict, wait_until_done=False):
        ''' PI move relative method
        Lots of implementation details in here, should be replaced by a facade
        '''
        if 'x_rel' in dict:
            x_rel = dict['x_rel']
            if self.x_min < self.x_pos + x_rel and self.x_max > self.x_pos + x_rel:
                x_rel = x_rel / 1000
                self.pidevice.MVR({1: x_rel})
            else:
                print('Relative movement stopped: X Motion limit would be reached!', 1000)

        if 'y_rel' in dict:
            y_rel = dict['y_rel']
            if self.y_min < self.y_pos + y_rel and self.y_max > self.y_pos + y_rel:
                y_rel = y_rel / 1000
                self.pidevice.MVR({2: y_rel})
            else:
                print('Relative movement stopped: Y Motion limit would be reached!', 1000)

        if 'z_rel' in dict:
            z_rel = dict['z_rel']
            if self.z_min < self.z_pos + z_rel and self.z_max > self.z_pos + z_rel:
                z_rel = z_rel / 1000
                self.pidevice.MVR({3: z_rel})
            else:
                print('Relative movement stopped: z Motion limit would be reached!', 1000)

        if 'theta_rel' in dict:
            theta_rel = dict['theta_rel']
            if self.theta_min < self.theta_pos + theta_rel and self.theta_max > self.theta_pos + theta_rel:
                self.pidevice.MVR({4: theta_rel})
            else:
                print('Relative movement stopped: theta Motion limit would be reached!', 1000)

        if 'f_rel' in dict:
            f_rel = dict['f_rel']
            if self.f_min < self.f_pos + f_rel and self.f_max > self.f_pos + f_rel:
                f_rel = f_rel / 1000
                self.pidevice.MVR({5: f_rel})
            else:
                print('Relative movement stopped: f Motion limit would be reached!', 1000)

        if wait_until_done == True:
            self.pitools.waitontarget(self.pidevice)

    def move_absolute(self, dict, wait_until_done=False):
        '''
        PI move absolute method

        Lots of implementation details in here, should be replaced by a facade

        TODO: Also lots of repeating code.
        TODO: DRY principle violated
        '''

        if 'x_abs' in dict:
            x_abs = dict['x_abs']
            x_abs = x_abs - self.int_x_pos_offset
            if self.x_min < x_abs and self.x_max > x_abs:
                ''' Conversion to mm and command emission'''
                x_abs = x_abs / 1000
                self.pidevice.MOV({1: x_abs})
            else:
                print('Absolute movement stopped: X Motion limit would be reached!', 1000)

        if 'y_abs' in dict:
            y_abs = dict['y_abs']
            y_abs = y_abs - self.int_y_pos_offset
            if self.y_min < y_abs and self.y_max > y_abs:
                ''' Conversion to mm and command emission'''
                y_abs = y_abs / 1000
                self.pidevice.MOV({2: y_abs})
            else:
                print('Absolute movement stopped: Y Motion limit would be reached!', 1000)

        if 'z_abs' in dict:
            z_abs = dict['z_abs']
            z_abs = z_abs - self.int_z_pos_offset
            if self.z_min < z_abs and self.z_max > z_abs:
                ''' Conversion to mm and command emission'''
                z_abs = z_abs / 1000
                self.pidevice.MOV({3: z_abs})
            else:
                print('Absolute movement stopped: Z Motion limit would be reached!', 1000)

        if 'f_abs' in dict:
            f_abs = dict['f_abs']
            f_abs = f_abs - self.int_f_pos_offset
            if self.f_min < f_abs and self.f_max > f_abs:
                ''' Conversion to mm and command emission'''
                f_abs = f_abs / 1000
                self.pidevice.MOV({5: f_abs})
            else:
                print('Absolute movement stopped: F Motion limit would be reached!', 1000)

        if 'theta_abs' in dict:
            theta_abs = dict['theta_abs']
            theta_abs = theta_abs - self.int_theta_pos_offset
            if self.theta_min < theta_abs and self.theta_max > theta_abs:
                ''' No Conversion to mm !!!! and command emission'''
                self.pidevice.MOV({4: theta_abs})
            else:
                print('Absolute movement stopped: Theta Motion limit would be reached!', 1000)

        if wait_until_done == True:
            self.pitools.waitontarget(self.pidevice)

    def stop(self):
        self.pidevice.STP(noraise=True)

    def load_sample(self):
        y_abs = self.cfg.y_load_position / 1000
        self.pidevice.MOV({2: y_abs})

    def unload_sample(self):
        y_abs = self.cfg.y_unload_position / 1000
        self.pidevice.MOV({2: y_abs})

    def go_to_rotation_position(self, wait_until_done=False):
        x_abs = self.x_rot_position / 1000
        y_abs = self.y_rot_position / 1000
        z_abs = self.z_rot_position / 1000
        self.pidevice.MOV({1: x_abs, 2: y_abs, 3: z_abs})
        if wait_until_done == True:
            self.pitools.waitontarget(self.pidevice)

    def block_till_controller_is_ready(self):
        '''
        Blocks further execution (especially during referencing moves)
        till the PI controller returns ready
        '''
        blockflag = True
        while blockflag:
            if self.pidevice.IsControllerReady():
                blockflag = False
            else:
                time.sleep(0.1)
