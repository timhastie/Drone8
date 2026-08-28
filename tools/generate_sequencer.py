import re
p = open('pdtest/base.pd').read()

base_geo = [
 ("#X coords 0 -1 1 1 695 702 2 -1 0;", "#X coords 0 -1 1 1 695 760 2 -1 0;"),
 ("#X obj 581 0 cnv 0 114 702 empty empty empty 20 12 0 14 -58255 -58255 0;",
  "#X obj 581 0 cnv 0 114 760 empty empty empty 20 12 0 14 -58255 -58255 0;"),
 ("#X obj 0 26 cnv 19 580 675 empty empty empty 20 12 0 14 -199852",
  "#X obj 0 26 cnv 19 580 734 empty empty empty 20 12 0 14 -199852"),
 ("#X obj 378 216 hsl 56 10 0 127 0 0 \\$0-s-vib-speed \\$0-r-vib-speed SPEED 0 -7 0 10 -262144 -1 -1 0 1;",
  "#X obj 446 236 hsl 86 12 0 127 0 0 \\$0-s-vib-speed \\$0-r-vib-speed SPEED 0 -9 0 10 -262144 -1 -1 0 1;"),
 ("#X obj 366 216 hsl 56 10 0 127 0 0 \\$0-s-vib-speed \\$0-r-vib-speed SPEED 0 -7 0 10 -262144 -1 -1 0 1;",
  "#X obj 446 236 hsl 86 12 0 127 0 0 \\$0-s-vib-speed \\$0-r-vib-speed SPEED 0 -9 0 10 -262144 -1 -1 0 1;"),
 ("#X obj 430 215 tgl 12 0 \\$0-s-vib-sync \\$0-r-vib-sync SYNC -6 -7 0 10 -262144 -1 -1 0 1;",
  "#X obj 400 234 tgl 15 0 \\$0-s-vib-sync \\$0-r-vib-sync SYNC -2 -8 0 10 -262144 -1 -1 0 1;"),
 ("#X symbolatom 366 234 5 0 0 0 - \\$0-vib-div empty;",
  "#X symbolatom 540 234 4 0 0 0 - \\$0-vib-div empty;"),
 ("#X obj 583 658 cnv 0 106 24 empty empty INIT_PATCH 17 12 0 11 -20806 -262144 0;",
  "#X obj 583 658 cnv 0 106 24 empty \\$0-r-mh-inp INIT_PATCH 17 12 0 11 -20806 -262144 0;"),
 ("#X obj 626 683 bng 16 250 50 0 lira8init empty empty 0 0 0 10 -216373 -1 -1;",
  "#X obj 626 683 bng 16 250 50 0 lira8init \\$0-r-mh-inb empty 0 0 0 10 -216373 -1 -1;"),
]
for old_,new_ in base_geo:
    if p.count(old_)==1:
        p=p.replace(old_,new_)
assert p.count("695 760")==1, "canvas height edit failed"

deco_edits = [
 ("#X connect 210 0 208 0;", ""),
 ("#X obj 25 187 cnv 19 105 20 empty empty HYPER-LFO",   "#X obj 25 187 cnv 19 105 20 empty \\$0-r-mh-hyp HYPER-LFO"),
 ("#X obj 240 187 cnv 19 115 20 empty empty MOD-DELAY",  "#X obj 240 187 cnv 19 115 20 empty \\$0-r-mh-md MOD-DELAY"),
 ("#X obj 450 187 cnv 19 110 20 empty empty DISTORTION", "#X obj 450 187 cnv 19 110 20 empty \\$0-r-mh-di DISTORTION"),
 ("#X obj 470 226 cnv 15 15 15 empty empty ORGANISMIC",  "#X obj -60 -80 cnv 15 15 15 empty empty empty"),
 ("#X obj 466 240 cnv 15 15 15 empty empty SYNTHESIZER", "#X obj -60 -60 cnv 15 15 15 empty empty empty"),
 ("#X obj 583 80 cnv 0 106 24 empty empty RANDOMIZE",    "#X obj 583 80 cnv 0 106 24 empty \\$0-r-mh-rnd RANDOMIZE"),
 ("#X obj 583 130 cnv 0 106 24 empty empty SCALE",       "#X obj 583 130 cnv 0 106 24 empty \\$0-r-mh-scl SCALE"),
 ("#X obj 583 613 cnv 0 51 24 empty empty CLEAR",        "#X obj 583 613 cnv 0 51 24 empty \\$0-r-mh-clr CLEAR"),
 ("#X obj 636 613 cnv 0 54 24 empty empty SEL_ALL",      "#X obj 636 613 cnv 0 54 24 empty \\$0-r-mh-sel SEL_ALL"),
 ("#X obj 0 0 cnv 24 580 24 empty empty LYRA", "#X obj 0 0 cnv 24 580 24 empty \\$0-r-mh-top LYRA"),
 ("#X obj 583 0 cnv 0 106 24 empty empty LFO_SYNC", "#X obj 583 0 cnv 0 106 24 empty \\$0-r-mh-lfs LFO_SYNC"),
 ("#X obj 24 4 bng 16 250 50 0 lira8_prev_preset empty", "#X obj 24 4 bng 16 250 50 0 lira8_prev_preset \\$0-r-mh-pv"),
 ("#X obj 148 4 bng 16 250 50 0 lira8_next_preset empty", "#X obj 148 4 bng 16 250 50 0 lira8_next_preset \\$0-r-mh-nx"),
 ("#X obj 403 4 bng 16 250 50 0 lira8_save_preset empty", "#X obj 403 4 bng 16 250 50 0 lira8_save_preset \\$0-r-mh-sv"),
 ("#X obj 484 4 bng 16 250 50 0 lira8_saveas_preset empty", "#X obj 484 4 bng 16 250 50 0 lira8_saveas_preset \\$0-r-mh-sa"),
 ("#X obj 558 4 bng 16 250 50 0 lira8_load_preset empty", "#X obj 558 4 bng 16 250 50 0 lira8_load_preset \\$0-r-mh-ld"),
 ("#X obj 583 80 cnv 0 16 16 empty empty empty",         "#X obj 583 80 cnv 0 16 16 empty \\$0-r-mh-rm empty"),
 ("#X obj 35 648 cnv 19 28 46 empty empty 1 10 12 0 14 -1 -262144", "#X obj 35 648 cnv 19 28 46 empty \\$0-r-mh-sn1 1 10 12 0 14 -1 -262144"),
 ("#X obj 99 648 cnv 19 28 46 empty empty 2 10 12 0 14 -1 -262144", "#X obj 99 648 cnv 19 28 46 empty \\$0-r-mh-sn2 2 10 12 0 14 -1 -262144"),
 ("#X obj 175 648 cnv 19 28 46 empty empty 3 10 12 0 14 -1 -262144", "#X obj 175 648 cnv 19 28 46 empty \\$0-r-mh-sn3 3 10 12 0 14 -1 -262144"),
 ("#X obj 239 648 cnv 19 28 46 empty empty 4 10 12 0 14 -1 -262144", "#X obj 239 648 cnv 19 28 46 empty \\$0-r-mh-sn4 4 10 12 0 14 -1 -262144"),
 ("#X obj 315 648 cnv 19 28 46 empty empty 5 10 12 0 14 -1 -262144", "#X obj 315 648 cnv 19 28 46 empty \\$0-r-mh-sn5 5 10 12 0 14 -1 -262144"),
 ("#X obj 379 648 cnv 19 28 46 empty empty 6 10 12 0 14 -1 -262144", "#X obj 379 648 cnv 19 28 46 empty \\$0-r-mh-sn6 6 10 12 0 14 -1 -262144"),
 ("#X obj 455 648 cnv 19 28 46 empty empty 7 10 12 0 14 -1 -262144", "#X obj 455 648 cnv 19 28 46 empty \\$0-r-mh-sn7 7 10 12 0 14 -1 -262144"),
 ("#X obj 519 648 cnv 19 28 46 empty empty 8 10 12 0 14 -1 -262144", "#X obj 519 648 cnv 19 28 46 empty \\$0-r-mh-sn8 8 10 12 0 14 -1 -262144"),
 ("#X obj 627 106 bng 18 250 50 0 lira8rand lira8rand",  "#X obj 627 106 bng 18 250 50 0 lira8rand \\$0-r-mh-rndb"),
 ("#X obj 599 638 bng 18 250 50 0 lira8clear empty",     "#X obj 599 638 bng 18 250 50 0 lira8clear \\$0-r-mh-clrb"),
 ("#X obj 653 638 bng 18 250 50 0 lira8selall empty",    "#X obj 653 638 bng 18 250 50 0 lira8selall \\$0-r-mh-selb"),
]
for old,new in deco_edits:
    assert p.count(old)==1, old
    p=p.replace(old,new)

import re as _re
def _shift(mm):
    x,y=int(mm.group(2)),int(mm.group(3))
    if x<581 and 255<=y<=745 and 'vib-' not in mm.group(4):
        return "#X %s %d %d %s" % (mm.group(1),x,y+50,mm.group(4))
    return mm.group(0)
p=_re.sub(r'^#X (obj|text|floatatom|symbolatom) (-?\d+) (-?\d+) (.*)$', _shift, p, flags=_re.M)

# ---- piecewise vertical re-flow: spread the 50px across all rows ----
_MAIN_ANCHORS=[(255,255),(311,280),(354,326),(398,378),(438,426),(478,472),(523,520),(669,668),(698,692),(741,735),(760,754)]
def _fmain(y):
    a=_MAIN_ANCHORS
    if y<=a[0][0]: return y
    if y>=a[-1][0]: return y+(a[-1][1]-a[-1][0])
    for i in range(len(a)-1):
        (x0,y0),(x1,y1)=a[i],a[i+1]
        if x0<=y<=x1:
            return int(round(y0+(y-x0)*(y1-y0)/(x1-x0)))
    return y
_SIDE_BANDS=[(612,637,22),(638,657,27),(658,682,37),(683,699,41)]
def _fside(y):
    for lo,hi,d in _SIDE_BANDS:
        if lo<=y<=hi: return y+d
    return y
def _reflow(line):
    mm=_re.match(r'#X (obj|text|floatatom|symbolatom) (-?\d+) (-?\d+) (.*)$',line)
    if not mm: return line
    kind,x,y,rest=mm.group(1),int(mm.group(2)),int(mm.group(3)),mm.group(4)
    if 'vib-' in rest: return line
    if x<581:
        if not (255<=y<=760): return line
        ny=_fmain(y)
        cm=_re.match(r'(obj)?',kind) # noop
        cnv=_re.match(r'cnv (\d+) (\d+) (\d+) (.*)$',rest)
        if cnv and int(cnv.group(3))>=60:
            h=int(cnv.group(3)); nh=_fmain(y+h)-ny
            rest="cnv %s %s %d %s"%(cnv.group(1),cnv.group(2),nh,cnv.group(4))
        return "#X %s %d %d %s"%(kind,x,ny,rest)
    else:
        if not (612<=y<=699): return line
        return "#X %s %d %d %s"%(kind,x,_fside(y),rest)
p="\n".join(_reflow(l) for l in p.split("\n"))

# ---- horizontal re-flow: widen main panel 580->784, insert filter columns ----
_XA=[(0,0),(10,14),(41,66),(101,151),(177,252),(237,337),(313,438),(373,523),(449,624),(509,709),(537,741),(580,784)]
def _fx(x):
    if x<0: return x
    a=_XA
    if x>=a[-1][0]: return x+(a[-1][1]-a[-1][0])
    for i in range(len(a)-1):
        (x0,y0),(x1,y1)=a[i],a[i+1]
        if x0<=x<=x1:
            return int(round(y0+(x-x0)*(y1-y0)/(x1-x0)))
    return x
def _xflow(line):
    mm=_re.match(r'#X (obj|text|floatatom|symbolatom) (-?\d+) (-?\d+) (.*)$',line)
    if not mm: return line
    kind,x,y,rest=mm.group(1),int(mm.group(2)),int(mm.group(3)),mm.group(4)
    if x<0: return line
    if rest.startswith('cnv 1 ') and 4<=y<=19:
        for bx in (403,484,558):
            if bx<=x<=bx+16:
                return "#X %s %d %d %s"%(kind,_fx(bx)+(x-bx),y,rest)
    if y==4 and rest.startswith('bng 16 250 50 0 lira8_next_preset'):
        return "#X %s %d %d %s"%(kind,180,y,rest)
    if y==714 and rest.startswith('tgl 18 '):
        for bx in (35,99,175,239,315,379,455,519):
            if x==bx+5:
                return "#X %s %d %d %s"%(kind,_fx(bx)+5,y,rest)
    if y==697 and rest.startswith('vsl 9 38 '):
        for bx in (10,74,150,214,290,354,430,494):
            if x==bx+12:
                return "#X %s %d %d %s"%(kind,_fx(bx)+12,y,rest)
    if x>=581:
        return "#X %s %d %d %s"%(kind,x+204,y,rest)
    nx=_fx(x)
    cnv=_re.match(r'cnv (\d+) (\d+) (\d+) (.*)$',rest)
    if cnv and int(cnv.group(2))>=40:
        w=int(cnv.group(2)); nw=_fx(x+w)-nx
        rest="cnv %s %d %s %s"%(cnv.group(1),nw,cnv.group(3),cnv.group(4))
    hsl=_re.match(r'hsl (\d+) (\d+) (.*)$',rest)
    if hsl and int(hsl.group(1))>=60:
        w=int(hsl.group(1)); nw=_fx(x+w)-nx
        rest="hsl %d %s %s"%(nw,hsl.group(2),hsl.group(3))
    return "#X %s %d %d %s"%(kind,nx,y,rest)
p="\n".join(_xflow(l) for l in p.split("\n"))
_tl=[l for l in p.split("\n") if "mh-top" in l][0]
_parts=_tl.split()
_li=_parts.index("13")-2   # label token sits two before the '13' font-size token pair? locate via receive
_ri=[i for i,t in enumerate(_parts) if t.endswith("mh-top")][0]
_parts[_ri+1]="LIRA-8_V2"
_parts[_ri+2]="334"
p=p.replace(_tl," ".join(_parts))
p=p.replace("#X coords 0 -1 1 1 695 760 2 -1 0;","#X coords 0 -1 1 1 900 760 2 -1 0;")

# ---- inject 16 filter mini-sliders left of each tune column ----
_flt=[]
for _v,_tx in enumerate([66,151,252,337,438,523,624,709],1):
    _flt.append("#X obj %d 520 vsl 9 38 0 127 0 0 \\$0-s-cut-%d \\$0-r-cut-%d empty 0 -9 0 10 -262144 -1 -1 0 1;"%(_tx-27,_v,_v))
    _flt.append("#X obj %d 520 vsl 9 38 0 127 0 0 \\$0-s-res-%d \\$0-r-res-%d empty 0 -9 0 10 -262144 -1 -1 0 1;"%(_tx-15,_v,_v))
p=p.replace("#X coords 0 -1 1 1 900 760 2 -1 0;","\n".join(_flt)+"\n#X coords 0 -1 1 1 900 760 2 -1 0;")

# ---- inject 8 per-voice main-out isolation toggles under the sensors ----
_iso=[]
for _v,_ix in enumerate([63,155,256,347,448,538,639,727],1):
    _iso.append("#X obj %d 740 tgl 15 0 \\$0-s-iso-%d \\$0-r-iso-%d empty 0 0 0 10 -262144 -1 -1 0 1;"%(_ix,_v,_v))
p=p.replace("#X coords 0 -1 1 1 900 760 2 -1 0;","\n".join(_iso)+"\n#X coords 0 -1 1 1 900 760 2 -1 0;")

