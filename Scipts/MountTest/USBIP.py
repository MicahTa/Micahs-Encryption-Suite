Stringfiles = {'Hi.txt': 'Hi file contents', 'Yoooo': 'Yooo contets'}

files = {}
for i in Stringfiles:
    files[i.encode('ascii')] = Stringfiles[i].encode('ascii')


# Create File

slash = '/'.encode('ascii')

header = b''
data = b''

for i in files:
    header += slash + f'{len(i)}-{len(files[i])}'.encode('ascii') + slash + i
    data += files[i]

header = str(len(header)).encode('ascii') + header

print (header)
print (data)

output = header + data