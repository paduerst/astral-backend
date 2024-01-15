import os

from binascii import hexlify, unhexlify
from dotenv import load_dotenv
from serial import Serial


this_directory = os.path.dirname(os.path.abspath(__file__))


class Camera(object):
    _output = None
    _output_string = None

    def __init__(self, output: str = '', deaf: bool = False):
        """Sony VISCA control class.

        :param output: Outbound serial port string. (default: loads from CAMERA_PORT in .env)
        :type output: str
        """
        if output == '':
            load_dotenv(dotenv_path=os.path.join(this_directory, '.env'))
            camera_port = os.getenv('CAMERA_PORT')
            if camera_port == None:
                raise RuntimeError("CAMERA_PORT not defined in .env")
            self._output_string = camera_port
        else:
            self._output_string = output

        if (deaf):
            self._timeout = 0.5
        else:
            self._timeout = 4.5

    def init(self):
        """Initializes camera object by connecting to serial port.

        :return: Camera object.
        :rtype: Camera
        """
        self._output = Serial(self._output_string, timeout=self._timeout)
        return self

    def comm(self, com, listen=1):
        """Sends hexadecimal string to serial port.

        :param com: Command string. Hexadecimal format.
        :type com: str
        :return: Success.
        :rtype: bool
        """
        self._output.write(unhexlify(com))
        return self.read(listen=listen)

    def read(self, listen=1, amount=13):
        total = ""
        subtotal = ""
        while True:
            for placeholder in range(amount):
                msg = hexlify(self._output.read()).decode('ascii')
                subtotal = subtotal + msg
                if msg == "ff" or msg == "":
                    total = total + ' ' + subtotal
                    break
            if not listen:
                break
            else:
                if subtotal == "":
                    break
                else:
                    subtotal = ""
        return total.strip()


