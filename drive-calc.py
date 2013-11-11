#!/usr/bin/env python
import sys
import re
from optparse import OptionParser
from optparse import OptionError

conversion_table = {
    'b' : 1,
    'k' : 1024,
    'm' : 1024 ** 2,
    'g' : 1024 ** 3,
    't' : 1024 ** 4,
    'e' : 1024 ** 5
}

def to_bytes(size):
    size = str(size)
    size_re= re.compile('(-?\d\d*\.?\d*)([bBkKmMgGtTeE])')
    if size_re.match(size):
        sz, id= size_re.match(size).groups()
        id = id.lower()
        sz = int(sz)
        if conversion_table.has_key(id):
            multiplier = int(conversion_table[id])
            return int(sz * multiplier)
        else:
            raise ValueError("The size identifier '%s' is not recongized")
    else:
        return int(size)

def to_sector(sector_size, disk_size):
    bytes = to_bytes(disk_size)
    sector_sz = to_bytes(sector_size)
    return int(bytes / sector_sz)

def to_disksize(sector_size, sectors):
    sectors_sz = to_bytes(sectors)
    sector = to_bytes(sector_size)
    return int(sectors_sz * sector)

def convert_to(size, identifier='b'):
    # convert everything to bytes
    bytes = to_bytes(size)
    if identifier == 'b':
        return int(bytes)
    elif identifier in ['k', 'm', 'g', 't', 'e']:
        divisor = conversion_table[identifier]
        return int(bytes / divisor)

if __name__ == "__main__":
    cmd = sys.argv[0]
    def_sizes = ['b','k','m','g','t','e']

    parser = OptionParser()

    parser.set_usage('\n\nExamples:\n[convert disk size to sectors]\n %s --disk-size=300m --sector-size=512 --to-sector' %(cmd))

    parser.add_option('-d', '--disk-size', dest='disksize', type='str', help='disk size with identifier [b,k,m,g,t,e]')
    parser.add_option('-S', '--sectors', dest='sectors', type='str', help='The number of sectors with identifier [b,k,m,g,t,e]')
    parser.add_option('-s', '--sector-size', dest='sectorsize', type='str', help='disk sector size with identifier [b,k,m,g,t,e]')
    parser.add_option('--to-sector', dest='tosector', choices=def_sizes, default='b', help='Convert to sectors to identifier=%s' %(def_sizes))
    parser.add_option('--to-disk-size', dest='todisksize', choices=def_sizes, default='b', help='Convert to disk size to identifier=%s' %(def_sizes))

    options, pargs= parser.parse_args()

    # require disksize and sectorize options
    if options.tosector is not None and (options.disksize and options.sectorsize):
#        if not (options.disksize and options.sectorsize):
#            print('tosectors require disksize and sectorsize options')
#            sys.exit(1)
        sectors = to_sector(options.sectorsize, options.disksize)
        print convert_to(sectors, options.tosector)
    elif options.todisksize is not None and (options.sectors and options.sectorsize):
#        # requires sectors and sectorsize options
#        if not (options.sectors and options.sectorsize):
#            print('todisksize require sectors and sectorsize options')
#            sys.exit(1)
        disk_size = to_disksize(options.sectorsize, options.sectors)
        print convert_to(disk_size, options.todisksize)
