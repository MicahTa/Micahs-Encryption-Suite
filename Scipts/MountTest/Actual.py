import time

def write_report(report):
    with open('/dev/vboxusb/001/002', 'rb+') as fd:
        fd.write(report)

# Wait for the device to be ready
time.sleep(2)

# Send "H"
write_report(b'\x00\x00\x0b\x00\x00\x00\x00\x00')
time.sleep(0.05)
write_report(b'\x00\x00\x00\x00\x00\x00\x00\x00')

# Send "i"
write_report(b'\x00\x00\x0c\x00\x00\x00\x00\x00')
time.sleep(0.05)
write_report(b'\x00\x00\x00\x00\x00\x00\x00\x00')

# Disconnect the gadget
with open('/sys/kernel/config/usb_gadget/mykeyboard/UDC', 'w') as udc:
    udc.write('')