class D30(Camera):
    """Sony EVI-D30 VISCA control class.

    Further documentation on the VISCA protocol:
    [to be added]
    """

    def on(self):
        return self.comm('8101040002FF')

    def off(self):
        return self.comm('8101040003FF')

    # TODO: Add controls for manual focus, wb, ae, brightness, shutter, iris, gain, and backlight.

    def memory(self, address=0, action=2):
        if address not in [0, 1, 2, 3, 4, 5]:
            raise ValueError('Invalid Address.')
        if action not in [0, 1, 2]:
            raise ValueError('Invalid Action.')
        command = '8101043F0'+str(action)+'0'+str(address)+'FF'
        return self.comm(command)

    @staticmethod
    def _hex2dec(hex):
        dec = int(hex, 16)
        if dec > 32768:
            dec = dec - 65536
        return dec

    @staticmethod
    def _dec2hex(dec):
        if dec < 0:
            dec = dec + 65536
        hex = '%X' % round(dec)
        if len(hex) == 1:
            hex = '000' + hex
        if len(hex) == 2:
            hex = '00' + hex
        if len(hex) == 3:
            hex = '0' + hex
        return hex

    def set_zoom(self, zoom=0.00, scale=1):
        if scale:
            zoom = self._dec2hex(zoom*1023)
        else:
            zoom = self._dec2hex(zoom)
        return self.set_zoom_str(zoom=zoom)

    def set_zoom_str(self, zoom='0000'):
        command = '81010447'
        command = command+'0'+zoom[0]+'0'+zoom[1]+'0'+zoom[2]+'0'+zoom[3]
        command = command+'FF'
        return self.comm(command)

    def set_pos(self, pan_speed=1.0, tilt_speed=1.0, pan=0.00, tilt=0.00, shift=0, scale=1):
        if scale:
            pan_speed = str(round(pan_speed*18))
            tilt_speed = str(round(tilt_speed*14))
            pan = self._dec2hex(pan*865)
            tilt = self._dec2hex(tilt*285)
        else:
            pan_speed = str(round(pan_speed))
            tilt_speed = str(round(tilt_speed))
            pan = self._dec2hex(pan)
            tilt = self._dec2hex(tilt)
        if len(pan_speed) == 1:
            pan_speed = '0' + pan_speed
        if len(tilt_speed) == 1:
            tilt_speed = '0' + tilt_speed
        return self.set_pos_str(pan_speed=pan_speed, tilt_speed=tilt_speed, pan=pan, tilt=tilt, shift=shift)

    def set_pos_str(self, pan_speed='18', tilt_speed='14', pan='0000', tilt='0000', shift=0):
        if shift:
            shift_bit = '3'
        else:
            shift_bit = '2'
        command = '8101060'+shift_bit+pan_speed+tilt_speed
        command = command+'0'+pan[0]+'0'+pan[1]+'0'+pan[2]+'0'+pan[3]
        command = command+'0'+tilt[0]+'0'+tilt[1]+'0'+tilt[2]+'0'+tilt[3]
        command = command+'FF'
        return self.comm(command)

    def home(self):
        """Moves camera to home position.

        :return: True if successful, False if not.
        :rtype: bool
        """
        return self.comm('81010604FF')

    def reset_pantilt(self):
        """Resets camera.

        :return: True if successful, False if not.
        :rtype: bool
        """
        return self.comm('81010605FF')

    def stop(self):
        """Stops camera movement (pan/tilt).

        :return: True if successful, False if not.
        :rtype: bool
        """
        return self.comm('8101060115150303FF')

    def cancel(self):
        """Cancels current command.

        :return: True if successful, False if not.
        :rtype: bool
        """
        return self.comm('81010001FF')  # Undocumented for D30.

    def left(self, amount=5):
        """Modifies pan speed to left.

        :param amount: Speed (0-24)
        :return: True if successful, False if not.
        :rtype: bool
        """
        hex_string = "%X" % amount
        hex_string = '0' + hex_string if len(hex_string) < 2 else hex_string
        s = '81010601VVWW0103FF'.replace(
            'VV', hex_string).replace('WW', str(15))
        return self.comm(s)

    def right(self, amount=5):
        """Modifies pan speed to right.

        :param amount: Speed (0-24)
        :return: True if successful, False if not.
        """
        hex_string = "%X" % amount
        hex_string = '0' + hex_string if len(hex_string) < 2 else hex_string
        s = '81010601VVWW0203FF'.replace(
            'VV', hex_string).replace('WW', str(15))
        return self.comm(s)

    def up(self, amount=5):
        """Modifies tilt speed to up.

        :param amount: Speed (0-24)
        :return: True if successful, False if not.
        """
        hs = "%X" % amount
        hs = '0' + hs if len(hs) < 2 else hs
        s = '81010601VVWW0301FF'.replace('VV', str(15)).replace('WW', hs)
        return self.comm(s)

    def down(self, amount=5):
        """Modifies tilt to down.

        :param amount: Speed (0-24)
        :return: True if successful, False if not.
        """
        hs = "%X" % amount
        hs = '0' + hs if len(hs) < 2 else hs
        s = '81010601VVWW0302FF'.replace('VV', str(15)).replace('WW', hs)
        return self.comm(s)

    def _move(self, string, a1, a2):
        h1 = "%X" % a1
        h1 = '0' + h1 if len(h1) < 2 else h1

        h2 = "%X" % a2
        h2 = '0' + h2 if len(h2) < 2 else h2
        return self.comm(string.replace('VV', h1).replace('WW', h2))

    def left_up(self, pan, tilt):
        return self._move('81010601VVWW0101FF', pan, tilt)

    def right_up(self, pan, tilt):
        return self._move('81010601VVWW0201FF', pan, tilt)

    def left_down(self, pan, tilt):
        return self._move('81010601VVWW0102FF', pan, tilt)

    def right_down(self, pan, tilt):
        return self._move('81010601VVWW0202FF', pan, tilt)

    def set_cam_ae_auto(self):
        """Changes exposure to full-auto.

        :return: True if successful, False if not.
        :rtype: bool
        """
        return self.comm('8101043900FF')

    def set_cam_ae_bright(self):
        return self.comm('810104390DFF')

    def set_bright_reset(self):
        return self.comm('8101040D00FF')

    def set_bright_up(self):
        return self.comm('8101040D02FF')

    def set_bright_down(self):
        return self.comm('8101040D03FF')

    def set_cam_focus_auto(self):
        """Turns autofocus on.

        :return: True if successful, False if not.
        :rtype: bool
        """
        return self.comm('8101043802FF')

    def set_cam_wb_auto(self):
        """White balance: Automatic mode

        :return: True if successful, False if not.
        :rtype: bool
        """
        return self.comm('8101043500FF')

    def set_cam_wb_indoor(self):
        """White balance: Indoor mode

        :return: True if successful, False if not.
        :rtype: bool
        """
        return self.comm('8101043501FF')

    def set_cam_wb_outdoor(self):
        """White balance: Outdoor mode

        :return: True if successful, False if not.
        :rtype: bool
        """
        return self.comm('8101043502FF')

    def set_wide_compensation(self, conversion):
        """Automatic Target Trace: Conversion for Wide Lens

        :conversion: float from 0 to 1
        """
        Z = int(7*conversion)
        return self.comm('81010726000'+str(Z)+'FF')

    def check_power(self):
        response = self.get_cam_power()
        bit = response[5]
        if bit == '2':
            return 1
        elif bit == '3':
            return 0
        else:
            raise ValueError('Invalid State Reading: ' +
                             str(response)+', '+str(bit))

    def get_cam_power(self):
        return self.comm('81090400FF')

    def get_zoom(self):
        zoom = self.get_zoom_str()
        zoom = self._hex2dec(zoom)
        return zoom

    def get_zoom_str(self):
        r = self.get_cam_zoom_pos()
        zoom = r[5] + r[7] + r[9] + r[11]
        return zoom

    def get_cam_zoom_pos(self):
        return self.comm('81090447FF')

    def get_cam_focus_af_mode(self):
        return self.comm('81090438FF')

    def get_cam_focus_pos(self):
        return self.comm('81090448FF')

    def get_cam_wb_mode(self):
        return self.comm('81090435FF')

    def get_cam_ae_mode(self):
        return self.comm('81090439FF')

    def get_cam_shutter_pos(self):
        return self.comm('8109044AFF')

    def get_cam_iris_pos(self):
        return self.comm('8109044BFF')

    def get_cam_gain_pos(self):
        return self.comm('8109044CFF')

    def get_cam_backlight_mode(self):
        return self.comm('81090433FF')

    def get_cam_memory(self):
        return self.comm('8109043FFF')

    def get_cam_key_lock(self):
        return self.comm('81090417FF')

    def get_cam_id(self):
        return self.comm('81090422FF')

    def get_video_system(self):
        return self.comm('81090623FF')

    def get_pantilt_mode(self, amount=5):
        return self.comm('81090610FF')

    def get_pantilt_max_speed(self, amount=5):
        return self.comm('81090611FF')

    def get_pos(self):
        pan, tilt = self.get_pos_str()
        pan = self._hex2dec(pan)
        tilt = self._hex2dec(tilt)
        return [pan, tilt]

    def get_pos_str(self):
        r = self.get_pantilt_pos()
        pan = r[5]+r[7]+r[9]+r[11]
        tilt = r[13]+r[15]+r[17]+r[19]
        return [pan, tilt]

    def get_pantilt_pos(self):
        return self.comm('81090612FF')
