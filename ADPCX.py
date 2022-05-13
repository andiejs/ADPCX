import PIL
from PIL import Image
from PIL import ImageFilter
from PIL import ImageChops
from PIL import ImageOps

def do_it (photo1,photo2,output,cutoff=100,ax=0,ay=0,bx=0,by=0): # cutoff 0 -- 255
    ph1 = Image.open(photo1)
    ph2 = Image.open(photo2)

    ## make sure they're the same size
    aw,ah = ph1.size
    bw,bh = ph2.size
    w = min(aw,bw)
    h = min(ah,bh)
    ph1 = ph1.crop((ax,ay,w + ax,h + ay))
    ph2 = ph2.crop((bx,by,w + bx,h + by))

    blur1 = ph1.filter(ImageFilter.BLUR)
    blur2 = ph2.filter(ImageFilter.BLUR)
    
    alphachannel0 = ImageChops.difference(blur1,blur2)
    alphachannel1 = ImageOps.grayscale(alphachannel0)
    alphachannel2 = Image.eval(alphachannel1,lambda px:0 if px < cutoff else 255)
    alphachannel3 = alphachannel2.filter(ImageFilter.BLUR)
    alphachannel3.convert('1')
    alphachannel3.save("/tmp/alphachannel.png",format='png')
    
    ph1.paste(ph2,None,alphachannel3)
    ph1.save(output,format='png')
