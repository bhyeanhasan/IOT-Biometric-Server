from django.shortcuts import render, redirect
import serial
import serial.tools.list_ports


def index(request):
    return render(request, 'finger_index.html')


def showAllPorts(request):
    ports = serial.tools.list_ports.comports()
    for port, desc, hwid in sorted(ports):
        print("{}: {} [{}]".format(port, desc, hwid))
    return redirect("finger_index")


def takeFingerPrint(request):
    WIDTH = 256
    HEIGHT = 288
    READ_LEN = int(WIDTH * HEIGHT / 2)
    DEPTH = 8
    HEADER_SZ = 54
    portSettings = ['COM3', 57600]

    def assembleHeader(width, height, depth, cTable=False):
        header = bytearray(HEADER_SZ)
        header[0:2] = b'BM'  # bmp signature
        byte_width = int((depth * width + 31) / 32) * 4
        if cTable:
            header[2:6] = ((byte_width * height) + (2 ** depth) * 4 + HEADER_SZ).to_bytes(4,
                                                                                          byteorder='little')  # file size
        else:
            header[2:6] = ((byte_width * height) + HEADER_SZ).to_bytes(4, byteorder='little')  # file size
        # header[6:10] = (0).to_bytes(4, byteorder='little')
        if cTable:
            header[10:14] = ((2 ** depth) * 4 + HEADER_SZ).to_bytes(4, byteorder='little')  # offset
        else:
            header[10:14] = (HEADER_SZ).to_bytes(4, byteorder='little')  # offset

        header[14:18] = (40).to_bytes(4, byteorder='little')  # file header size
        header[18:22] = width.to_bytes(4, byteorder='little')  # width
        header[22:26] = (-height).to_bytes(4, byteorder='little', signed=True)  # height
        header[26:28] = (1).to_bytes(2, byteorder='little')  # no of planes
        header[28:30] = depth.to_bytes(2, byteorder='little')  # depth
        # header[30:34] = (0).to_bytes(4, byteorder='little')
        header[34:38] = (byte_width * height).to_bytes(4, byteorder='little')  # image size
        header[38:42] = (1).to_bytes(4, byteorder='little')  # resolution
        header[42:46] = (1).to_bytes(4, byteorder='little')
        # header[46:50] = (0).to_bytes(4, byteorder='little')
        # header[50:54] = (0).to_bytes(4, byteorder='little')
        return header

    def getPrint():
        out = open('static/' + 'finger' + '.bmp', 'wb')
        # assemble and write the BMP header to the file
        out.write(assembleHeader(WIDTH, HEIGHT, DEPTH, True))
        for i in range(256):
            # write the colour palette
            out.write(i.to_bytes(1, byteorder='little') * 4)
        try:
            # open the port; timeout is 1 sec; also resets the arduino
            ser = serial.Serial(portSettings[0], portSettings[1], timeout=1)
        except Exception as e:
            print('Invalid port settings:', e)
            print()
            out.close()
            return
        while ser.isOpen():
            try:
                # assumes everything recved at first is printable ascii
                curr = ser.read().decode()
                # based on the image_to_pc sketch, \t indicates start of the stream
                if curr != '\t':
                    # print the debug messages from arduino running the image_to_pc sketch
                    print(curr, end='')
                    continue
                for i in range(READ_LEN):  # start recving image
                    byte = ser.read()
                    # if we get nothing after the 1 sec timeout period
                    if not byte:
                        print("Timeout!")
                        out.close()  # close port and file
                        ser.close()
                        return False
                    # make each nibble a high nibble
                    out.write((byte[0] & 0xf0).to_bytes(1, byteorder='little'))
                    out.write(((byte[0] & 0x0f) << 4).to_bytes(1, byteorder='little'))

                out.close()  # close file
                print('Image saved as', out.name)

                # read anything that's left and print
                left = ser.read(100)
                print(left.decode('ascii', errors='ignore'))
                ser.close()

                print()
                return True
            except Exception as e:
                print("Read failed: ", e)
                out.close()
                ser.close()
                return False
            except KeyboardInterrupt:
                print("Closing port.")
                out.close()
                ser.close()
                return False

    res = getPrint()
    if not res:
        print("Image extraction failed!")

    return redirect("show")


