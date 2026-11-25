import base64,io
from PIL import Image
U='/mnt/user-data/uploads/'
def uri(b,m):return f'data:{m};base64,'+base64.b64encode(b).decode()
def img(f,w,fmt='JPEG',crop=False):
    im=Image.open(U+f)
    if crop:
        bg=Image.new('RGBA',im.size,(255,255,255,255));bg.alpha_composite(im.convert('RGBA'))
        g=bg.convert('L').point(lambda p:255 if p<245 else 0);bb=g.getbbox();pad=12
        im=im.crop((max(bb[0]-pad,0),max(bb[1]-pad,0),min(bb[2]+pad,im.width),min(bb[3]+pad,im.height)))
    im.thumbnail((w,w*2));o=io.BytesIO()
    if fmt=='JPEG':im.convert('RGB').save(o,'JPEG',quality=86)
    else:im.save(o,'PNG',optimize=True)
    return uri(o.getvalue(),'image/'+fmt.lower())
logo=img('HEAT-Recovery-Logo.png',700,'PNG',True)
fav=Image.open(U+'HEAT-Recovery-Logo.png')
t=open('tpl.html').read()
for k,v in {'LOGO':logo,'FAV':logo,'GIO':img('Giovanni-Emad.png',800),'MOH':img('Mohamed-Mohamed.jpg',800),'STEM':img('STEM-School-Logo.png',400,'PNG'),
 'MOE':uri(open(U+'Ministry-of-Education-Logo.svg','rb').read(),'image/svg+xml'),'ISEF':uri(open(U+'ISEF-Logo.svg','rb').read(),'image/svg+xml')}.items():t=t.replace('{{'+k+'}}',v)
open('/mnt/user-data/outputs/heat-recovery.html','w').write(t);print(len(t)/1e6,'MB')