# ---- front-panel RANDOMIZE ALL! and INIT ALL circle buttons ----
_oldb="#X obj 787 80 cnv 0 106 24 empty \\$0-r-mh-rnd RANDOMIZE 17 12 0 11 -20806 -262144 0;"
assert p.count(_oldb)==1
p=p.replace(_oldb,"#X obj 787 80 cnv 0 66 24 empty \\$0-r-mh-rnd RANDOMIZE 2 12 0 11 -20806 -262144 0;")
_oldb="#X obj 787 695 cnv 0 106 24 empty \\$0-r-mh-inp INIT_PATCH 17 12 0 11 -20806 -262144 0;"
assert p.count(_oldb)==1
p=p.replace(_oldb,"#X obj 787 695 cnv 0 76 24 empty \\$0-r-mh-inp INIT_PATCH 2 12 0 11 -20806 -262144 0;")
_M18=((0,0,18,1),(0,1,5,1),(13,1,5,1),(0,2,4,1),(14,2,4,1),(0,3,3,1),(15,3,3,1),(0,4,2,1),(16,4,2,1),(0,5,1,8),(17,5,1,8),(0,13,2,1),(16,13,2,1),(0,14,3,1),(15,14,3,1),(0,15,4,1),(14,15,4,1),(0,16,5,1),(13,16,5,1),(0,17,18,1))
_M16=((0,0,16,1),(0,1,4,1),(12,1,4,1),(0,2,3,1),(13,2,3,1),(0,3,2,1),(14,3,2,1),(0,4,1,8),(15,4,1,8),(0,12,2,1),(14,12,2,1),(0,13,3,1),(13,13,3,1),(0,14,4,1),(12,14,4,1),(0,15,16,1))
def _move(rec,ox,oy,nx,ny):
    global p
    _o=rec%(ox,oy)
    assert p.count(_o)==1,_o
    p=p.replace(_o,rec%(nx,ny))
def _movemasks(offs,ox,oy,nx,ny,col):
    for _dx,_dy,_w,_h in offs:
        _move("#X obj %d %d cnv 1 "+str(_w)+" "+str(_h)+" empty empty empty 0 0 0 7 "+col+" 0;",ox+_dx,oy+_dy,nx+_dx,ny+_dy)
_move("#X obj %d %d bng 18 250 50 0 lira8rand \\$0-r-mh-rndb empty 0 0 0 10 -216373 -1 -1;",831,106,811,106)
_movemasks(_M18,831,106,811,106,"-58255 -58255")
_move("#X obj %d %d bng 16 250 50 0 lira8init \\$0-r-mh-inb empty 0 0 0 10 -216373 -1 -1;",830,724,817,724)
_movemasks(_M16,830,724,817,724,"-58255 -58255")
_move("#X obj %d %d bng 16 250 50 0 lira8_save_preset \\$0-r-mh-sv SAVE -34 7 0 11 -216373 -1 -262144;",563,4,590,4)
_movemasks(_M16,563,4,590,4,"-1 -1")
_move("#X obj %d %d bng 16 250 50 0 lira8_saveas_preset \\$0-r-mh-sa SAVE_AS -52 7 0 11 -216373 -1 -262144;",674,4,685,4)
_movemasks(_M16,674,4,685,4,"-1 -1")
_fb=["#X obj 855 80 cnv 0 39 24 empty \\$0-r-mh-rn2 ALL! 6 12 0 11 -20806 -262144 0;",
     "#X obj 865 695 cnv 0 29 24 empty \\$0-r-mh-in2 ALL 4 12 0 11 -20806 -262144 0;",
     "#X obj 866 106 bng 18 250 50 0 \\$0-s-sq-fral \\$0-r-mh-ranb empty 0 0 0 10 -216373 -1 -1;"]
for _dx,_dy,_w,_h in _M18:
    _fb.append("#X obj %d %d cnv 1 %d %d empty empty empty 0 0 0 7 -58255 -58255 0;"%(866+_dx,106+_dy,_w,_h))
_fb.append("#X obj 871 724 bng 16 250 50 0 \\$0-s-sq-fial \\$0-r-mh-inab empty 0 0 0 10 -216373 -1 -1;")
for _dx,_dy,_w,_h in _M16:
    _fb.append("#X obj %d %d cnv 1 %d %d empty empty empty 0 0 0 7 -58255 -58255 0;"%(871+_dx,724+_dy,_w,_h))
p=p.replace("#X coords 0 -1 1 1 900 760 2 -1 0;","\n".join(_fb)+"\n#X coords 0 -1 1 1 900 760 2 -1 0;")

# ---- NEW PATCH button in the top bar (left of SAVE) ----
_np=["#X obj 513 4 bng 16 250 50 0 lira8_new_preset \\$0-r-mh-nw NEW -28 7 0 11 -216373 -1 -262144;"]
for _dx,_dy,_w,_h in _M16:
    _np.append("#X obj %d %d cnv 1 %d %d empty empty empty 0 0 0 7 -1 -1 0;"%(513+_dx,4+_dy,_w,_h))
p=p.replace("#X coords 0 -1 1 1 900 760 2 -1 0;","\n".join(_np)+"\n#X coords 0 -1 1 1 900 760 2 -1 0;")

# ---- gui.link bindings for params 88..103 ----
_gl=""
for _v in range(1,9): _gl+="#X obj 642 %d gui.link %d \\$0 cut-%d;\n"%(512+_v*20,87+_v,_v)
for _v in range(1,9): _gl+="#X obj 742 %d gui.link %d \\$0 res-%d;\n"%(512+_v*20,95+_v,_v)
for _v in range(1,9): _gl+="#X obj 842 %d gui.link %d \\$0 iso-%d;\n"%(512+_v*20,103+_v,_v)
_ga="#X restore -1 746 pd gui.link;"
assert p.count(_ga)==1
p=p.replace(_ga,_gl+_ga)

mains=[]; seen=set()
for m in re.finditer(r'#X obj (-?\d+) (-?\d+) (vsl|hsl|tgl|bng|hradio|vradio|cnv) .*?\\\$0-r-([a-z0-9-]+)', p):
    x,y,suf=int(m.group(1)),int(m.group(2)),'r-'+m.group(4)
    if suf in seen: continue
    if 0<=x<=900 and 0<=y<=760: mains.append((suf,x,y)); seen.add(suf)

HIDE=1500
chrome=[]; page1=[]; page2=[]; widgets=[]
OVX=100
IDX={}
MASKB=[]
def W(group,rec,x,y,suf):
    x=x+OVX
    widgets.append(rec.format(x=x,y=y+HIDE)); group.append((suf,x,y)); IDX[suf]=len(widgets)-1
    if " bng 14 " in rec or " bng 16 " in rec:
        if suf!="r-sq-close":
            MASKB.append((group,x,y,16 if " bng 16 " in rec else 14))
def emit_masks():
    for k,(grp,bx,by,N) in enumerate(MASKB):
        cg=(4,3,2) if N==16 else (3,2,1)
        sl=[(0,0,N,1),(0,N-1,N,1)]
        for t,cv in enumerate(cg):
            sl += [(0,t+1,cv,1),(N-cv,t+1,cv,1),(0,N-2-t,cv,1),(N-cv,N-2-t,cv,1)]
        sl += [(0,4,1,N-8),(N-1,4,1,N-8)]
        for i,(dx,dy,w,h) in enumerate(sl):
            suf="r-sq-msk-%d-%d"%(k,i)
            widgets.append("#X obj %d %d cnv 1 %d %d empty \\$0-%s empty 0 0 0 7 -58255 -58255 0;"%(bx+dx,by+dy+HIDE,w,h,suf))
            grp.append((suf,bx+dx,by+dy)); IDX[suf]=len(widgets)-1