def changeFingerPrint(request):
    WIDTH = 256
    HEIGHT = 288
    READ_LEN = int(WIDTH * HEIGHT / 2)
    DEPTH = 8
    HEADER_SZ = 54
    portSettings = ['COM3', 57600]

    def assembleHeader(width, height, depth, cTable=False):
        header = bytearray(HEADER_SZ)
        header[0:2] = b'BM'  # bmp signature
        byte_width = int((depth * width + 31) / 32) * 4
        if cTable:
            header[2:6] = ((byte_width * height) + (2 ** depth) * 4 + HEADER_SZ).to_bytes(4,
                                                                                          byteorder='little')  # file size
        else:
            header[2:6] = ((byte_width * height) + HEADER_SZ).to_bytes(4, byteorder='little')  # file size
        # header[6:10] = (0).to_bytes(4, byteorder='little')
        if cTable:
            header[10:14] = ((2 ** depth) * 4 + HEADER_SZ).to_bytes(4, byteorder='little')  # offset
        else:
            header[10:14] = (HEADER_SZ).to_bytes(4, byteorder='little')  # offset

        header[14:18] = (40).to_bytes(4, byteorder='little')  # file header size
        header[18:22] = width.to_bytes(4, byteorder='little')  # width
        header[22:26] = (-height).to_bytes(4, byteorder='little', signed=True)  # height
        header[26:28] = (1).to_bytes(2, byteorder='little')  # no of planes
        header[28:30] = depth.to_bytes(2, byteorder='little')  # depth
        # header[30:34] = (0).to_bytes(4, byteorder='little')
        header[34:38] = (byte_width * height).to_bytes(4, byteorder='little')  # image size
        header[38:42] = (1).to_bytes(4, byteorder='little')  # resolution
        header[42:46] = (1).to_bytes(4, byteorder='little')
        # header[46:50] = (0).to_bytes(4, byteorder='little')
        # header[50:54] = (0).to_bytes(4, byteorder='little')
        return header

    def getPrint():
        out = open('static/' + str( request.user.username) + '.bmp', 'wb')
        # assemble and write the BMP header to the file
        out.write(assembleHeader(WIDTH, HEIGHT, DEPTH, True))
        for i in range(256):
            # write the colour palette
            out.write(i.to_bytes(1, byteorder='little') * 4)
        try:
            # open the port; timeout is 1 sec; also resets the arduino
            ser = serial.Serial(portSettings[0], portSettings[1], timeout=1)
        except Exception as e:
            print('Invalid port settings:', e)
            print()
            out.close()
            return
        while ser.isOpen():
            try:
                # assumes everything recved at first is printable ascii
                curr = ser.read().decode()
                # based on the image_to_pc sketch, \t indicates start of the stream
                if curr != '\t':
                    # print the debug messages from arduino running the image_to_pc sketch
                    print(curr, end='')
                    continue
                for i in range(READ_LEN):  # start recving image
                    byte = ser.read()
                    # if we get nothing after the 1 sec timeout period
                    if not byte:
                        print("Timeout!")
                        out.close()  # close port and file
                        ser.close()
                        return False
                    # make each nibble a high nibble
                    out.write((byte[0] & 0xf0).to_bytes(1, byteorder='little'))
                    out.write(((byte[0] & 0x0f) << 4).to_bytes(1, byteorder='little'))

                out.close()  # close file
                print('Image saved as', out.name)

                # read anything that's left and print
                left = ser.read(100)
                print(left.decode('ascii', errors='ignore'))
                ser.close()

                print()
                return True
            except Exception as e:
                print("Read failed: ", e)
                out.close()
                ser.close()
                return False
            except KeyboardInterrupt:
                print("Closing port.")
                out.close()
                ser.close()
                return False

    res = getPrint()
    if not res:
        print("Image extraction failed!")

    return redirect("profile")


def show(request):
    return render(request, 'show.html')
