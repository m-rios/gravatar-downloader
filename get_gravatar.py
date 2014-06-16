import urllib, hashlib, urllib2, sys

def get_url(email, size): 
	# construct the url
    gravatar_url = "http://www.gravatar.com/avatar/" + hashlib.md5(email.lower()).hexdigest() + "?"
    gravatar_url += urllib.urlencode({'s':str(size)})
    return gravatar_url + ".png"

##main:

if len(sys.argv) > 3 or len(sys.argv) < 2:
    print 'wrong parameters, type -h for help'
    quit()

if sys.argv[1] == '-h':
    print 'parameters: mail [size]'
    quit()

email = sys.argv[1]
if len(sys.argv) == 3:
    try:
        size = int(sys.argv[2])
    except ValueError, e:
        print 'size must be a number'
        quit()
else:
    size = 200

url = get_url(email, size)

file_name = url.split('/')[-1]
print file_name

try:
    u = urllib2.urlopen(url)
except urllib2.HTTPError, e:
    print ('email not valid: %s' %e)
    quit() 

f = open(file_name, 'wb')
meta = u.info()
file_size = int(meta.getheaders("Content-Length")[0])
print "Downloading: %s Bytes: %s" % (file_name, file_size)

file_size_dl = 0
block_sz = 8192
while True:
    buffer = u.read(block_sz)
    if not buffer:
        break

    file_size_dl += len(buffer)
    f.write(buffer)
    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
    status = status + chr(8)*(len(status)+1)
    print status,

f.close()