# chrome (both pages)
W(chrome,"#X obj {x} {y} cnv 0 900 760 empty \\$0-r-sq-brd empty 20 12 0 14 -1 -1 0;",-100,0,"r-sq-brd")
W(chrome,"#X obj {x} {y} cnv 0 892 752 empty \\$0-r-sq-bg empty 20 12 0 14 -58255 -58255 0;",-96,4,"r-sq-bg")
W(chrome,"#X obj {x} {y} cnv 0 892 24 empty \\$0-r-sq-tt SEQUENCER 400 12 0 13 -20806 -262144 0;",-96,4,"r-sq-tt")
W(chrome,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-close \\$0-r-sq-close X 5 9 0 12 -20806 -20806 -262144;",772,8,"r-sq-close")
W(chrome,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-arna \\$0-r-sq-srna RND_ALL! -72 8 0 10 -216373 -1 -262144;",630,52,"r-sq-srna")
W(chrome,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-aini \\$0-r-sq-sini INIT_ALL! -80 8 0 10 -216373 -1 -262144;",766,52,"r-sq-sini")
W(chrome,"#X obj {x} {y} hsl 120 18 0 127 0 0 \\$0-s-sq-pgt \\$0-r-sq-pgtb empty 0 -9 0 10 -20806 -20806 -20806 0 1;",55,87,"r-sq-pgtb")
W(chrome,"#X obj {x} {y} cnv 0 120 18 empty \\$0-r-sq-tr TRIGGER 34 9 0 11 -20806 -262144 0;",55,87,"r-sq-tr")
W(chrome,"#X obj {x} {y} hsl 120 18 0 127 0 0 \\$0-s-sq-pgp \\$0-r-sq-pgpb empty 0 -9 0 10 -20806 -20806 -20806 0 1;",185,87,"r-sq-pgpb")
W(chrome,"#X obj {x} {y} cnv 0 120 18 empty \\$0-r-sq-pr PITCH 40 9 0 11 -20806 -262144 0;",185,87,"r-sq-pr")
W(chrome,"#X obj {x} {y} hsl 120 18 0 127 0 0 \\$0-s-sq-pgf \\$0-r-sq-pgfb empty 0 -9 0 10 -20806 -20806 -20806 0 1;",315,87,"r-sq-pgfb")
W(chrome,"#X obj {x} {y} cnv 0 120 18 empty \\$0-r-sq-fr FILTER 36 9 0 11 -20806 -262144 0;",315,87,"r-sq-fr")
W(chrome,"#X obj {x} {y} hsl 120 18 0 127 0 0 \\$0-s-sq-pgm \\$0-r-sq-pgmb empty 0 -9 0 10 -20806 -20806 -20806 0 1;",445,87,"r-sq-pgmb")
W(chrome,"#X obj {x} {y} cnv 0 120 18 empty \\$0-r-sq-mr MOD 46 9 0 11 -20806 -262144 0;",445,87,"r-sq-mr")
W(chrome,"#X obj {x} {y} hsl 120 18 0 127 0 0 \\$0-s-sq-pgm2 \\$0-r-sq-pgm2b empty 0 -9 0 10 -20806 -20806 -20806 0 1;",575,87,"r-sq-pgm2b")
W(chrome,"#X obj {x} {y} cnv 0 120 18 empty \\$0-r-sq-m2r MOD2 40 9 0 11 -20806 -262144 0;",575,87,"r-sq-m2r")
# page1: headers + rows (halo UNDER toggles)
for i,lab in enumerate(("A","D","S","R")):
    W(page1,"#X obj {x} {y} cnv 1 1 1 empty \\$0-r-sq-h%d %s 2 0 0 10 -58255 -262144 0;"%(i,lab),470+i*18,116,"r-sq-h%d"%i)
W(page1,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-trna \\$0-r-sq-trna RND_ALL_TRIGGER -111 9 0 10 -216373 -1 -4034;",672,710,"r-sq-trna")
W(page1,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-tcla \\$0-r-sq-tcla CLR_ALL_TRIGGER -111 9 0 10 -216373 -1 -4034;",827,710,"r-sq-tcla")
W(page1,"#X obj {x} {y} tgl 15 0 \\$0-s-sq-menv \\$0-r-sq-menv MIDI_ENV 19 8 0 10 -262144 -1 -262144 0 1;",788,89,"r-sq-menv")
row_y=lambda v:120+(v-1)*74
for v in range(1,9):
    y0=row_y(v)
    W(page1,"#X obj {x} {y} cnv 1 1 1 empty \\$0-r-sq-rl-%d %d 0 8 0 12 -58255 -262144 0;"%(v,v),60,y0+12,"r-sq-rl-%d"%v)
    for s in range(16):
        idx=(v-1)*16+s
        W(page1,"#X obj {x} {y} tgl 22 0 empty \\$0-r-sq-fl-%d empty 17 7 0 10 -58255 -4034 -1 0 1;"%idx,
          97+s*22,y0+9,"r-sq-fl-%d"%idx)
    for s in range(16):
        idx=(v-1)*16+s
        W(page1,"#X obj {x} {y} tgl 16 0 \\$0-s-sq-t-%d \\$0-r-sq-t-%d empty 17 7 0 10 -262144 -1 -1 0 1;"%(idx,idx),
          100+s*22,y0+12,"r-sq-t-%d"%idx)
    ADSRY=y0+12
    for i,pn in enumerate(("a","d","su","re")):
        W(page1,"#X obj {x} {y} vsl 12 44 0 127 0 0 \\$0-s-sq-%s-%d \\$0-r-sq-%s-%d empty 0 -9 0 10 -262144 -1 -1 0 1;"%(pn,v,pn,v),
          470+i*18,ADSRY,"r-sq-%s-%d"%(pn,v))
    W(page1,"#X obj {x} {y} tgl 15 0 \\$0-s-sq-m-%d \\$0-r-sq-m-%d OFF 18 8 0 10 -262144 -1 -262144 0 1;"%(v,v),
      560,y0+12,"r-sq-m-%d"%v)
    W(page1,"#X obj {x} {y} hsl 34 10 0 127 0 0 \\$0-s-sq-rt-%d \\$0-r-sq-rt-%d x1 10 18 0 9 -262144 -1 -262144 0 1;"%(v,v),
      618,y0+15,"r-sq-rt-%d"%v)
    W(page1,"#X obj {x} {y} bng 14 250 50 0 \\$0-s-sq-trn-%d \\$0-r-sq-trn-%d RND 17 8 0 10 -216373 -1 -262144;"%(v,v),
      690,y0+12,"r-sq-trn-%d"%v)
    W(page1,"#X obj {x} {y} bng 14 250 50 0 \\$0-s-sq-tcl-%d \\$0-r-sq-tcl-%d CLR 17 8 0 10 -216373 -1 -262144;"%(v,v),
      745,y0+12,"r-sq-tcl-%d"%v)
# page2: pitch rows
for v in range(1,9):
    y0=row_y(v)
    W(page2,"#X obj {x} {y} cnv 1 1 1 empty \\$0-r-sq-prl-%d %d 0 8 0 12 -58255 -262144 0;"%(v,v),60,y0+26,"r-sq-prl-%d"%v)
    for s in range(16):
        idx=(v-1)*16+s
        W(page2,"#X obj {x} {y} vsl 16 40 0 127 0 0 \\$0-s-sq-p-%d \\$0-r-sq-p-%d empty 1 -5 0 9 -262144 -1 -262144 0 1;"%(idx,idx),
          100+s*22,y0+10,"r-sq-p-%d"%idx)
    for s in range(16):
        idx=(v-1)*16+s
        W(page2,"#X obj {x} {y} tgl 12 0 empty \\$0-r-sq-pfl-%d empty 17 7 0 10 -58255 -4034 -1 0 1;"%idx,
          102+s*22,y0+54,"r-sq-pfl-%d"%idx)
    W(page2,"#X obj {x} {y} tgl 15 0 \\$0-s-sq-pe-%d \\$0-r-sq-pe-%d ON 18 8 0 10 -262144 -1 -262144 0 1;"%(v,v),
      460,y0+22,"r-sq-pe-%d"%v)
    W(page2,"#X obj {x} {y} bng 14 250 50 0 \\$0-s-sq-rn-%d \\$0-r-sq-rn-%d RND 17 8 0 10 -216373 -1 -262144;"%(v,v),
      505,y0+22,"r-sq-rn-%d"%v)
    W(page2,"#X obj {x} {y} bng 14 250 50 0 \\$0-s-sq-cl-%d \\$0-r-sq-cl-%d CLR 17 8 0 10 -216373 -1 -262144;"%(v,v),
      550,y0+22,"r-sq-cl-%d"%v)
    W(page2,"#X obj {x} {y} hsl 34 10 0 127 0 0 \\$0-s-sq-rp-%d \\$0-r-sq-rp-%d x1 10 18 0 9 -262144 -1 -262144 0 1;"%(v,v),
      615,y0+25,"r-sq-rp-%d"%v)
W(page2,"#X obj {x} {y} tgl 15 0 \\$0-s-sq-q \\$0-r-sq-q QUANTIZE 19 8 0 10 -262144 -1 -262144 0 1;",720,89,"r-sq-q")
W(page2,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-rna \\$0-r-sq-rna RND_ALL_PITCH -97 9 0 10 -216373 -1 -4034;",604,710,"r-sq-rna")
W(page2,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-cla \\$0-r-sq-cla CLR_ALL_PITCH -97 9 0 10 -216373 -1 -4034;",759,710,"r-sq-cla")
page3=[]
W(page3,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-frna \\$0-r-sq-frna RND_ALL_FILTER -104 9 0 10 -216373 -1 -4034;",656,710,"r-sq-frna")
W(page3,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-fcla \\$0-r-sq-fcla CLR_ALL_FILTER -104 9 0 10 -216373 -1 -4034;",811,710,"r-sq-fcla")
for i,lab in enumerate(("A","D","S","R")):
    W(page3,"#X obj {x} {y} cnv 1 1 1 empty \\$0-r-sq-fh%d %s 2 0 0 10 -58255 -262144 0;"%(i,lab),470+i*18,116,"r-sq-fh%d"%i)
for v in range(1,9):
    y0=row_y(v)
    W(page3,"#X obj {x} {y} cnv 1 1 1 empty \\$0-r-sq-frl-%d %d 0 8 0 12 -58255 -262144 0;"%(v,v),60,y0+22,"r-sq-frl-%d"%v)
    for s in range(16):
        idx=(v-1)*16+s
        W(page3,"#X obj {x} {y} vsl 16 34 0 127 0 0 \\$0-s-sq-fc-%d \\$0-r-sq-fc-%d empty 1 -5 0 9 -262144 -1 -262144 0 1;"%(idx,idx),
          100+s*22,y0+6,"r-sq-fc-%d"%idx)
    for s in range(16):
        idx=(v-1)*16+s
        W(page3,"#X obj {x} {y} tgl 14 0 \\$0-s-sq-ft-%d \\$0-r-sq-ft-%d empty 17 7 0 10 -262144 -1 -1 0 1;"%(idx,idx),
          101+s*22,y0+44,"r-sq-ft-%d"%idx)
    for s in range(16):
        idx=(v-1)*16+s
        W(page3,"#X obj {x} {y} tgl 10 0 empty \\$0-r-sq-ffl-%d empty 17 7 0 10 -58255 -4034 -1 0 1;"%idx,
          103+s*22,y0+60,"r-sq-ffl-%d"%idx)
    ADSRY=y0+6
    for i,pn in enumerate(("fa","fd","fsu","fre")):
        W(page3,"#X obj {x} {y} vsl 12 44 0 127 0 0 \\$0-s-sq-%s-%d \\$0-r-sq-%s-%d empty 0 -9 0 10 -262144 -1 -1 0 1;"%(pn,v,pn,v),
          470+i*18,ADSRY,"r-sq-%s-%d"%(pn,v))
    W(page3,"#X obj {x} {y} tgl 15 0 \\$0-s-sq-fe-%d \\$0-r-sq-fe-%d ON 18 8 0 10 -262144 -1 -262144 0 1;"%(v,v),
      560,y0+22,"r-sq-fe-%d"%v)
    W(page3,"#X obj {x} {y} bng 14 250 50 0 \\$0-s-sq-frn-%d \\$0-r-sq-frn-%d RND 17 8 0 10 -216373 -1 -262144;"%(v,v),
      608,y0+22,"r-sq-frn-%d"%v)
    W(page3,"#X obj {x} {y} bng 14 250 50 0 \\$0-s-sq-fcl-%d \\$0-r-sq-fcl-%d CLR 17 8 0 10 -216373 -1 -262144;"%(v,v),
      662,y0+22,"r-sq-fcl-%d"%v)
    W(page3,"#X obj {x} {y} hsl 34 10 0 127 0 0 \\$0-s-sq-rf-%d \\$0-r-sq-rf-%d x1 10 18 0 9 -262144 -1 -262144 0 1;"%(v,v),
      722,y0+25,"r-sq-rf-%d"%v)
W(page3,"#X obj {x} {y} cnv 1 1 1 empty \\$0-r-sq-famth AMT 2 0 0 10 -58255 -262144 0;",537,116,"r-sq-famth")
for v in range(1,9):
    W(page3,"#X obj {x} {y} vsl 12 44 0 127 0 0 \\$0-s-sq-famt-%d \\$0-r-sq-famt-%d empty 0 -9 0 10 -262144 -1 -1 0 1;"%(v,v),
      540,row_y(v)+6,"r-sq-famt-%d"%v)
page4=[]
W(page4,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-mrna \\$0-r-sq-mrna RND_ALL_MOD -83 9 0 10 -216373 -1 -4034;",604,710,"r-sq-mrna")
W(page4,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-mcla \\$0-r-sq-mcla CLR_ALL_MOD -83 9 0 10 -216373 -1 -4034;",759,710,"r-sq-mcla")
_MROWS=("M12","M34","M56","M78","S12","S34","S56","S78")
for v in range(1,9):
    y0=row_y(v)
    W(page4,"#X obj {x} {y} cnv 1 1 1 empty \\$0-r-sq-mrl-%d %s 0 8 0 11 -58255 -262144 0;"%(v,_MROWS[v-1]),52,y0+22,"r-sq-mrl-%d"%v)
    for s in range(16):
        idx=(v-1)*16+s
        W(page4,"#X obj {x} {y} vsl 16 40 0 127 0 0 \\$0-s-sq-mv-%d \\$0-r-sq-mv-%d empty 1 -5 0 9 -262144 -1 -262144 0 1;"%(idx,idx),
          100+s*22,y0+10,"r-sq-mv-%d"%idx)
    for s in range(16):
        idx=(v-1)*16+s
        W(page4,"#X obj {x} {y} tgl 12 0 empty \\$0-r-sq-mfl-%d empty 17 7 0 10 -58255 -4034 -1 0 1;"%idx,
          102+s*22,y0+54,"r-sq-mfl-%d"%idx)
    W(page4,"#X obj {x} {y} tgl 15 0 \\$0-s-sq-me-%d \\$0-r-sq-me-%d ON 18 8 0 10 -262144 -1 -262144 0 1;"%(v,v),
      460,y0+22,"r-sq-me-%d"%v)
    W(page4,"#X obj {x} {y} bng 14 250 50 0 \\$0-s-sq-mrn-%d \\$0-r-sq-mrn-%d RND 17 8 0 10 -216373 -1 -262144;"%(v,v),
      505,y0+22,"r-sq-mrn-%d"%v)
    W(page4,"#X obj {x} {y} bng 14 250 50 0 \\$0-s-sq-mcl-%d \\$0-r-sq-mcl-%d CLR 17 8 0 10 -216373 -1 -262144;"%(v,v),
      550,y0+22,"r-sq-mcl-%d"%v)
    W(page4,"#X obj {x} {y} hsl 34 10 0 127 0 0 \\$0-s-sq-rm-%d \\$0-r-sq-rm-%d x1 10 18 0 9 -262144 -1 -262144 0 1;"%(v,v),
      615,y0+25,"r-sq-rm-%d"%v)
page5=[]
W(page5,"#X obj {x} {y} tgl 15 0 \\$0-s-sq-m2ls \\$0-r-sq-m2ls LFO_SYNC 19 8 0 10 -262144 -1 -262144 0 1;",680,row_y(3)+22,"r-sq-m2ls")
W(page5,"#X obj {x} {y} tgl 15 0 \\$0-s-sq-m2vs \\$0-r-sq-m2vs VIB_SYNC 19 8 0 10 -262144 -1 -262144 0 1;",680,row_y(8)+22,"r-sq-m2vs")
W(page5,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-m2rna \\$0-r-sq-m2rna RND_ALL_MOD2 -90 9 0 10 -216373 -1 -4034;",657,710,"r-sq-m2rna")
W(page5,"#X obj {x} {y} bng 16 250 50 0 \\$0-s-sq-m2cla \\$0-r-sq-m2cla CLR_ALL_MOD2 -90 9 0 10 -216373 -1 -4034;",812,710,"r-sq-m2cla")
_M2ROWS=("P12","P56","LFA","LFB","DL1","DL2","FBK","VIB")
for v in range(1,9):
    y0=row_y(v)
    W(page5,"#X obj {x} {y} cnv 1 1 1 empty \\$0-r-sq-m2rl-%d %s 0 8 0 11 -58255 -262144 0;"%(v,_M2ROWS[v-1]),52,y0+22,"r-sq-m2rl-%d"%v)
    for s in range(16):
        idx=(v-1)*16+s
        W(page5,"#X obj {x} {y} vsl 16 40 0 127 0 0 \\$0-s-sq-m2v-%d \\$0-r-sq-m2v-%d empty 1 -5 0 9 -262144 -1 -262144 0 1;"%(idx,idx),
          100+s*22,y0+10,"r-sq-m2v-%d"%idx)
    for s in range(16):
        idx=(v-1)*16+s
        W(page5,"#X obj {x} {y} tgl 12 0 empty \\$0-r-sq-m2fl-%d empty 17 7 0 10 -58255 -4034 -1 0 1;"%idx,
          102+s*22,y0+54,"r-sq-m2fl-%d"%idx)
    W(page5,"#X obj {x} {y} tgl 15 0 \\$0-s-sq-m2e-%d \\$0-r-sq-m2e-%d ON 18 8 0 10 -262144 -1 -262144 0 1;"%(v,v),
      460,y0+22,"r-sq-m2e-%d"%v)
    W(page5,"#X obj {x} {y} bng 14 250 50 0 \\$0-s-sq-m2rn-%d \\$0-r-sq-m2rn-%d RND 17 8 0 10 -216373 -1 -262144;"%(v,v),
      505,y0+22,"r-sq-m2rn-%d"%v)
    W(page5,"#X obj {x} {y} bng 14 250 50 0 \\$0-s-sq-m2cl-%d \\$0-r-sq-m2cl-%d CLR 17 8 0 10 -216373 -1 -262144;"%(v,v),
      550,y0+22,"r-sq-m2cl-%d"%v)
    W(page5,"#X obj {x} {y} hsl 34 10 0 127 0 0 \\$0-s-sq-rm2-%d \\$0-r-sq-rm2-%d x1 10 18 0 9 -262144 -1 -262144 0 1;"%(v,v),
      615,y0+25,"r-sq-rm2-%d"%v)
# --- per-lane shift arrows ---
_ARROWS=((page1,"tsl","tsr",78,453,14),(page2,"psl","psr",76,447,24),
         (page3,"fsl","fsr",72,452,26),(page4,"msl","msr",82,447,24),
         (page5,"m2sl","m2sr",81,447,24))
for _pg,_ls,_rs,_lx,_rx,_dy in _ARROWS:
    for v in range(1,9):
        y0=row_y(v)
        W(_pg,"#X obj {x} {y} bng 15 250 50 0 \\$0-s-sq-%s-%d \\$0-r-sq-%s-%d < 4 8 0 12 -58255 -58255 -262144;"%(_ls,v,_ls,v),
          _lx,y0+_dy,"r-sq-%s-%d"%(_ls,v))
        W(_pg,"#X obj {x} {y} bng 15 250 50 0 \\$0-s-sq-%s-%d \\$0-r-sq-%s-%d > 4 8 0 12 -58255 -58255 -262144;"%(_rs,v,_rs,v),
          _rx,y0+_dy,"r-sq-%s-%d"%(_rs,v))
emit_masks()
def shift_page(group,dx,dy=0):
    for gi,(suf,x,y) in enumerate(group):
        wi=IDX[suf]
        rec=widgets[wi]
        t=rec.split()
        t[2]=str(int(t[2])+dx)
        t[3]=str(int(t[3])+dy)
        widgets[wi]=" ".join(t)
        group[gi]=(suf,x+dx,y+dy)
shift_page(page1,-72,24)
shift_page(page2,-4,24)
shift_page(page3,-56,24)
shift_page(page4,-4,24)
shift_page(page5,-57,24)
# launcher (visible at home)
launcher=[
 ("#X obj {x} {y} cnv 19 100 20 empty \\$0-r-mh-seqb SEQUENCER 22 11 0 13 -1 -262144 0;",216,187,"r-mh-seqb"),
 ("#X obj {x} {y} bng 15 250 50 0 \\$0-s-sq-open \\$0-r-sq-open empty 17 7 0 10 -1 -1 -1;",220,190,"r-sq-open"),
 ("#X obj {x} {y} cnv 1 11 2 empty \\$0-r-mh-d1 empty 0 0 0 7 -262144 -262144 0;",222,192,"r-mh-d1"),
 ("#X obj {x} {y} cnv 1 11 2 empty \\$0-r-mh-d2 empty 0 0 0 7 -262144 -262144 0;",222,196,"r-mh-d2"),
 ("#X obj {x} {y} cnv 1 11 2 empty \\$0-r-mh-d3 empty 0 0 0 7 -262144 -262144 0;",222,200,"r-mh-d3"),
]
for rec,x,y,suf in launcher:
    widgets.append(rec.format(x=x,y=y)); mains.append((suf,x,y))

def T(s,x,y): return "%s %d %d"%(s,x,y)
def home(g): return [T(s,x,y) for s,x,y in g]
def away(g): return [T(s,x,y+HIDE) for s,x,y in g]
close_lines = home(mains)+away(chrome)+away(page1)+away(page2)+away(page3)+away(page4)+away(page5)
trig_lines  = away(mains)+home(chrome)+home(page1)+away(page2)+away(page3)+away(page4)+away(page5)
pit_lines   = away(mains)+home(chrome)+away(page1)+home(page2)+away(page3)+away(page4)+away(page5)
flt_lines   = away(mains)+home(chrome)+away(page1)+away(page2)+home(page3)+away(page4)+away(page5)
mod_lines   = away(mains)+home(chrome)+away(page1)+away(page2)+away(page3)+home(page4)+away(page5)
mod2_lines  = away(mains)+home(chrome)+away(page1)+away(page2)+away(page3)+away(page4)+home(page5)
N=len(close_lines)
assert len(trig_lines)==N==len(pit_lines)==len(flt_lines)==len(mod_lines)==len(mod2_lines)

objs=[];conns=[]
src=open('pd3.py').read().split("cvs=parse")[0]; ns={}; exec(src,ns)
open('tmp_count.pd','w').write(p); BASE=len(ns['parse']('tmp_count.pd')[0]['objs'])
def add(r): objs.append(r); return BASE+len(objs)-1
def c(a,ao,b,bo): conns.append((a,ao,b,bo))
widx0=BASE
for w in widgets: add(w)
def widx(group_offset): return widx0+group_offset

# widget index helpers
def wid(suf): return widx0+IDX[suf]

# --- 3-state dispatcher ---
tb_names=[("close",close_lines),("trig",trig_lines),("pit",pit_lines),("flt",flt_lines),("mod",mod_lines),("mod2",mod2_lines)]
t_objs={}
for nm,lines in tb_names:
    t_objs[nm]=add("#X obj 2100 800 text define -k \\$0-sqpos-%s;\n#A set "%nm+" \; ".join(lines)+";")
drivers=[("r \\$0-s-sq-close","close"),("r \\$0-s-sq-open","trig"),("r \\$0-s-sq-pgt","trig"),("r \\$0-s-sq-pgp","pit"),("r \\$0-s-sq-pgf","flt"),("r \\$0-s-sq-pgm","mod"),("r \\$0-s-sq-pgm2","mod2")]
sp={}; tg={}
cnt=add("#X obj 2200 1020 f;"); inc=add("#X obj 2260 1020 + 1;")
tff=add("#X obj 2200 1050 t f f;")
m0=add("#X msg 2200 960 0;")
tll=add("#X obj 2200 1140 t l l;")
up_a=add("#X obj 2260 1170 unpack s f f;")
up_b=add("#X obj 2200 1200 unpack s f f;")
mkfn=add("#X obj 2260 1230 makefilename \\$0-%s;")
pkxy=add("#X obj 2200 1230 pack f f;")
mpos=add("#X msg 2200 1260 pos \\$1 \\$2;")
sdyn=add("#X obj 2200 1290 s;")
srdw=add("#X obj 2450 930 s \\$0-redraw;")
c(m0,0,cnt,1); c(cnt,0,tff,0); c(tff,1,inc,0); c(inc,0,cnt,1)
c(tll,1,up_a,0); c(tll,0,up_b,0)
c(up_a,0,mkfn,0); c(mkfn,0,sdyn,1)
c(up_b,1,pkxy,0); c(up_b,2,pkxy,1); c(pkxy,0,mpos,0); c(mpos,0,sdyn,0)
for nm,_ in tb_names:
    sp[nm]=add("#X obj 2130 1065 spigot 0;")
    tg[nm]=add("#X obj 2130 1110 text get \\$0-sqpos-%s;"%nm)
    c(tff,0,sp[nm],0); c(sp[nm],0,tg[nm],0); c(tg[nm],0,tll,0)
TABS=("r-sq-tr","r-sq-pr","r-sq-fr","r-sq-mr","r-sq-m2r")
STATE_TAB={"trig":0,"pit":1,"flt":2,"mod":3,"mod2":4}
tabsends=[add("#X obj %d 3200 s \\$0-%s;"%(17800+i*90,t)) for i,t in enumerate(TABS)]
for drv,target in drivers:
    r=add("#X obj 2100 900 %s;"%drv)
    tb=add("#X obj 2100 930 t b b b b;")
    c(r,0,tb,0)
    if target in STATE_TAB:
        act=STATE_TAB[target]
        for i in range(5):
            col="-65285" if i==act else "-16777216"
            cm=add("#X msg %d %d color -1315861 -1315861 %s;"%(17800+i*90,3240+len(objs)%40,col))
            c(tb,3,cm,0); c(cm,0,tabsends[i],0)
    for nm,_ in tb_names:
        mg=add("#X msg 2060 960 %d;"%(1 if nm==target else 0))
        c(tb,3,mg,0); c(mg,0,sp[nm],1)
    c(tb,2,m0,0)
    mN=add("#X msg 2130 1000 %d;"%N); unt=add("#X obj 2130 1030 until;")
    c(tb,1,mN,0); c(mN,0,unt,0); c(unt,0,cnt,0)
    c(tb,0,srdw,0)

# --- clock: transport intake + shared rate processor + 24 per-row clocks ---
r_ph=add("#X obj 2100 1350 r playhead;")
rt=add("#X obj 2100 1380 route position playing;")
un=add("#X obj 2100 1410 unpack f;")
c(r_ph,0,rt,0); c(rt,0,un,0)
selstop=add("#X obj 2500 1410 sel 0;")
sstop=add("#X obj 2500 1440 s \\$0-sq-stopclr;")
c(rt,1,selstop,0); c(selstop,0,sstop,0)
RT_SUF=["rt-%d"%v for v in range(1,9)]+["rp-%d"%v for v in range(1,9)]+["rf-%d"%v for v in range(1,9)]+["rm-%d"%v for v in range(1,9)]+["rm2-%d"%v for v in range(1,9)]
add("#X obj 2100 4560 text define -k \\$0-sq-rtmap;\n#A set "+" \; ".join(RT_SUF)+";")
r_rtp=add("#X obj 2100 4600 r \\$0-sq-rtproc;")
upr=add("#X obj 2100 4630 unpack f f;")
fvr=add("#X obj 2200 4660 f;")
tur=add("#X obj 2100 4660 t f b f f;")
mkM=add("#X obj 2100 4690 makefilename \\$0-sq-mult-%d;")
sdM=add("#X obj 2100 4780 s;")
tgr=add("#X obj 2260 4690 text get \\$0-sq-rtmap;")
mkL=add("#X obj 2260 4720 makefilename \\$0-r-sq-%s;")
sdL=add("#X obj 2260 4780 s;")
d18=add("#X obj 2400 4690 / 18.15;")
i18=add("#X obj 2400 4720 i;")
cl6=add("#X obj 2400 4750 clip 0 6;")
rt7=add("#X obj 2400 4780 route 0 1 2 3 4 5 6;")
c(r_rtp,0,upr,0); c(upr,1,fvr,1); c(upr,0,tur,0)
c(tur,3,mkM,0); c(mkM,0,sdM,1)
c(tur,2,tgr,0); c(tgr,0,mkL,0); c(mkL,0,sdL,1)
c(tur,1,fvr,0); c(fvr,0,d18,0); c(d18,0,i18,0); c(i18,0,cl6,0); c(cl6,0,rt7,0)
c(tur,0,srdw,0)
_MULTS=("0.5","1","2","4","8","16","32"); _LBLS=("1/8","1/4","1/2","x1","x2","x4","x8")
for i in range(7):
    mm=add("#X msg %d 4810 %s;"%(2400+i*60,_MULTS[i]))
    lm=add("#X msg %d 4840 label %s;"%(2400+i*60,_LBLS[i]))
    c(rt7,i,mm,0); c(rt7,i,lm,0)
    c(mm,0,sdM,0); c(lm,0,sdL,0)
rowclk={}
_uid=0
for pg,lampfx in (("t","fl"),("p","pfl"),("f","ffl"),("m","mfl"),("m2","m2fl")):
    for v in range(1,9):
        X=2100+_uid*160; base=(v-1)*16
        mul=add("#X obj %d 1500 * 4;"%X)
        rmu=add("#X obj %d 1470 r \\$0-sq-mult-%d;"%(X+60,_uid))
        ii2=add("#X obj %d 1530 i;"%X)
        md2=add("#X obj %d 1560 mod 16;"%X)
        ch2=add("#X obj %d 1590 change -1;"%X)
        tspl=add("#X obj %d 1620 t f f f b;"%X)
        fpv=add("#X obj %d 1650 f -1;"%(X+60))
        addO=add("#X obj %d 1680 + %d;"%(X+60,base))
        mkO=add("#X obj %d 1710 makefilename \\$0-r-sq-%s-%%d;"%(X+60,lampfx))
        tbO=add("#X obj %d 1740 t b a;"%(X+60))
        m0=add("#X msg %d 1770 set 0;"%(X+60))
        addN=add("#X obj %d 1680 + %d;"%(X,base))
        mkN=add("#X obj %d 1710 makefilename \\$0-r-sq-%s-%%d;"%(X,lampfx))
        tbN=add("#X obj %d 1740 t b a;"%X)
        m1=add("#X msg %d 1770 set 1;"%X)
        sd=add("#X obj %d 1810 s;"%X)
        rsc=add("#X obj %d 1440 r \\$0-sq-stopclr;"%(X+100))
        tsc=add("#X obj %d 1470 t b b;"%(X+100))
        mn=add("#X msg %d 1500 -1;"%(X+100))
        c(un,0,mul,0); c(rmu,0,mul,1)
        c(mul,0,ii2,0); c(ii2,0,md2,0); c(md2,0,ch2,0); c(ch2,0,tspl,0)
        c(tspl,3,fpv,0)
        c(fpv,0,addO,0); c(addO,0,mkO,0); c(mkO,0,tbO,0)
        c(tbO,1,sd,1); c(tbO,0,m0,0); c(m0,0,sd,0)
        c(tspl,2,fpv,1)
        c(tspl,1,addN,0); c(addN,0,mkN,0); c(mkN,0,tbN,0)
        c(tbN,1,sd,1); c(tbN,0,m1,0); c(m1,0,sd,0)
        c(rsc,0,tsc,0); c(tsc,1,fpv,0)
        c(tsc,0,mn,0); c(mn,0,fpv,1)
        rowclk[(pg,v)]=tspl
        _uid+=1

# --- lamp click-revert: lamps are display-only cues ---
s_lrev=add("#X obj 25000 5000 s \\$0-sq-lamprevert;")
r_lrev=add("#X obj 25000 5040 r \\$0-sq-lamprevert;")
uplr=add("#X obj 25000 5070 unpack f f;")
finv=add("#X obj 25400 5100 f;")
inv1=add("#X obj 25400 5130 * -1;")
inv2=add("#X obj 25400 5160 + 1;")
tgid=add("#X obj 25000 5100 t f f;")
md128=add("#X obj 25060 5130 mod 128;")
d128=add("#X obj 25000 5130 / 128;")
i128=add("#X obj 25000 5160 i;")
rt5=add("#X obj 25000 5190 route 0 1 2 3 4;")
sdrv=add("#X obj 25000 5400 s;")
mset=add("#X msg 25400 5220 set \\$1;")
c(r_lrev,0,uplr,0)
c(uplr,1,inv1,0); c(inv1,0,inv2,0); c(inv2,0,finv,1)
c(uplr,0,tgid,0)
c(tgid,1,md128,0)
c(tgid,0,d128,0); c(d128,0,i128,0); c(i128,0,rt5,0)
for _pi,_pfx in enumerate(("fl","pfl","ffl","mfl","m2fl")):
    _fb=add("#X obj %d 5230 f;"%(25000+_pi*100))
    _mk=add("#X obj %d 5260 makefilename \\$0-r-sq-%s-%%d;"%(25000+_pi*100,_pfx))
    _tb=add("#X obj %d 5290 t b a;"%(25000+_pi*100))
    c(rt5,_pi,_fb,0); c(md128,0,_fb,1)
    c(_fb,0,_mk,0); c(_mk,0,_tb,0)
    c(_tb,1,sdrv,1); c(_tb,0,finv,0)
c(finv,0,mset,0); c(mset,0,sdrv,0)
for _pi,_pfx in enumerate(("fl","pfl","ffl","mfl","m2fl")):
    for _idx in range(128):
        _gid=_pi*128+_idx
        _mm=add("#X msg %d %d %d \\$1;"%(25000+(_gid%16)*70,5500+(_gid//16)*26,_gid))
        c(wid("r-sq-%s-%d"%(_pfx,_idx)),0,_mm,0)
        c(_mm,0,s_lrev,0)

# --- trigger voices (env) ---
envsel={}
ptrans={}
lb=add("#X obj 3400 1350 loadbang;")
m15=add("#X msg 3400 1380 1 5;")
c(lb,0,m15,0)
for v in range(1,9):
    X=2100+(v-1)*220
    add("#N canvas 0 0 200 140 (subpatch) 0;\n#X array \\$0-sq-seq-%d 16 float 3;\n#A 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;\n#X coords 0 1 16 0 140 60 1;\n#X restore %d 1900 graph;"%(v,X))
    s_arr=add("#X obj %d 1980 s \\$0-sq-seq-%d;"%(X,v))
    for s in range(16):
        gm=add("#X msg %d %d %d \\$1;"%(X,2010+s*22,s))
        ti=wid("r-sq-t-%d"%((v-1)*16+s))
        assert 'tgl' in objs[ti-BASE] and ('sq-t-%d '%((v-1)*16+s)) in objs[ti-BASE], objs[ti-BASE][:80]
        c(ti,0,gm,0); c(gm,0,s_arr,0)
    tr=add("#X obj %d 2400 tabread \\$0-sq-seq-%d;"%(X,v))
    spv=add("#X obj %d 2430 spigot 0;"%X)
    sel=add("#X obj %d 2460 sel 1 0;"%X)
    envsel[v]=sel
    tb=add("#X obj %d 2490 t b b b;"%X)
    fA=add("#X obj %d 2520 f 5;"%X)
    fD=add("#X obj %d 2550 f 120;"%(X+40))
    fS=add("#X obj %d 2580 f 0.7;"%(X+80))
    pk=add("#X obj %d 2610 pack 5 120 0.7;"%X)
    mOn=add("#X msg %d 2640 1 \\$1 \\, \\$3 \\$2 \\$1;"%X)
    fR=add("#X obj %d 2670 f 300;"%(X+120))
    mOff=add("#X msg %d 2700 0 \\$1;"%(X+120))
    vl=add("#X obj %d 2730 vline~;"%X)
    ss=add("#X obj %d 2760 s~ \\$0-env-%d;"%(X,v))
    c(rowclk[("t",v)],0,tr,0); c(tr,0,spv,0); c(spv,0,sel,0); c(sel,0,tb,0)
    c(tb,2,fS,0); c(tb,1,fD,0); c(tb,0,fA,0)
    c(fS,0,pk,2); c(fD,0,pk,1); c(fA,0,pk,0)
    c(pk,0,mOn,0); c(mOn,0,vl,0)
    c(sel,1,fR,0); c(fR,0,mOff,0); c(mOff,0,vl,0)
    c(vl,0,ss,0); c(m15,0,vl,0)
    rm=add("#X obj %d 2800 r \\$0-s-sq-m-%d;"%(X,v))
    tfm=add("#X obj %d 2830 t f f f;"%X)
    slm=add("#X obj %d 2860 sel 0 1;"%X)
    mDr=add("#X msg %d 2890 1 30;"%X)
    mEn=add("#X msg %d 2920 0 300;"%(X+50))
    lD=add("#X msg %d 2950 label OFF;"%X)
    lE=add("#X msg %d 2980 label ON;"%(X+80))
    sLb=add("#X obj %d 3010 s \\$0-r-sq-m-%d;"%(X,v))
    c(rm,0,tfm,0); c(tfm,2,spv,1); c(tfm,1,slm,0)
    c(slm,0,mDr,0); c(slm,1,mEn,0); c(mDr,0,vl,0); c(mEn,0,vl,0)
    c(slm,0,lD,0); c(slm,1,lE,0); c(lD,0,sLb,0); c(lE,0,sLb,0)
    c(tfm,0,srdw,0)
    for pn,tgt,curve,scale in (("a",fA,True,499),("d",fD,True,999),("su",fS,False,None),("re",fR,True,1999)):
        rr=add("#X obj %d 3050 r \\$0-s-sq-%s-%d;"%(X,pn,v))
        dv=add("#X obj %d 3080 / 127;"%X)
        c(rr,0,dv,0)
        if curve:
            pw=add("#X obj %d 3110 pow 2;"%X); ml=add("#X obj %d 3140 * %d;"%(X,scale)); adx=add("#X obj %d 3170 + 1;"%X)
            c(dv,0,pw,0); c(pw,0,ml,0); c(ml,0,adx,0); c(adx,0,tgt,1)
        else:
            c(dv,0,tgt,1)

# --- pitch engine ---
splab_live=add("#X obj 4500 3260 s \\$0-sq-plab;")
RANGES=[(-16,109),(-16,109),(7,102),(9,98),(20,96.54),(20,96.54),(33,93.24),(33,98.22)]
# store as (lo, hi-lo); values from $0-tune table: lo hi -> span=hi-lo
RANGES=[(-16,93),(-16,93),(7,109),(9,107),(20,116.54),(20,116.54),(33,126.24),(33,131.22)]
for v in range(1,9):
    X=2100+(v-1)*220
    add("#N canvas 0 0 200 140 (subpatch) 0;\n#X array \\$0-sq-pit-%d 16 float 3;\n#A 0 64 64 64 64 64 64 64 64 64 64 64 64 64 64 64 64;\n#X coords 0 127 16 0 140 60 1;\n#X restore %d 3300 graph;"%(v,X))
    s_par=add("#X obj %d 3380 s \\$0-sq-pit-%d;"%(X,v))
    for s in range(16):
        idx=(v-1)*16+s
        wm=add("#X msg %d %d %d \\$1;"%(X,3410+s*22,s))
        lm=add("#X msg %d %d %d \\$1;"%(X+110,3410+s*22,idx))
        pi=wid("r-sq-p-%d"%idx)
        assert 'vsl 16 40' in objs[pi-BASE] and ('sq-p-%d '%idx) in objs[pi-BASE], objs[pi-BASE][:80]
        c(pi,0,wm,0); c(wm,0,s_par,0)
        c(pi,0,lm,0); c(lm,0,splab_live,0)
    # apply at step
    trp=add("#X obj %d 3800 tabread \\$0-sq-pit-%d;"%(X,v))
    spp=add("#X obj %d 3830 spigot 0;"%X)
    stn=add("#X obj %d 3860 s \\$0-r-tune-%d;"%(X,v))
    rpe=add("#X obj %d 3890 r \\$0-s-sq-pe-%d;"%(X,v))
    ptr=add("#X obj %d 3845 + 0;"%(X+80))
    ptrans[v]=ptr
    c(rowclk[("p",v)],0,trp,0); c(trp,0,spp,0); c(spp,0,ptr,0); c(ptr,0,stn,0); c(rpe,0,spp,1)
# scale state + nearest-enabled-note map for quantized labels
add("#N canvas 0 0 200 140 (subpatch) 0;\n#X array \\$0-sq-scale 12 float 3;\n#A 0 1 1 1 1 1 1 1 1 1 1 1 1;\n#X coords 0 1 12 0 100 40 1;\n#X restore 22000 1300 graph;")
add("#N canvas 0 0 200 140 (subpatch) 0;\n#X array \\$0-sq-qmap 12 float 3;\n#A 0 0 1 2 3 4 5 6 7 8 9 10 11;\n#X coords 0 11 12 0 100 40 1;\n#X restore 22200 1300 graph;")
s_scl=add("#X obj 22000 1400 s \\$0-sq-scale;")
s_qrc=add("#X obj 22400 1400 s \\$0-sq-qmaprc;")
for n in range(12):
    r1=add("#X obj %d 1440 r \\$0-s-scale-%d;"%(22000+n*90,n))
    r2=add("#X obj %d 1470 r \\$0-scale-%d;"%(22000+n*90,n))
    mm=add("#X msg %d 1500 %d \\$1;"%(22000+n*90,n))
    tb_=add("#X obj %d 1530 t b;"%(22000+n*90))
    c(r1,0,mm,0); c(r2,0,mm,0); c(mm,0,s_scl,0); c(mm,0,tb_,0); c(tb_,0,s_qrc,0)
r_qrc=add("#X obj 22000 1600 r \\$0-sq-qmaprc;")
tqr=add("#X obj 22000 1630 t b b b b;")
c(r_qrc,0,tqr,0)
m0q=add("#X msg 22100 1660 0;")
m12q=add("#X msg 22160 1660 12;")
untq=add("#X obj 22160 1690 until;")
cntq=add("#X obj 22100 1720 f;")
incq=add("#X obj 22160 1720 + 1;")
tpc=add("#X obj 22100 1750 t f f;")
fpcv=add("#X obj 22240 1750 f;")
m13=add("#X msg 22100 1780 13;")
unt7=add("#X obj 22100 1810 until;")
cntk=add("#X obj 22040 1840 f;")
inck=add("#X obj 22100 1840 + 1;")
m0k=add("#X msg 22300 1780 0;")
tk=add("#X obj 22040 1870 t f f;")
kp1=add("#X obj 22100 1900 + 1;")
kd2=add("#X obj 22100 1930 / 2;")
ki=add("#X obj 22100 1960 i;")
km2=add("#X obj 22180 1900 mod 2;")
ke1=add("#X obj 22180 1930 == 0;")
ks=add("#X obj 22180 1960 * -2;")
ka1=add("#X obj 22180 1990 + 1;")
kmul=add("#X obj 22100 2020 *;")
cadd=add("#X obj 22100 2050 + 0;")
c12a=add("#X obj 22100 2080 + 12;")
cm12=add("#X obj 22100 2110 mod 12;")
tcand=add("#X obj 22100 2140 t f f;")
trd=add("#X obj 22160 2170 tabread \\$0-sq-scale;")
sl1=add("#X obj 22160 2200 sel 1;")
fcand=add("#X obj 22100 2230 f;")
pkq=add("#X obj 22100 2260 pack f f;")
mswap=add("#X msg 22100 2290 \\$2 \\$1;")
s_qm=add("#X obj 22100 2320 s \\$0-sq-qmap;")
stopb=add("#X obj 22300 2230 t b;")
c(tqr,3,m0q,0); c(m0q,0,cntq,1)
c(tqr,2,m12q,0); c(m12q,0,untq,0); c(untq,0,cntq,0)
c(cntq,0,tpc,0); c(tpc,1,incq,0); c(incq,0,cntq,1)
c(tpc,1,cadd,1); c(tpc,1,pkq,1)
c(tpc,0,m0k,0); c(m0k,0,cntk,1)
c(tpc,0,m13,0); c(m13,0,unt7,0); c(unt7,0,cntk,0)
c(cntk,0,tk,0); c(tk,1,inck,0); c(inck,0,cntk,1)
c(tk,0,kp1,0); c(kp1,0,kd2,0); c(kd2,0,ki,0); c(ki,0,kmul,0)
c(tk,0,km2,0); c(km2,0,ke1,0); c(ke1,0,ks,0); c(ks,0,ka1,0); c(ka1,0,kmul,1)
c(kmul,0,cadd,0)
c(cadd,0,c12a,0); c(c12a,0,cm12,0); c(cm12,0,tcand,0)
c(tcand,1,fcand,1)
c(tcand,0,trd,0); c(trd,0,sl1,0)
c(sl1,0,fcand,0); c(fcand,0,pkq,0)
c(pkq,0,mswap,0); c(mswap,0,s_qm,0)
c(sl1,0,stopb,0); c(stopb,0,unt7,1)
qtr=add("#X obj 22400 2140 tabread \\$0-sq-qmap;")
lb_q=add("#X obj 22500 1600 loadbang;")
dl_q=add("#X obj 22500 1630 del 600;")
c(lb_q,0,dl_q,0); c(dl_q,0,s_qrc,0)
# shared labeler
s_plab_r=add("#X obj 4600 3300 r \\$0-sq-plab;")
upl=add("#X obj 4600 3330 unpack f f;")
tidx=add("#X obj 4600 3390 t f f f;")
mkt=add("#X obj 4700 3420 makefilename \\$0-r-sq-p-%d;")
sd2=add("#X obj 4600 3900 s;")
d16=add("#X obj 4600 3450 / 16;")
i16=add("#X obj 4600 3480 i;")
p1v=add("#X obj 4600 3510 + 1;")
rt8=add("#X obj 4600 3540 route 1 2 3 4 5 6 7 8;")
mrg=add("#X obj 4600 3690 + 120;")
imrg=add("#X obj 4600 3720 i;")
md12=add("#X obj 4600 3750 mod 12;")
q_on=add("#X obj 4560 3660 spigot 0;")
rt12=add("#X obj 4600 3780 route 0 1 2 3 4 5 6 7 8 9 10 11;")
NOTE=["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"]
nmsgs=[add("#X msg %d 3810 label %s;"%(4600+i*38,NOTE[i])) for i in range(12)]
chsem=add("#X obj 5100 3750 change;")
tbr=add("#X obj 5100 3780 t b;")
q_off=add("#X obj 5200 3660 spigot 1;")
moff=add("#X msg 5200 3690 label empty;")
c(s_plab_r,0,upl,0)
c(upl,0,tidx,0)
c(tidx,2,mkt,0); c(mkt,0,sd2,1)
c(tidx,1,d16,0); c(d16,0,i16,0); c(i16,0,p1v,0); c(p1v,0,rt8,0)
for i,(lo,hi) in enumerate(RANGES):
    fv=add("#X obj %d 3570 f;"%(4600+i*60))
    dv=add("#X obj %d 3600 / 127;"%(4600+i*60))
    ml=add("#X obj %d 3630 * %s;"%(4600+i*60,("%g"%(hi-lo))))
    al=add("#X obj %d 3660 + %s;"%(4600+i*60,("%g"%lo)))
    c(rt8,i,fv,0); c(upl,1,fv,1)
    c(fv,0,dv,0); c(dv,0,ml,0); c(ml,0,al,0); c(al,0,q_on,0)
tsem=add("#X obj 4600 3765 t f f;")
c(q_on,0,mrg,0); c(mrg,0,imrg,0); c(imrg,0,md12,0); c(md12,0,qtr,0); c(qtr,0,tsem,0)
c(tsem,1,rt12,0)
for i,nm in enumerate(nmsgs): c(rt12,i,nm,0); c(nm,0,sd2,0)
c(tsem,0,chsem,0); c(chsem,0,tbr,0); c(tbr,0,srdw,0)
c(tidx,0,q_off,0); c(q_off,0,moff,0); c(moff,0,sd2,0)
# quantize watcher + full refresh loop
rq1=add("#X obj 5400 3300 r \\$0-s-quantize;")
rq2=add("#X obj 5520 3300 r \\$0-quantize;")
lbq=add("#X obj 5640 3300 loadbang;")
mq0=add("#X msg 5640 3330 0;")
fq=add("#X obj 5400 3360 f;")
chq=add("#X obj 5400 3390 change;")
tq=add("#X obj 5400 3420 t b f f;")
eq0=add("#X obj 5480 3450 == 0;")
c(rq1,0,fq,0); c(rq2,0,fq,0); c(lbq,0,mq0,0); c(mq0,0,fq,0)
c(fq,0,chq,0); c(chq,0,tq,0)
c(tq,2,q_on,1)
c(tq,1,eq0,0); c(eq0,0,q_off,1)
# refresh: iterate all 128 (uses its own counter + shared tabread w/ settable name)
m0b=add("#X msg 5400 3480 0;")
mNb=add("#X msg 5460 3480 128;")
untb=add("#X obj 5460 3510 until;")
cntb=add("#X obj 5400 3540 f;")
incb=add("#X obj 5460 3540 + 1;")
tfb=add("#X obj 5400 3570 t f f f;")
d16b=add("#X obj 5480 3600 / 16;")
i16b=add("#X obj 5480 3630 i;")
p1b=add("#X obj 5480 3660 + 1;")
mkab=add("#X obj 5480 3690 makefilename \\$0-sq-pit-%d;")
msetb=add("#X msg 5480 3720 set \\$1;")
md16b=add("#X obj 5440 3750 mod 16;")
trb=add("#X obj 5440 3780 tabread \\$0-sq-pit-1;")
pkb=add("#X obj 5400 3810 pack f f;")
splab=add("#X obj 5400 3840 s \\$0-sq-plab;")
c(tq,0,m0b,0); c(tq,0,mNb,0)
c(m0b,0,cntb,1); c(mNb,0,untb,0); c(untb,0,cntb,0)
c(cntb,0,tfb,0); c(tfb,1,incb,0); c(incb,0,cntb,1)
c(tfb,2,d16b,0); c(d16b,0,i16b,0); c(i16b,0,p1b,0); c(p1b,0,mkab,0); c(mkab,0,msetb,0); c(msetb,0,trb,0)
c(tfb,1,md16b,0); c(md16b,0,trb,0); c(trb,0,pkb,1)
c(tfb,0,pkb,0); c(pkb,0,splab,0)
c(tq,0,srdw,0)
c(tqr,1,srdw,0)
c(tqr,0,m0b,0); c(tqr,0,mNb,0)
# quantize sync bridges (page copy <-> main widget, loop-safe)
rq_pg=add("#X obj 5700 3200 r \\$0-s-sq-q;")
sq_main=add("#X obj 5700 3230 s \\$0-r-quantize;")
c(rq_pg,0,sq_main,0)
rq_mn=add("#X obj 5850 3200 r \\$0-s-quantize;")
mset_q=add("#X msg 5850 3230 set \\$1;")
sq_pg=add("#X obj 5850 3260 s \\$0-r-sq-q;")
c(rq_mn,0,mset_q,0); c(mset_q,0,sq_pg,0)
# per-voice randomize / clear (drives the widgets; array+labels follow)
vmsgs_r=[]; vmsgs_c=[]
for v in range(1,9):
    rr=add("#X obj %d 4000 r \\$0-s-sq-rn-%d;"%(5400+v*90,v))
    mr=add("#X msg %d 4030 %d 0;"%(5400+v*90,v))
    c(rr,0,mr,0); vmsgs_r.append(mr)
    rc=add("#X obj %d 4060 r \\$0-s-sq-cl-%d;"%(5400+v*90,v))
    mc=add("#X msg %d 4090 %d 1;"%(5400+v*90,v))
    c(rc,0,mc,0); vmsgs_c.append(mc)
r_rna=add("#X obj 5400 4130 r \\$0-s-sq-rna;")
fan_rna=add("#X obj 5400 4160 t b b b b b b b b;")
c(r_rna,0,fan_rna,0)
r_cla=add("#X obj 5400 4200 r \\$0-s-sq-cla;")
fan_cla=add("#X obj 5400 4230 t b b b b b b b b;")
c(r_cla,0,fan_cla,0)
for v in range(8):
    c(fan_rna,7-v,vmsgs_r[v],0)
    c(fan_cla,7-v,vmsgs_c[v],0)
upvc=add("#X obj 5400 4270 unpack f f;")
fmd=add("#X obj 5620 4300 f;")
tvv=add("#X obj 5400 4300 t f f f;")
sub1=add("#X obj 5470 4330 - 1;")
mul16=add("#X obj 5470 4360 * 16;")
addb=add("#X obj 5400 4450 + 0;")
m0d=add("#X msg 5400 4330 0;")
m16d=add("#X msg 5440 4390 16;")
untd=add("#X obj 5440 4420 until;")
cntd=add("#X obj 5400 4390 f;")
incd=add("#X obj 5460 4450 + 1;")
tcd=add("#X obj 5400 4420 t f f;")
mkd=add("#X obj 5400 4480 makefilename \\$0-r-sq-p-%d;")
tad=add("#X obj 5400 4510 t b a;")
sd4=add("#X obj 5400 4600 s;")
seld=add("#X obj 5480 4540 sel 0 1;")
tbd=add("#X obj 5480 4570 t b;")
rnd128=add("#X obj 5480 4600 random 128;")
m64d=add("#X msg 5560 4570 64;")
srd2=add("#X obj 5650 4400 s \\$0-redraw;")
for m in vmsgs_r+vmsgs_c: c(m,0,upvc,0)
c(upvc,1,fmd,1)
c(upvc,0,tvv,0)
c(tvv,2,sub1,0); c(sub1,0,mul16,0); c(mul16,0,addb,1)
c(tvv,1,m0d,0); c(m0d,0,cntd,1)
c(tvv,1,m16d,0); c(m16d,0,untd,0); c(untd,0,cntd,0)
c(cntd,0,tcd,0); c(tcd,1,incd,0); c(incd,0,cntd,1)
c(tcd,0,addb,0); c(addb,0,mkd,0); c(mkd,0,tad,0)
c(tad,1,sd4,1)
c(tad,0,fmd,0); c(fmd,0,seld,0)
c(seld,0,tbd,0); c(tbd,0,rnd128,0); c(rnd128,0,sd4,0)
c(seld,1,m64d,0); c(m64d,0,sd4,0)
c(tvv,0,srd2,0)
# --- filter sequencer engine ---
famt_targets=[]
for v in range(1,9):
    X=6200+(v-1)*240
    add("#N canvas 0 0 200 140 (subpatch) 0;\n#X array \\$0-sq-fcut-%d 16 float 3;\n#A 0 127 127 127 127 127 127 127 127 127 127 127 127 127 127 127 127;\n#X coords 0 127 16 0 140 60 1;\n#X restore %d 3300 graph;"%(v,X))
    add("#N canvas 0 0 200 140 (subpatch) 0;\n#X array \\$0-sq-ftrg-%d 16 float 3;\n#A 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;\n#X coords 0 1 16 0 140 60 1;\n#X restore %d 3380 graph;"%(v,X+120))
    s_fc=add("#X obj %d 3460 s \\$0-sq-fcut-%d;"%(X,v))
    s_ft=add("#X obj %d 3460 s \\$0-sq-ftrg-%d;"%(X+120,v))
    for s in range(16):
        idx=(v-1)*16+s
        fm=add("#X msg %d %d %d \\$1;"%(X,3490+s*22,s))
        c(wid("r-sq-fc-%d"%idx),0,fm,0); c(fm,0,s_fc,0)
        tm=add("#X msg %d %d %d \\$1;"%(X+120,3490+s*22,s))
        c(wid("r-sq-ft-%d"%idx),0,tm,0); c(tm,0,s_ft,0)
    trc=add("#X obj %d 3860 tabread \\$0-sq-fcut-%d;"%(X,v))
    spc=add("#X obj %d 3890 spigot 0;"%X)
    stc=add("#X obj %d 3920 s \\$0-r-cut-%d;"%(X,v))
    rfe=add("#X obj %d 3950 r \\$0-s-sq-fe-%d;"%(X,v))
    c(rowclk[("f",v)],0,trc,0); c(trc,0,spc,0); c(spc,0,stc,0); c(rfe,0,spc,1)
    trf=add("#X obj %d 3990 tabread \\$0-sq-ftrg-%d;"%(X,v))
    sef=add("#X obj %d 4020 sel 1 0;"%X)
    tbf=add("#X obj %d 4050 t b b b;"%X)
    ffA=add("#X obj %d 4080 f 5;"%X)
    ffD=add("#X obj %d 4110 f 150;"%(X+40))
    ffS=add("#X obj %d 4140 f 0.5;"%(X+80))
    pkf=add("#X obj %d 4170 pack 5 150 0.5;"%X)
    mOnf=add("#X msg %d 4200 1 \\$1 \\, \\$3 \\$2 \\$1;"%X)
    ffR=add("#X obj %d 4230 f 300;"%(X+120))
    mOfff=add("#X msg %d 4260 0 \\$1;"%(X+120))
    vlf=add("#X obj %d 4290 vline~;"%X)
    ssf=add("#X obj %d 4320 s~ \\$0-fenv-%d;"%(X,v))
    c(rowclk[("f",v)],0,trf,0); c(trf,0,sef,0); c(sef,0,tbf,0)
    c(tbf,2,ffS,0); c(tbf,1,ffD,0); c(tbf,0,ffA,0)
    c(ffS,0,pkf,2); c(ffD,0,pkf,1); c(ffA,0,pkf,0)
    c(pkf,0,mOnf,0); c(mOnf,0,vlf,0)
    c(sef,1,ffR,0); c(ffR,0,mOfff,0); c(mOfff,0,vlf,0)
    mulfam=add("#X obj %d 4310 *~;"%(X+160))
    c(vlf,0,mulfam,0); c(mulfam,0,ssf,0); famt_targets.append(mulfam)
    for pn,tgt,curve,scale in (("fa",ffA,True,499),("fd",ffD,True,999),("fsu",ffS,False,None),("fre",ffR,True,1999)):
        rr=add("#X obj %d 4360 r \\$0-s-sq-%s-%d;"%(X,pn,v))
        dv=add("#X obj %d 4390 / 127;"%X)
        c(rr,0,dv,0)
        if curve:
            pw=add("#X obj %d 4420 pow 2;"%X); ml=add("#X obj %d 4450 * %d;"%(X,scale)); adx=add("#X obj %d 4480 + 1;"%X)
            c(dv,0,pw,0); c(pw,0,ml,0); c(ml,0,adx,0); c(adx,0,tgt,1)
        else:
            c(dv,0,tgt,1)

# --- filter rnd/clr (targets fc widgets; clear=127) ---
fmsgs_r=[];fmsgs_c=[]
for v in range(1,9):
    rr=add("#X obj %d 5000 r \\$0-s-sq-frn-%d;"%(5400+v*90,v))
    mr=add("#X msg %d 5030 %d 0;"%(5400+v*90,v)); c(rr,0,mr,0); fmsgs_r.append(mr)
    rc=add("#X obj %d 5060 r \\$0-s-sq-fcl-%d;"%(5400+v*90,v))
    mc=add("#X msg %d 5090 %d 1;"%(5400+v*90,v)); c(rc,0,mc,0); fmsgs_c.append(mc)
rfna=add("#X obj 5400 5130 r \\$0-s-sq-frna;")
ffna=add("#X obj 5400 5160 t b b b b b b b b;")
c(rfna,0,ffna,0)
rfca=add("#X obj 5400 5200 r \\$0-s-sq-fcla;")
ffca=add("#X obj 5400 5230 t b b b b b b b b;")
c(rfca,0,ffca,0)
for v in range(8):
    c(ffna,7-v,fmsgs_r[v],0); c(ffca,7-v,fmsgs_c[v],0)
upf=add("#X obj 5400 5270 unpack f f;")
fmdf=add("#X obj 5620 5300 f;")
tvf=add("#X obj 5400 5300 t f f f;")
subf=add("#X obj 5470 5330 - 1;")
mulf=add("#X obj 5470 5360 * 16;")
addf=add("#X obj 5400 5450 + 0;")
m0e=add("#X msg 5400 5330 0;")
m16e=add("#X msg 5440 5390 16;")
unte=add("#X obj 5440 5420 until;")
cnte=add("#X obj 5400 5390 f;")
ince=add("#X obj 5460 5450 + 1;")
tce=add("#X obj 5400 5420 t f f;")
mke=add("#X obj 5400 5480 makefilename \\$0-r-sq-fc-%d;")
tae=add("#X obj 5400 5510 t b a;")
sd6=add("#X obj 5400 5600 s;")
sele=add("#X obj 5480 5540 sel 0 1;")
tbe=add("#X obj 5480 5570 t b;")
rnde=add("#X obj 5480 5600 random 128;")
m127e=add("#X msg 5560 5570 127;")
for m in fmsgs_r+fmsgs_c: c(m,0,upf,0)
c(upf,1,fmdf,1); c(upf,0,tvf,0)
c(tvf,2,subf,0); c(subf,0,mulf,0); c(mulf,0,addf,1)
c(tvf,1,m0e,0); c(m0e,0,cnte,1)
c(tvf,1,m16e,0); c(m16e,0,unte,0); c(unte,0,cnte,0)
c(cnte,0,tce,0); c(tce,1,ince,0); c(ince,0,cnte,1)
c(tce,0,addf,0); c(addf,0,mke,0); c(mke,0,tae,0)
c(tae,1,sd6,1); c(tae,0,fmdf,0); c(fmdf,0,sele,0)
c(sele,0,tbe,0); c(tbe,0,rnde,0); c(rnde,0,sd6,0)
c(sele,1,m127e,0); c(m127e,0,sd6,0)
c(tvf,0,srd2,0)
# --- mod/sharp sequencer engine ---
_MTGT=("mod-12","mod-34","mod-56","mod-78","sharp-12","sharp-34","sharp-56","sharp-78")
for v in range(1,9):
    X=12000+(v-1)*240
    add("#N canvas 0 0 200 140 (subpatch) 0;\n#X array \\$0-sq-mval-%d 16 float 3;\n#A 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0;\n#X coords 0 127 16 0 140 60 1;\n#X restore %d 1300 graph;"%(v,X))
    s_mv=add("#X obj %d 1380 s \\$0-sq-mval-%d;"%(X,v))
    for s in range(16):
        idx=(v-1)*16+s
        wm=add("#X msg %d %d %d \\$1;"%(X,1420+s*22,s))
        c(wid("r-sq-mv-%d"%idx),0,wm,0); c(wm,0,s_mv,0)
    trm=add("#X obj %d 1800 tabread \\$0-sq-mval-%d;"%(X,v))
    spm=add("#X obj %d 1830 spigot 0;"%X)
    stm=add("#X obj %d 1860 s \\$0-r-%s;"%(X,_MTGT[v-1]))
    rme=add("#X obj %d 1890 r \\$0-s-sq-me-%d;"%(X,v))
    c(rowclk[("m",v)],0,trm,0); c(trm,0,spm,0); c(spm,0,stm,0); c(rme,0,spm,1)
mmsgs_r=[];mmsgs_c=[]
for v in range(1,9):
    rr=add("#X obj %d 2000 r \\$0-s-sq-mrn-%d;"%(12000+v*90,v))
    mr=add("#X msg %d 2030 %d 0;"%(12000+v*90,v)); c(rr,0,mr,0); mmsgs_r.append(mr)
    rc=add("#X obj %d 2060 r \\$0-s-sq-mcl-%d;"%(12000+v*90,v))
    mc=add("#X msg %d 2090 %d 1;"%(12000+v*90,v)); c(rc,0,mc,0); mmsgs_c.append(mc)
rmna=add("#X obj 12000 2130 r \\$0-s-sq-mrna;")
fmna=add("#X obj 12000 2160 t b b b b b b b b;")
c(rmna,0,fmna,0)
rmca=add("#X obj 12000 2200 r \\$0-s-sq-mcla;")
fmca=add("#X obj 12000 2230 t b b b b b b b b;")
c(rmca,0,fmca,0)
for v in range(8):
    c(fmna,7-v,mmsgs_r[v],0); c(fmca,7-v,mmsgs_c[v],0)
upm=add("#X obj 12000 2270 unpack f f;")
fmdm=add("#X obj 12220 2300 f;")
tvm=add("#X obj 12000 2300 t f f f;")
subm=add("#X obj 12070 2330 - 1;")
mulm=add("#X obj 12070 2360 * 16;")
addm=add("#X obj 12000 2450 + 0;")
m0m=add("#X msg 12000 2330 0;")
m16m=add("#X msg 12040 2390 16;")
untm=add("#X obj 12040 2420 until;")
cntm=add("#X obj 12000 2390 f;")
incm=add("#X obj 12060 2450 + 1;")
tcm=add("#X obj 12000 2420 t f f;")
mkm2=add("#X obj 12000 2480 makefilename \\$0-r-sq-mv-%d;")
tam=add("#X obj 12000 2510 t b a;")
sd9=add("#X obj 12000 2600 s;")
selm2=add("#X obj 12080 2540 sel 0 1;")
tbm2=add("#X obj 12080 2570 t b;")
rndm=add("#X obj 12080 2600 random 128;")
m0v=add("#X msg 12160 2570 0;")
for m in mmsgs_r+mmsgs_c: c(m,0,upm,0)
c(upm,1,fmdm,1); c(upm,0,tvm,0)
c(tvm,2,subm,0); c(subm,0,mulm,0); c(mulm,0,addm,1)
c(tvm,1,m0m,0); c(m0m,0,cntm,1)
c(tvm,1,m16m,0); c(m16m,0,untm,0); c(untm,0,cntm,0)
c(cntm,0,tcm,0); c(tcm,1,incm,0); c(incm,0,cntm,1)
c(tcm,0,addm,0); c(addm,0,mkm2,0); c(mkm2,0,tam,0)
c(tam,1,sd9,1); c(tam,0,fmdm,0); c(fmdm,0,selm2,0)
c(selm2,0,tbm2,0); c(tbm2,0,rndm,0); c(rndm,0,sd9,0)
c(selm2,1,m0v,0); c(m0v,0,sd9,0)
c(tvm,0,srd2,0)
# --- MOD2 sequencer engine ---
_M2TGT=("pitch-1234","pitch-5678","f-a","f-b","time-1","time-2","feedback","vib-speed")
_M2DEF=(64,64,64,64,64,64,64,76)
s_m2lab=add("#X obj 15800 1300 s \\$0-sq-m2lab;")
for v in range(1,9):
    X=16000+(v-1)*240
    add("#N canvas 0 0 200 140 (subpatch) 0;\n#X array \\$0-sq-m2val-%d 16 float 3;\n#A 0 %s;\n#X coords 0 127 16 0 140 60 1;\n#X restore %d 1300 graph;"%(v," ".join([str(_M2DEF[v-1])]*16),X))
    s_m2=add("#X obj %d 1380 s \\$0-sq-m2val-%d;"%(X,v))
    for s in range(16):
        idx=(v-1)*16+s
        wm=add("#X msg %d %d %d \\$1;"%(X,1420+s*22,s))
        c(wid("r-sq-m2v-%d"%idx),0,wm,0); c(wm,0,s_m2,0)
        lm2=add("#X msg %d %d %d \\$1;"%(X+110,1420+s*22,idx))
        c(wid("r-sq-m2v-%d"%idx),0,lm2,0); c(lm2,0,s_m2lab,0)
    trm2=add("#X obj %d 1800 tabread \\$0-sq-m2val-%d;"%(X,v))
    spm2=add("#X obj %d 1830 spigot 0;"%X)
    stm2=add("#X obj %d 1860 s \\$0-r-%s;"%(X,_M2TGT[v-1]))
    rm2e=add("#X obj %d 1890 r \\$0-s-sq-m2e-%d;"%(X,v))
    c(rowclk[("m2",v)],0,trm2,0); c(trm2,0,spm2,0); c(spm2,0,stm2,0); c(rm2e,0,spm2,1)
m2r=[];m2c=[]
for v in range(1,9):
    rr=add("#X obj %d 2000 r \\$0-s-sq-m2rn-%d;"%(16000+v*90,v))
    mr=add("#X msg %d 2030 %d 0;"%(16000+v*90,v)); c(rr,0,mr,0); m2r.append(mr)
    rc=add("#X obj %d 2060 r \\$0-s-sq-m2cl-%d;"%(16000+v*90,v))
    mc=add("#X msg %d 2090 %d 1;"%(16000+v*90,v)); c(rc,0,mc,0); m2c.append(mc)
rm2na=add("#X obj 16000 2130 r \\$0-s-sq-m2rna;")
fm2na=add("#X obj 16000 2160 t b b b b b b b b;")
c(rm2na,0,fm2na,0)
rm2ca=add("#X obj 16000 2200 r \\$0-s-sq-m2cla;")
fm2ca=add("#X obj 16000 2230 t b b b b b b b b;")
c(rm2ca,0,fm2ca,0)
for v in range(8):
    c(fm2na,7-v,m2r[v],0); c(fm2ca,7-v,m2c[v],0)
up2=add("#X obj 16000 2270 unpack f f;")
fmd2=add("#X obj 16220 2300 f;")
flane=add("#X obj 16290 2300 f;")
tv2=add("#X obj 16000 2300 t f f f f;")
sub2=add("#X obj 16070 2330 - 1;")
mul2=add("#X obj 16070 2360 * 16;")
add2=add("#X obj 16000 2450 + 0;")
m02=add("#X msg 16000 2330 0;")
m162=add("#X msg 16040 2390 16;")
unt2=add("#X obj 16040 2420 until;")
cnt2=add("#X obj 16000 2390 f;")
inc2=add("#X obj 16060 2450 + 1;")
tc2=add("#X obj 16000 2420 t f f;")
mk2b=add("#X obj 16000 2480 makefilename \\$0-r-sq-m2v-%d;")
ta2=add("#X obj 16000 2510 t b a;")
sdA=add("#X obj 16000 2600 s;")
sel2=add("#X obj 16080 2540 sel 0 1;")
tb2b=add("#X obj 16080 2570 t b;")
rnd2=add("#X obj 16080 2600 random 128;")
tb2c=add("#X obj 16160 2570 t b;")
rt8b=add("#X obj 16160 2600 route 8;")
m76=add("#X msg 16160 2630 76;")
m64b=add("#X msg 16240 2630 64;")
for m in m2r+m2c: c(m,0,up2,0)
c(up2,1,fmd2,1); c(up2,0,tv2,0)
c(tv2,3,flane,1)
c(tv2,2,sub2,0); c(sub2,0,mul2,0); c(mul2,0,add2,1)
c(tv2,1,m02,0); c(m02,0,cnt2,1)
c(tv2,1,m162,0); c(m162,0,unt2,0); c(unt2,0,cnt2,0)
c(cnt2,0,tc2,0); c(tc2,1,inc2,0); c(inc2,0,cnt2,1)
c(tc2,0,add2,0); c(add2,0,mk2b,0); c(mk2b,0,ta2,0)
c(ta2,1,sdA,1); c(ta2,0,fmd2,0); c(fmd2,0,sel2,0)
c(sel2,0,tb2b,0); c(tb2b,0,rnd2,0); c(rnd2,0,sdA,0)
c(sel2,1,tb2c,0); c(tb2c,0,flane,0); c(flane,0,rt8b,0)
c(rt8b,0,m76,0); c(rt8b,1,m64b,0)
c(m76,0,sdA,0); c(m64b,0,sdA,0)
c(tv2,0,srd2,0)
# sync bridges (page toggles <-> main widgets, loop-safe)
for pgs,mainn in (("m2ls","lfo-sync"),("m2vs","vib-sync")):
    rp=add("#X obj 16600 2700 r \\$0-s-sq-%s;"%pgs)
    sm=add("#X obj 16600 2730 s \\$0-r-%s;"%mainn)
    c(rp,0,sm,0)
    rm_=add("#X obj 16800 2700 r \\$0-s-%s;"%mainn)
    ms_=add("#X msg 16800 2730 set \\$1;")
    sp_=add("#X obj 16800 2760 s \\$0-r-sq-%s;"%pgs)
    c(rm_,0,ms_,0); c(ms_,0,sp_,0)
# division labeler (lanes 3,4 gated by lfo-sync; lane 8 by vib-sync; others blank)
r_m2l=add("#X obj 17000 1300 r \\$0-sq-m2lab;")
upl2=add("#X obj 17000 1330 unpack f f;")
fvl2=add("#X obj 17260 1360 f;")
til2=add("#X obj 17000 1360 t f f;")
mkl2=add("#X obj 17100 1390 makefilename \\$0-r-sq-m2v-%d;")
sdB=add("#X obj 17000 1760 s;")
d16l=add("#X obj 17000 1420 / 16;")
i16l=add("#X obj 17000 1450 i;")
rtl=add("#X obj 17000 1480 route 2 3 7;")
spLF=add("#X obj 17000 1510 spigot 0;")
spLF2=add("#X obj 17060 1510 spigot 0;")
spVB=add("#X obj 17120 1510 spigot 0;")
spLFb=add("#X obj 17180 1510 spigot 1;")
spLF2b=add("#X obj 17240 1510 spigot 1;")
spVBb=add("#X obj 17300 1510 spigot 1;")
d128=add("#X obj 17000 1570 / 12.8;")
i10=add("#X obj 17000 1600 i;")
cl9=add("#X obj 17000 1630 clip 0 9;")
rt10=add("#X obj 17000 1660 route 0 1 2 3 4 5 6 7 8 9;")
mblk=add("#X msg 17420 1570 label empty;")
c(r_m2l,0,upl2,0)
c(upl2,1,fvl2,1)
c(upl2,0,til2,0)
c(til2,1,mkl2,0); c(mkl2,0,sdB,1)
c(til2,0,d16l,0); c(d16l,0,i16l,0); c(i16l,0,rtl,0)
c(rtl,0,spLF,0); c(rtl,0,spLFb,0)
c(rtl,1,spLF2,0); c(rtl,1,spLF2b,0)
c(rtl,2,spVB,0); c(rtl,2,spVBb,0)
c(rtl,3,mblk,0)
for sp_ in (spLF,spLF2,spVB):
    c(sp_,0,fvl2,0)
c(fvl2,0,d128,0)
for sp_ in (spLFb,spLF2b,spVBb):
    c(sp_,0,mblk,0)
c(d128,0,i10,0); c(i10,0,cl9,0); c(cl9,0,rt10,0)
c(mblk,0,sdB,0)
_DIVL=("x16","x8","x4","x2","x1","1/2","1/4","1/8","1/16","1/32")
for i in range(10):
    dm=add("#X msg %d 1690 label %s;"%(17000+i*60,_DIVL[i]))
    c(rt10,i,dm,0); c(dm,0,sdB,0)
# sync watchers: gates + full relabel + redraw
relb=add("#X obj 17600 2900 r \\$0-sq-m2relabel;")
srelb=add("#X obj 18400 2900 s \\$0-sq-m2relabel;")
t_rl=add("#X obj 17600 2930 t b b;")
m0r=add("#X msg 17600 2960 0;")
mNr=add("#X msg 17660 2960 128;")
untr=add("#X obj 17660 2990 until;")
cntr=add("#X obj 17600 3020 f;")
incr=add("#X obj 17660 3020 + 1;")
tcr=add("#X obj 17600 3050 t f f f f;")
d16r=add("#X obj 17720 3080 / 16;")
i16r=add("#X obj 17720 3110 i;")
p1r=add("#X obj 17720 3140 + 1;")
mkar=add("#X obj 17720 3170 makefilename \\$0-sq-m2val-%d;")
msr=add("#X msg 17720 3200 set \\$1;")
md16r=add("#X obj 17660 3230 mod 16;")
trr=add("#X obj 17660 3260 tabread \\$0-sq-m2val-1;")
pkr=add("#X obj 17600 3290 pack f f;")
c(relb,0,t_rl,0)
c(t_rl,1,m0r,0); c(m0r,0,cntr,1)
c(t_rl,1,mNr,0); c(mNr,0,untr,0); c(untr,0,cntr,0)
c(cntr,0,tcr,0); c(tcr,3,incr,0); c(incr,0,cntr,1)
c(tcr,2,d16r,0); c(d16r,0,i16r,0); c(i16r,0,p1r,0); c(p1r,0,mkar,0); c(mkar,0,msr,0); c(msr,0,trr,0)
c(tcr,1,md16r,0); c(md16r,0,trr,0); c(trr,0,pkr,1)
c(tcr,0,pkr,0); c(pkr,0,s_m2lab,0)
c(t_rl,0,srdw,0)
for psuf,gates in (("lfo-sync",(spLF,spLF2)),("vib-sync",(spVB,))):
    rw1=add("#X obj %d 3400 r \\$0-s-%s;"%(17600,psuf))
    rw2=add("#X obj %d 3430 r \\$0-%s;"%(17750,psuf))
    lbw=add("#X obj %d 3460 loadbang;"%(17900))
    mw0=add("#X msg %d 3490 0;"%(17900))
    fw=add("#X obj %d 3520 f;"%(17600))
    chw=add("#X obj %d 3550 change;"%(17600))
    tw=add("#X obj %d 3580 t b f f;"%(17600))
    ez=add("#X obj %d 3610 == 0;"%(17700))
    c(rw1,0,fw,0); c(rw2,0,fw,0); c(lbw,0,mw0,0); c(mw0,0,fw,0)
    c(fw,0,chw,0); c(chw,0,tw,0)
    for sp_ in gates:
        c(tw,2,sp_,1)
    c(tw,1,ez,0)
    for sp_ in gates:
        bidx={spLF:spLFb,spLF2:spLF2b,spVB:spVBb}[sp_]
        c(ez,0,bidx,1)
    c(tw,0,srelb,0)
# --- trigger-page rnd/clr engine ---
tr_r=[];tr_c=[]
for v in range(1,9):
    rr=add("#X obj %d 5700 r \\$0-s-sq-trn-%d;"%(20000+v*90,v))
    mr=add("#X msg %d 5730 %d 0;"%(20000+v*90,v)); c(rr,0,mr,0); tr_r.append(mr)
    rc=add("#X obj %d 5760 r \\$0-s-sq-tcl-%d;"%(20000+v*90,v))
    mc=add("#X msg %d 5790 %d 1;"%(20000+v*90,v)); c(rc,0,mc,0); tr_c.append(mc)
rtna=add("#X obj 20000 5830 r \\$0-s-sq-trna;")
ftna=add("#X obj 20000 5860 t b b b b b b b b;")
c(rtna,0,ftna,0)
rtca=add("#X obj 20000 5900 r \\$0-s-sq-tcla;")
ftca=add("#X obj 20000 5930 t b b b b b b b b;")
c(rtca,0,ftca,0)
for v in range(8):
    c(ftna,7-v,tr_r[v],0); c(ftca,7-v,tr_c[v],0)
upT=add("#X obj 20000 5970 unpack f f;")
fmdT=add("#X obj 20220 6000 f;")
tvT=add("#X obj 20000 6000 t f f f;")
subT=add("#X obj 20070 6030 - 1;")
mulT=add("#X obj 20070 6060 * 16;")
addT=add("#X obj 20000 6150 + 0;")
m0T=add("#X msg 20000 6030 0;")
m16T=add("#X msg 20040 6090 16;")
untT=add("#X obj 20040 6120 until;")
cntT=add("#X obj 20000 6090 f;")
incT=add("#X obj 20060 6150 + 1;")
tcT=add("#X obj 20000 6120 t f f;")
mkT=add("#X obj 20000 6180 makefilename \\$0-r-sq-t-%d;")
taT=add("#X obj 20000 6210 t b a;")
sdT=add("#X obj 20000 6300 s;")
selT=add("#X obj 20080 6240 sel 0 1;")
tbT=add("#X obj 20080 6270 t b;")
rndT=add("#X obj 20080 6300 random 2;")
m0z=add("#X msg 20160 6270 0;")
for m in tr_r+tr_c: c(m,0,upT,0)
c(upT,1,fmdT,1); c(upT,0,tvT,0)
c(tvT,2,subT,0); c(subT,0,mulT,0); c(mulT,0,addT,1)
c(tvT,1,m0T,0); c(m0T,0,cntT,1)
c(tvT,1,m16T,0); c(m16T,0,untT,0); c(untT,0,cntT,0)
c(cntT,0,tcT,0); c(tcT,1,incT,0); c(incT,0,cntT,1)
c(tcT,0,addT,0); c(addT,0,mkT,0); c(mkT,0,taT,0)
c(taT,1,sdT,1); c(taT,0,fmdT,0); c(fmdT,0,selT,0)
c(selT,0,tbT,0); c(tbT,0,rndT,0); c(rndT,0,sdT,0)
c(selT,1,m0z,0); c(m0z,0,sdT,0)
c(tvT,0,srd2,0)
# --- MIDI engine: ch1-8 per-voice play, ch9 legacy sensor map ---
_LO=(-16,-16,7,9,20,20,33,33)
_SPAN=(109.0,109.0,102.0,98.0,96.54,96.54,93.24,98.22)
nin=add("#X obj 20000 6000 notein;")
mpk=add("#X obj 20000 6040 pack f f;")
c(nin,0,mpk,0); c(nin,1,mpk,1)
tst=add("#X obj 20400 6000 r lira8midi;")
tup=add("#X obj 20400 6030 unpack f f f;")
c(tst,0,tup,0)
c(tup,0,mpk,0); c(tup,1,mpk,1)
c(tup,0,207,0); c(tup,1,207,1)
c9=add("#X obj 20800 6000 == 9;")
s9=add("#X obj 20800 6030 spigot;")
c(206,2,c9,0); c(tup,2,c9,0)
c(c9,0,s9,1); c(210,0,s9,0); c(s9,0,208,0)
rme=add("#X obj 21200 6000 r \\$0-s-sq-menv;")
for v in range(1,9):
    X=20000+(v-1)*400; _lo=_LO[v-1]; _k=127.0/_SPAN[v-1]
    eq=add("#X obj %d 6100 == %d;"%(X,v))
    sch=add("#X obj %d 6130 spigot;"%X)
    c(nin,2,eq,0); c(tup,2,eq,0)
    c(eq,0,sch,1); c(mpk,0,sch,0)
    um=add("#X obj %d 6160 unpack f f;"%X)
    c(sch,0,um,0)
    vg=add("#X obj %d 6190 > 0;"%(X+140))
    c(um,1,vg,0)
    tvg=add("#X obj %d 6220 t f f;"%(X+140))
    c(vg,0,tvg,0)
    d2=add("#X obj %d 6250 * 2;"%(X+140))
    d1=add("#X obj %d 6280 - 1;"%(X+140))
    acc=add("#X obj %d 6310 + 0;"%(X+140))
    tac=add("#X obj %d 6340 t f f;"%(X+140))
    c(tvg,0,d2,0); c(d2,0,d1,0); c(d1,0,acc,0); c(acc,0,tac,0); c(tac,1,acc,1)
    g0=add("#X obj %d 6370 > 0;"%(X+140))
    chg=add("#X obj %d 6400 change;"%(X+140))
    c(tac,0,g0,0); c(g0,0,chg,0)
    tse=add("#X obj %d 6430 t f f f;"%(X+140))
    c(chg,0,tse,0)
    ssr=add("#X obj %d 6460 s \\$0-r-sensor-%d;"%(X+140,v))
    sss=add("#X obj %d 6460 s \\$0-s-sensor-%d;"%(X+240,v))
    c(tse,2,ssr,0); c(tse,1,sss,0)
    se1=add("#X obj %d 6490 spigot;"%(X+140))
    se2=add("#X obj %d 6520 spigot;"%(X+140))
    rmv=add("#X obj %d 6490 r \\$0-s-sq-m-%d;"%(X+260,v))
    c(rme,0,se1,1); c(rmv,0,se2,1)
    c(tse,0,se1,0); c(se1,0,se2,0); c(se2,0,envsel[v],0)
    sp=add("#X obj %d 6250 spigot;"%X)
    c(tvg,1,sp,1)
    c(um,0,sp,0)
    tmode=add("#X obj %d 6280 t f f;"%X)
    c(sp,0,tmode,0)
    spt=add("#X obj %d 6310 spigot 0;"%(X+70))
    c(tmode,1,spt,0)
    sub60=add("#X obj %d 6340 - 60;"%(X+70))
    mk1=add("#X obj %d 6370 * %.5f;"%(X+70,_k))
    c(spt,0,sub60,0); c(sub60,0,mk1,0); c(mk1,0,ptrans[v],1)
    spa=add("#X obj %d 6310 spigot 1;"%X)
    c(tmode,0,spa,0)
    tq=add("#X obj %d 6340 t f f;"%X)
    c(spa,0,tq,0)
    nadd=add("#X obj %d 6580 + 0;"%X)
    c(tq,1,nadd,1)
    md=add("#X obj %d 6370 mod 12;"%X)
    c(tq,0,md,0)
    tpc=add("#X obj %d 6400 t f f;"%X)
    c(md,0,tpc,0)
    dsub=add("#X obj %d 6490 - 0;"%X)
    c(tpc,1,dsub,1)
    qt=add("#X obj %d 6430 tabread \\$0-sq-qmap;"%X)
    c(tpc,0,qt,0); c(qt,0,dsub,0)
    a18=add("#X obj %d 6520 + 18;"%(X+70))
    m12b=add("#X obj %d 6550 mod 12;"%(X+70))
    s6=add("#X obj %d 6580 - 6;"%(X+70))
    c(dsub,0,a18,0); c(a18,0,m12b,0); c(m12b,0,s6,0); c(s6,0,nadd,0)
    slo=add("#X obj %d 6610 - %d;"%(X,_lo))
    mk2=add("#X obj %d 6640 * %.5f;"%(X,_k))
    clp=add("#X obj %d 6670 clip 0 127;"%X)
    stw=add("#X obj %d 6700 s \\$0-r-tune-%d;"%(X,v))
    c(nadd,0,slo,0); c(slo,0,mk2,0); c(mk2,0,clp,0); c(clp,0,stw,0)
    rp2=add("#X obj %d 6100 r \\$0-s-sq-pe-%d;"%(X+200,v))
    tpe=add("#X obj %d 6130 t f f;"%(X+200))
    ez=add("#X obj %d 6160 == 0;"%(X+200))
    c(rp2,0,tpe,0)
    c(tpe,1,spt,1)
    c(tpe,0,ez,0); c(ez,0,spa,1)
# --- lane shift engines (rotate with wraparound via temp array) ---
add("#N canvas 0 0 200 140 (subpatch) 0;\n#X array \\$0-sq-shtmp 16 float 0;\n#X coords 0 127 16 0 140 60 1;\n#X restore 12000 4900 graph;")
def _emit_shift(key,arr,wpre,X):
    rsh=add("#X obj %d 5000 r \\$0-sq-sh-%s;"%(X,key))
    up=add("#X obj %d 5030 unpack f f;"%X)
    dadd=add("#X obj %d 5230 + 0;"%(X+140))
    tv=add("#X obj %d 5060 t b b b b b f f;"%X)
    sub1=add("#X obj %d 5090 - 1;"%(X+280))
    mul16=add("#X obj %d 5120 * 16;"%(X+280))
    badd=add("#X obj %d 5300 + 0;"%(X+340))
    mka=add("#X obj %d 5090 makefilename \\$0-sq-%s-%%d;"%(X+200,arr))
    msa=add("#X msg %d 5120 set \\$1;"%(X+200))
    m0a=add("#X msg %d 5150 0;"%X)
    m16a=add("#X msg %d 5150 16;"%(X+40))
    unta=add("#X obj %d 5180 until;"%(X+40))
    fa=add("#X obj %d 5210 f;"%X)
    ta=add("#X obj %d 5240 t f f f;"%X)
    inca=add("#X obj %d 5270 + 1;"%(X+40))
    a16=add("#X obj %d 5260 + 16;"%(X+140))
    amod=add("#X obj %d 5290 mod 16;"%(X+140))
    tra=add("#X obj %d 5320 tabread \\$0-sq-%s-1;"%(X+140,arr))
    pka=add("#X obj %d 5350 pack f f;"%X)
    mpa=add("#X msg %d 5380 \\$1 \\$2;"%X)
    stmp=add("#X obj %d 5410 s \\$0-sq-shtmp;"%X)
    m0b=add("#X msg %d 5150 0;"%(X+300))
    m16b=add("#X msg %d 5150 16;"%(X+340))
    untb=add("#X obj %d 5180 until;"%(X+340))
    fb=add("#X obj %d 5210 f;"%(X+300))
    tb3=add("#X obj %d 5240 t f f f;"%(X+300))
    incb=add("#X obj %d 5270 + 1;"%(X+340))
    mkb=add("#X obj %d 5330 makefilename \\$0-r-sq-%s-%%d;"%(X+340,wpre))
    trb=add("#X obj %d 5330 tabread \\$0-sq-shtmp;"%(X+300))
    sdb=add("#X obj %d 5400 s;"%(X+300))
    srd=add("#X obj %d 5090 s \\$0-redraw;"%(X+80))
    c(rsh,0,up,0)
    c(up,1,dadd,1)
    c(up,0,tv,0)
    c(tv,6,sub1,0); c(sub1,0,mul16,0); c(mul16,0,badd,1)
    c(tv,5,mka,0); c(mka,0,msa,0); c(msa,0,tra,0)
    c(tv,4,m0a,0); c(m0a,0,fa,1)
    c(tv,3,m16a,0); c(m16a,0,unta,0); c(unta,0,fa,0)
    c(tv,2,m0b,0); c(m0b,0,fb,1)
    c(tv,1,m16b,0); c(m16b,0,untb,0); c(untb,0,fb,0)
    c(tv,0,srd,0)
    c(fa,0,ta,0)
    c(ta,2,dadd,0); c(dadd,0,a16,0); c(a16,0,amod,0); c(amod,0,tra,0); c(tra,0,pka,1)
    c(ta,1,pka,0); c(pka,0,mpa,0); c(mpa,0,stmp,0)
    c(ta,0,inca,0); c(inca,0,fa,1)
    c(fb,0,tb3,0)
    c(tb3,2,badd,0); c(badd,0,mkb,0); c(mkb,0,sdb,1)
    c(tb3,1,trb,0); c(trb,0,sdb,0)
    c(tb3,0,incb,0); c(incb,0,fb,1)
_SHENG=(("t","seq","t"),("p","pit","p"),("f","fcut","fc"),("f","ftrg","ft"),("m","mval","mv"),("m2","m2val","m2v"))
for _i,(_k,_a,_w) in enumerate(_SHENG):
    _emit_shift(_k,_a,_w,12000+_i*500)
_ARWIRE=(("t","tsl","tsr"),("p","psl","psr"),("f","fsl","fsr"),("m","msl","msr"),("m2","m2sl","m2sr"))
for _j,(_k,_lsuf,_rsuf) in enumerate(_ARWIRE):
    _ssh=add("#X obj %d 5500 s \\$0-sq-sh-%s;"%(12000+_j*500,_k))
    for v in range(1,9):
        _ml=add("#X msg %d %d %d 1;"%(12000+_j*500,5530+v*30,v))
        c(wid("r-sq-%s-%d"%(_lsuf,v)),0,_ml,0); c(_ml,0,_ssh,0)
        _mr=add("#X msg %d %d %d -1;"%(12200+_j*500,5530+v*30,v))
        c(wid("r-sq-%s-%d"%(_rsuf,v)),0,_mr,0); c(_mr,0,_ssh,0)
# --- env amount control for filter envelopes ---
lb_famt=add("#X obj 15200 4900 loadbang;")
m1_famt=add("#X msg 15200 4930 1;")
c(lb_famt,0,m1_famt,0)
for _v in range(1,9):
    _rf=add("#X obj %d 5000 r \\$0-s-sq-famt-%d;"%(15200+(_v-1)*140,_v))
    _df=add("#X obj %d 5030 / 127;"%(15200+(_v-1)*140))
    _mf=add("#X msg %d 5060 \\$1 20;"%(15200+(_v-1)*140))
    _lf=add("#X obj %d 5090 line~;"%(15200+(_v-1)*140))
    c(_rf,0,_df,0); c(_df,0,_mf,0); c(_mf,0,_lf,0)
    c(m1_famt,0,_lf,0)
    c(_lf,0,famt_targets[_v-1],1)
# --- RND_ALL also randomizes envelope controls ---
_rta=add("#X obj 16800 5000 r \\$0-s-sq-trna;")
for _i,(_pn,_v) in enumerate([(p,v) for p in ("a","d","su","re") for v in range(1,9)]):
    _rd=add("#X obj %d %d random 128;"%(16800+(_i%8)*90,5030+(_i//8)*60))
    _sd=add("#X obj %d %d s \\$0-r-sq-%s-%d;"%(16800+(_i%8)*90,5060+(_i//8)*60,_pn,_v))
    c(_rta,0,_rd,0); c(_rd,0,_sd,0)
_rfa=add("#X obj 18000 5000 r \\$0-s-sq-frna;")
for _i,(_pn,_v) in enumerate([(p,v) for p in ("fa","fd","fsu","fre","famt") for v in range(1,9)]):
    _rd=add("#X obj %d %d random 128;"%(18000+(_i%8)*90,5030+(_i//8)*60))
    _sd=add("#X obj %d %d s \\$0-r-sq-%s-%d;"%(18000+(_i%8)*90,5060+(_i//8)*60,_pn,_v))
    c(_rfa,0,_rd,0); c(_rd,0,_sd,0)
# --- scalar state array + mirrors + refresh system ---
SCAL=[]
for grp,dflt in (("a",11),("d",44),("su",89),("re",49),("m",0),("pe",0),("fa",11),("fd",49),("fsu",64),("fre",49),("fe",0),("rt",64),("rp",64),("rf",64),("me",0),("rm",64)):
    for v in range(1,9): SCAL.append(("%s-%d"%(grp,v),dflt))
PANEL=[("cut-%d"%v,127) for v in range(1,9)]+[("res-%d"%v,0) for v in range(1,9)]
EXTRA=[("sq-m2e-%d"%v,0) for v in range(1,9)]+[("sq-rm2-%d"%v,64) for v in range(1,9)]+[("vib-speed",76),("vib-sync",0)]+[("sq-famt-%d"%v,127) for v in range(1,9)]+[("sq-menv",0)]+[("iso-%d"%v,0) for v in range(1,9)]+[("reset-lfo",0)]
# --- global seq randomize / seq init / front combo engines ---
r_arna=add("#X obj 30000 5000 r \\$0-s-sq-arna;")
t_arna=add("#X obj 30000 5030 t b b b b b;")
c(r_arna,0,t_arna,0)
for _i,_nm in enumerate(("trna","rna","frna","mrna","m2rna")):
    _sx=add("#X obj %d 5060 s \\$0-s-sq-%s;"%(30000+_i*130,_nm))
    c(t_arna,_i,_sx,0)
for _i,_tg in enumerate(["%s-%d"%(_g,_v) for _g in ("m","pe","fe","me","m2e") for _v in range(1,9)]):
    _rd=add("#X obj %d %d random 2;"%(34400+(_i%8)*100,5000+(_i//8)*60))
    _sd=add("#X obj %d %d s \\$0-r-sq-%s;"%(34400+(_i%8)*100,5030+(_i//8)*60,_tg))
    c(r_arna,0,_rd,0); c(_rd,0,_sd,0)
r_aini=add("#X obj 31000 5000 r \\$0-s-sq-aini;")
t_aini=add("#X obj 31000 5030 t b b;")
c(r_aini,0,t_aini,0)
s_rfsh=add("#X obj 31000 5800 s \\$0-sq-refresh;")
c(t_aini,0,s_rfsh,0)
_LDEF=[("seq",[0]*16),("pit",[64]*16),("fcut",[127]*16),("ftrg",[0]*16),("mval",[0]*16)]
_k=0
for _arr,_dv in _LDEF:
    for _v in range(1,9):
        _mm=add("#X msg %d %d 0 %s;"%(31000+(_k%8)*160,5060+(_k//8)*50," ".join(str(x) for x in _dv)))
        _ss=add("#X obj %d %d s \\$0-sq-%s-%d;"%(31000+(_k%8)*160,5090+(_k//8)*50,_arr,_v))
        c(t_aini,1,_mm,0); c(_mm,0,_ss,0); _k+=1
for _v in range(1,9):
    _dv=[_M2DEF[_v-1]]*16
    _mm=add("#X msg %d %d 0 %s;"%(31000+(_k%8)*160,5060+(_k//8)*50," ".join(str(x) for x in _dv)))
    _ss=add("#X obj %d %d s \\$0-sq-m2val-%d;"%(31000+(_k%8)*160,5090+(_k//8)*50,_v))
    c(t_aini,1,_mm,0); c(_mm,0,_ss,0); _k+=1
s_scw=add("#X obj 32600 5000 s \\$0-sq-scal;")
for _st,_vals in ((0,[d for _,d in SCAL]),(144,[d for _,d in EXTRA[0:16]]),(162,[d for _,d in EXTRA[18:27]])):
    _mm=add("#X msg %d %d %d %s;"%(32600,5060+_st,_st," ".join(str(x) for x in _vals)))
    c(t_aini,1,_mm,0); c(_mm,0,s_scw,0)
r_fral=add("#X obj 33400 5000 r \\$0-s-sq-fral;")
t_fral=add("#X obj 33400 5030 t b b;")
s_fr1=add("#X obj 33400 5060 s lira8rand;")
s_fr2=add("#X obj 33500 5060 s \\$0-s-sq-arna;")
c(r_fral,0,t_fral,0); c(t_fral,1,s_fr1,0); c(t_fral,0,s_fr2,0)
r_new=add("#X obj 34000 5000 r lira8_new_preset;")
t_new=add("#X obj 34000 5030 t b b;")
m_nsym=add("#X msg 34100 5060 symbol;")
s_nnam=add("#X obj 34100 5090 s lira8_preset_name;")
s_nini=add("#X obj 34000 5060 s \\$0-s-sq-fial;")
c(r_new,0,t_new,0); c(t_new,1,s_nini,0)
c(t_new,0,m_nsym,0); c(m_nsym,0,s_nnam,0)
r_fial=add("#X obj 33700 5000 r \\$0-s-sq-fial;")
t_fial=add("#X obj 33700 5030 t b b;")
s_fi1=add("#X obj 33700 5060 s lira8init;")
s_fi2=add("#X obj 33800 5060 s \\$0-s-sq-aini;")
c(r_fial,0,t_fial,0); c(t_fial,1,s_fi1,0); c(t_fial,0,s_fi2,0)
add("#N canvas 0 0 200 140 (subpatch) 0;\n#X array \\$0-sq-scal 180 float 3;\n#A 0 "+" ".join(str(d) for _,d in SCAL+PANEL+EXTRA)+";\n#X coords 0 127 112 0 200 60 1;\n#X restore 9000 1300 graph;")
s_scal=add("#X obj 9000 1380 s \\$0-sq-scal;")
for slot,(suf,_) in enumerate(SCAL):
    mm=add("#X msg %d %d %d \\$1;"%(9000+(slot%8)*70,1420+(slot//8)*24,slot))
    c(wid("r-sq-"+suf),0,mm,0); c(mm,0,s_scal,0)
for slot2,(suf,_) in enumerate(PANEL):
    rrp=add("#X obj %d %d r \\$0-s-%s;"%(9600+(slot2%8)*70,1420+(slot2//8)*24,suf))
    mmp=add("#X msg %d %d %d \\$1;"%(9600+(slot2%8)*70,1450+(slot2//8)*24,len(SCAL)+slot2))
    c(rrp,0,mmp,0); c(mmp,0,s_scal,0)
for slot3,(suf,_) in enumerate(EXTRA):
    base3=len(SCAL)+len(PANEL)+slot3
    if suf.startswith("sq-"):
        mmx=add("#X msg %d %d %d \\$1;"%(9600+(slot3%8)*70,1700+(slot3//8)*24,base3))
        c(wid("r-"+suf),0,mmx,0); c(mmx,0,s_scal,0)
    else:
        rrx=add("#X obj %d %d r \\$0-s-%s;"%(9600+(slot3%8)*70,1700+(slot3//8)*24,suf))
        mmx=add("#X msg %d %d %d \\$1;"%(9600+(slot3%8)*70,1730+(slot3//8)*24,base3))
        c(rrx,0,mmx,0); c(mmx,0,s_scal,0)
add("#X obj 9000 4560 text define -k \\$0-sq-scalmap;\n#A set "+" \; ".join(["r-sq-"+s for s,_ in SCAL]+["r-"+s for s,_ in PANEL]+["r-"+s if not s.startswith("sq-") else "r-"+s for s,_ in EXTRA])+";")
# rate slider -> shared processor
s_rtp=add("#X obj 9000 4620 s \\$0-sq-rtproc;")
for uidx,suf in enumerate(["rt-%d"%v for v in range(1,9)]+["rp-%d"%v for v in range(1,9)]+["rf-%d"%v for v in range(1,9)]+["rm-%d"%v for v in range(1,9)]+["rm2-%d"%v for v in range(1,9)]):
    mm=add("#X msg %d %d %d \\$1;"%(9800+(uidx%8)*70,4620+(uidx//8)*26,uidx))
    c(wid("r-sq-"+suf),0,mm,0); c(mm,0,s_rtp,0)
# refresh: scalars + 4 step classes + redraw
r_rf=add("#X obj 10500 1300 r \\$0-sq-refresh;")
t_rf=add("#X obj 10500 1330 t b b b b b b b b;")
c(r_rf,0,t_rf,0)
c(t_rf,0,srdw,0)
m0s=add("#X msg 10500 1360 0;")
mNs=add("#X msg 10560 1360 180;")
unts=add("#X obj 10560 1390 until;")
cnts=add("#X obj 10500 1420 f;")
incs=add("#X obj 10560 1420 + 1;")
tcs=add("#X obj 10500 1450 t f f f;")
tgs=add("#X obj 10560 1480 text get \\$0-sq-scalmap;")
mks=add("#X obj 10560 1510 makefilename \\$0-%s;")
sd7=add("#X obj 10500 1600 s;")
trs=add("#X obj 10500 1510 tabread \\$0-sq-scal;")
c(t_rf,7,m0s,0); c(m0s,0,cnts,1)
c(t_rf,7,mNs,0); c(mNs,0,unts,0); c(unts,0,cnts,0)
c(cnts,0,tcs,0); c(tcs,2,incs,0); c(incs,0,cnts,1)
c(tcs,1,tgs,0); c(tgs,0,mks,0); c(mks,0,sd7,1)
c(tcs,0,trs,0); c(trs,0,sd7,0)
for k,(arr,wpre,outn) in enumerate((("seq","t",6),("pit","p",5),("fcut","fc",4),("ftrg","ft",3),("mval","mv",2),("m2val","m2v",1))):
    Y=1700+k*400
    m0c2=add("#X msg 10500 %d 0;"%Y)
    mNc2=add("#X msg 10560 %d 128;"%Y)
    untc2=add("#X obj 10560 %d until;"%(Y+30))
    cntc2=add("#X obj 10500 %d f;"%(Y+60))
    incc2=add("#X obj 10560 %d + 1;"%(Y+60))
    tcc2=add("#X obj 10500 %d t f f f f;"%(Y+90))
    d16c=add("#X obj 10620 %d / 16;"%(Y+120))
    i16c=add("#X obj 10620 %d i;"%(Y+150))
    p1c=add("#X obj 10620 %d + 1;"%(Y+180))
    mkac=add("#X obj 10620 %d makefilename \\$0-sq-%s-%%d;"%(Y+210,arr))
    msc=add("#X msg 10620 %d set \\$1;"%(Y+240))
    md16c=add("#X obj 10560 %d mod 16;"%(Y+270))
    trc2=add("#X obj 10560 %d tabread \\$0-sq-%s-1;"%(Y+300,arr))
    mktc=add("#X obj 10680 %d makefilename \\$0-r-sq-%s-%%d;"%(Y+270,wpre))
    sd8=add("#X obj 10500 %d s;"%(Y+330))
    c(t_rf,outn,m0c2,0); c(m0c2,0,cntc2,1)
    c(t_rf,outn,mNc2,0); c(mNc2,0,untc2,0); c(untc2,0,cntc2,0)
    c(cntc2,0,tcc2,0); c(tcc2,3,incc2,0); c(incc2,0,cntc2,1)
    c(tcc2,2,d16c,0); c(d16c,0,i16c,0); c(i16c,0,p1c,0); c(p1c,0,mkac,0); c(mkac,0,msc,0); c(msc,0,trc2,0)
    c(tcc2,1,mktc,0); c(mktc,0,sd8,1)
    c(tcc2,0,md16c,0); c(md16c,0,trc2,0); c(trc2,0,sd8,0)
# loadbang: init all widgets from arrays
lb2=add("#X obj 10500 1250 loadbang;")
dl2=add("#X obj 10560 1250 del 400;")
sr2=add("#X obj 10620 1250 s \\$0-sq-refresh;")
c(lb2,0,dl2,0); c(dl2,0,sr2,0)

block="\n".join(objs)+"\n"+"\n".join("#X connect %d %d %d %d;"%t for t in conns)+"\n"
anchor="#X coords 0 -1 1 1 900 760 2 -1 0;"
assert p.count(anchor)==1
p=p.replace(anchor,block+anchor)
open('work.pd','w').write(p)
print("v4:",len(objs),"objs,",len(conns),"conns, mains:",len(mains),"tableN:",N)
