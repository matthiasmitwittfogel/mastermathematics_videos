"""English JPG covers; deterministic drawings derived from the scene sources.

Run with --repo and --studio. No video/audio rendering or network access.
"""
import argparse
import ast
import hashlib
import importlib.util
import json
import math
import sys
import tempfile
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageChops

NAVY = '#0B1020'
WHITE = '#EDF2FA'
GOLD = '#FFD166'
BLUE = '#528BFF'
TEAL = '#49DDBA'
RED = '#F37385'
MUTED = '#A6B7CF'
COLORS = [BLUE, TEAL, GOLD, RED, '#AE91EF']
ROOT = None
REGULAR = None
BOLD = None
WORK = None

# Copy is editorial; equations, arrays and geometric constants are source-bound.
SPECS = [
 ('20230905_apple_logo', ['Apple logo', 'with math'], 'Curves become an icon', 'HOW IS IT DRAWN?', 'apple'),
 ('20230907_sum_from_1_to_n', ['Add them', 'all up'], 'From 1 all the way to n', 'CAN YOU FIND THE SUM?', 'sum'),
 ('20230907_sum_from_1_over_2_to_1_over_64', ['Six terms', 'one square'], 'A finite geometric series', 'WHAT IS THE TOTAL?', 'finite'),
 ('20230909_a_plus_b_square', ['A square', 'of a sum'], 'Algebra you can see', 'HOW DOES IT EXPAND?', 'square2'),
 ('20230910_difference_of_squares', ['Difference', 'of squares'], 'Two squares. One identity.', 'CAN YOU FACTOR IT?', 'difference'),
 ('20230913_find_shaded_area', ['Find the', 'blue area'], 'A quarter-circle puzzle', 'TWO RIGHT ANGLES', 'shaded'),
 ('20230916_bubble_sort_algorithm', ['Bubble', 'sort'], 'Follow the adjacent swaps', 'HOW DO THE BARS SORT?', 'sort'),
 ('20230919_circle_area', ['Area of', 'a circle'], 'A radius. A familiar shape.', 'WHY THIS AREA FORMULA?', 'circle'),
 ('20230925_sum_from_1_to_2n_1', ['Adding', 'odd numbers'], 'The first n odd numbers', 'WHAT IS THE PATTERN?', 'odd'),
 ('20230927_sum_1_to_n_to_1', ['Up to n', 'back to one'], 'A symmetric sum', 'CAN YOU FIND THE TOTAL?', 'symmetric'),
 ('20231001_febonacci_square_sum', ['Fibonacci', 'squares'], 'From 1 squared to 89 squared', 'CAN YOU ADD THE AREAS?', 'fibonacci'),
 ('20231003_series_sum_from_one_over8', ['An endless', 'sum'], 'Start at one eighth', 'WHERE DOES IT END?', 'eighth'),
 ('20231008_a_plus_b__plus_c_square', ['Three terms', 'one square'], 'See the algebra in an area', 'HOW DOES IT EXPAND?', 'square3'),
 ('20231008_insertion_sort_animation', ['Insertion', 'sort'], 'Build order one item at a time', 'WHERE DOES EACH ITEM GO?', 'sort'),
 ('20231010_selection_sort', ['Selection', 'sort'], 'Find the next smallest item', 'WHICH BAR COMES NEXT?', 'sort'),
 ('20231021_infinite_series_from_1_over_2', ['Half, then', 'half again'], 'An infinite geometric series', 'WHAT IS THE TOTAL?', 'half'),
 ('20231025_1_over_3_series', ['Thirds', 'forever'], 'An infinite geometric series', 'WHAT IS THE TOTAL?', 'third'),
 ('20231031_bytedance_logo', ['TikTok logo', 'with math'], 'Circles, lines and color', 'HOW IS IT CONSTRUCTED?', 'tiktok'),
 ('20240416_mirror_equation', ['Mirror', 'equations'], 'Reverse the digits. Look again.', 'DOES THE PATTERN CONTINUE?', 'mirror'),
 ('20231025_express_love_with_formulas', ['Can math', 'say LOVE?'], 'Expressing love with formulas', 'Five curves. One message.', 'love'),
 ('20231104_cube_sum', ['Sum of', 'all cubes?'], 'The sum of cubes', 'From 1 cubed to n cubed', 'cubes'),
 ('20231107_china_flag', ['How to', 'place stars?'], 'Geometry of the Chinese flag', 'A 3:2 rectangle', 'flag'),
 ('20240416_bubble_sort', ['Smarter', 'bubble sort'], 'The optimized algorithm', 'WHEN CAN THE SORT STOP?', 'sort'),
]


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def source_info(path):
    tree = ast.parse(path.read_text(encoding='utf-8-sig'))
    strings, arrays, constants = [], {}, {}
    for node in sorted(ast.walk(tree), key=lambda item: getattr(item, 'lineno', 0)):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == 'MathTex':
            text = ''.join(a.value for a in node.args if isinstance(a, ast.Constant) and isinstance(a.value, str))
            if text:
                strings.append(text)
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    try:
                        val = ast.literal_eval(node.value)
                    except (ValueError, TypeError):
                        continue
                    if isinstance(val, list) and val and all(isinstance(v, (float, int)) for v in val):
                        arrays[target.id] = val
                    if isinstance(val, (int, float, str)):
                        constants[target.id] = val
    return {'mathtex': strings, 'arrays': arrays, 'constants': constants}


def txt(draw, xy, value, size=72, color=WHITE, bold=False, anchor='mm'):
    font = ImageFont.truetype(str(BOLD if bold else REGULAR), size)
    draw.text(xy, value, fill=color, font=font, anchor=anchor)


def formula(image, tex, xy, width=1450, height=210, color=WHITE):
    """Render actual LaTeX with Manim MathTex at native diagram resolution."""
    from manim import MathTex, config
    from manim.camera.camera import Camera
    config.media_dir = str(WORK / 'tex')
    config.tex_dir = str(WORK / 'tex' / 'Tex')
    Path(config.tex_dir).mkdir(parents=True, exist_ok=True)
    mob = MathTex(tex, color=color, font_size=90)
    ratio = (mob.width + .2) / (mob.height + .2)
    w = min(width, round(height * ratio))
    h = min(height, round(width / ratio))
    cam = Camera(pixel_width=max(1, w), pixel_height=max(1, h),
                 frame_width=mob.width + .2, frame_height=mob.height + .2,
                 background_color=NAVY)
    cam.capture_mobjects([mob])
    tile = Image.fromarray(cam.pixel_array).convert('RGB')
    image.paste(tile, (round(xy[0] - w / 2), round(xy[1] - h / 2)))


def poly(draw, points, fill=None, outline=WHITE, width=7):
    if fill:
        draw.polygon(points, fill=fill)
    draw.line(points + [points[0]], fill=outline, width=width, joint='curve')


def diagram(entry):
    im = Image.new('RGB', (1720, 1640), NAVY)
    d = ImageDraw.Draw(im)
    kind, info = entry['kind'], entry['source_info']
    # Initial equation is selected from real MathTex nodes, never from file names.
    eqs = info['mathtex']
    if kind in ('sum','finite','square2','odd','symmetric','fibonacci','eighth','square3','half','third','cubes'):
        if kind == 'square2':
            eq = next(t for t in eqs if '(a+b)' in t)
        elif kind == 'square3':
            eq = next(t for t in eqs if '(a+b+c)' in t) + '=?'
        elif kind == 'cubes':
            eq = eqs[0] + '=?'
        elif kind == 'fibonacci':
            assert '89^2' in eqs[0]
            eq = r'1^2+1^2+2^2+\cdots+89^2=?'
        else:
            eq = eqs[0].replace('...', r'\cdots')
            if '?' not in eq:
                eq += '=?'
        # Preserve endpoints while shortening long source expressions for mobile reading.
        compact = {
            'sum': r'1+2+\cdots+n=?',
            'finite': r'\frac12+\frac14+\cdots+\frac1{64}=?',
            'symmetric': r'1+2+\cdots+n+\cdots+2+1=?',
            'eighth': r'\frac18+\frac1{16}+\frac1{32}+\cdots=?',
            'half': r'\frac12+\frac14+\frac18+\cdots=?',
            'third': r'\frac13+\frac19+\frac1{27}+\cdots=?',
            'cubes': r'1^3+2^3+\cdots+n^3=?',
        }
        eq=compact.get(kind,eq)
        formula(im, eq, (860,160), height=190)
    if kind in ('square2','square3'):
        sides = [6,4] if kind == 'square2' else [3,3,2]
        labels = ['a','b','c']
        if kind == 'square2':
            assert info['constants'].get('OPACITY_VAL') is not None or 'a^2' in ''.join(eqs)
        scale = 1000 / sum(sides)
        y = 460
        for j, sj in enumerate(sides):
            x = 360
            for i, si in enumerate(sides):
                poly(d, [(x,y),(x+si*scale,y),(x+si*scale,y+sj*scale),(x,y+sj*scale)], COLORS[(i+j)%len(COLORS)], NAVY, 8)
                x += si*scale
            txt(d, (280,y+sj*scale/2), labels[j], 82, GOLD)
            y += sj*scale
        x=360
        for i, si in enumerate(sides):
            txt(d,(x+si*scale/2,390),labels[i],82,GOLD)
            x+=si*scale
    elif kind == 'difference':
        formula(im,r'a^2-b^2=?',(860,170),height=200)
        # Source square sides 8 and 3: keep exact 8:3 ratio.
        poly(d,[(340,440),(1380,440),(1380,1480),(340,1480)],BLUE)
        poly(d,[(340,440),(730,440),(730,830),(340,830)],NAVY,GOLD,9)
        txt(d,(860,375),'a',90,GOLD)
        txt(d,(535,875),'b',90,GOLD)
        txt(d,(1020,1110),'?',210,WHITE,True)
    elif kind in ('sum','odd','symmetric','cubes'):
        # Initial stacks of terms, without the final rearrangement/answer.
        n=7 if kind!='cubes' else 5
        unit=115 if kind!='symmetric' else 90
        rows=list(range(1,n+1))
        if kind=='symmetric': rows=[1,2,3,4,5,6,5,4,3,2,1]; unit=91
        if kind=='odd':
            for k in range(6):
                x0,y0=430,550
                for i in range(k+1):
                    d.rectangle((x0+i*145,y0+k*145,x0+(i+1)*145-5,y0+(k+1)*145-5),fill=COLORS[k%5])
                for j in range(k):
                    d.rectangle((x0+k*145,y0+j*145,x0+(k+1)*145-5,y0+(j+1)*145-5),fill=COLORS[k%5])
            txt(d,(860,430),'1, 3, 5, ...',80,GOLD)
        elif kind=='cubes':
            # Term areas k^3 represented by k squares of side k.
            y=440
            for k in range(1,5):
                side=k*54
                for j in range(k):
                    d.rectangle((400+j*(side+9),y,400+j*(side+9)+side,y+side),fill=COLORS[k-1],outline=WHITE,width=3)
                txt(d,(280,y+side/2),f'{k}³',70,GOLD)
                y+=side+65
        else:
            total=len(rows)*unit
            y=440+(1040-total)/2
            for row,k in enumerate(rows):
                x=500 if kind=='symmetric' else 420
                for j in range(k):
                    d.rectangle((x+j*unit,y,x+(j+1)*unit-5,y+unit-5),fill=COLORS[row%5])
                if kind!='symmetric': txt(d,(325,y+unit/2),str(k),60,GOLD)
                y+=unit
    elif kind=='finite':
        # Alternating bisections of the source unit square; final 1/64 uncolored.
        box=[330,450,1390,1510]
        for k in range(6):
            x,y,r,b=box
            if k%2==0:
                mid=(x+r)/2; region=(x,y,mid,b); box=[mid,y,r,b]
            else:
                mid=(y+b)/2; region=(x,y,r,mid); box=[x,mid,r,b]
            d.rectangle(region,fill=COLORS[k%5],outline=NAVY,width=5)
            if k<4:
                txt(d,((region[0]+region[2])/2,(region[1]+region[3])/2),f'1/{2**(k+1)}',72 if k<2 else 54,WHITE,True)
        d.rectangle((330,450,1390,1510),outline=WHITE,width=7)
        txt(d,(860,375),'1',80,GOLD)
    elif kind=='eighth':
        # Source uses successive 45-degree rotations with scale 1/sqrt(2).
        center=np.array([860,1000]); pts=np.array([[-490,-490],[490,-490],[490,490],[-490,490]])
        for k in range(7):
            poly(d,[tuple(p) for p in pts+center],None,COLORS[k%5],7)
            pts=np.array([(pts[i]+pts[(i+1)%4])/2 for i in range(4)])
        txt(d,(860,410),'A unit square',72,GOLD)
    elif kind=='third':
        # Source starts with thirds and then recursively partitions the remainder.
        side=1060; x=330; y=450
        d.rectangle((x,y,x+side/3,y+side),fill=BLUE)
        d.rectangle((x+side/3,y,x+2*side/3,y+side/3),fill=TEAL)
        d.rectangle((x+2*side/3,y,x+2*side/3+side/9,y+side/3),fill=GOLD)
        d.rectangle((x,y,x+side,y+side),outline=WHITE,width=7)
        txt(d,(505,980),'1/3',83,WHITE,True)
        txt(d,(860,625),'1/9',70,NAVY,True)
        txt(d,(860,390),'Divide into thirds',72,GOLD)
    elif kind=='half':
        # Initial source triangle (right isosceles), no proof slices on the cover.
        poly(d,[(390,1450),(1390,1450),(390,450)],'#1D3D78',WHITE,9)
        formula(im,r'\sqrt{2}',(860,1540),width=300,height=100,color=GOLD)
        formula(im,r'\sqrt{2}',(230,950),width=270,height=100,color=GOLD)
        txt(d,(955,905),'2',92,GOLD)
        txt(d,(695,1140),'?',190,WHITE,True)
    elif kind=='fibonacci':
        # Source places successive squares to the right, then below the bounding box.
        rects=[(0,0,1,1),(0,1,1,1)]
        x0,y0,x1,y1=0,0,1,2
        for idx,s in enumerate([2,3,5,8,13,21]):
            if idx%2==0: r=(x1,y0,s,s); x1+=s
            else: r=(x0,y1,s,s); y1+=s
            rects.append(r)
        scale=min(1280/x1,1060/y1); ox=860-x1*scale/2; oy=460
        for k,(x,y,w,h) in enumerate(rects):
            d.rectangle((ox+x*scale,oy+y*scale,ox+(x+w)*scale,oy+(y+h)*scale),fill=COLORS[k%5],outline=NAVY,width=6)
            if w>=3: txt(d,(ox+(x+w/2)*scale,oy+(y+h/2)*scale),str(w),max(44,round(w*scale*.23)),NAVY,True)
    elif kind=='circle':
        formula(im,r'A=?',(860,170),height=190)
        d.ellipse((340,400,1380,1440),fill='#183467',outline=BLUE,width=12)
        d.line((860,920,1380,920),fill=GOLD,width=10)
        d.ellipse((844,904,876,936),fill=WHITE)
        txt(d,(1120,845),'r',110,GOLD)
        txt(d,(815,985),'O',62,WHITE)
    elif kind=='shaded':
        # Exact displayed constraints: C lies on x²+y²=16 and x+y=16/3.
        r=4.; a=3.; total=r*r/a; delta=math.sqrt(2*r*r-total*total)
        cx,cy=(total+delta)/2,(total-delta)/2
        assert abs(cx*cx+cy*cy-16)<1e-9
        assert abs(cx*(cx-3)+cy*(cy-3))<1e-9
        def p(x,y): return (350+x*250,1420-y*250)
        arc=[p(r*math.cos(t),r*math.sin(t)) for t in np.linspace(0,math.pi/2,200)]
        poly(d,[p(0,0)]+arc,BLUE,WHITE,8)
        poly(d,[p(0,0),p(0,a),p(cx,cy),p(a,0)],NAVY,WHITE,8)
        for v,label,off in [((0,0),'O',(-55,55)),((0,3),'A',(-60,0)),((3,0),'B',(0,65)),((cx,cy),'C',(60,-20))]:
            q=p(*v); txt(d,(q[0]+off[0],q[1]+off[1]),label,73,GOLD,True)
        d.line([p(0,.25),p(.25,.25),p(.25,0)],fill=GOLD,width=6)
        u=np.array([-cx,3-cy]); v=np.array([3-cx,-cy]); u=u/np.linalg.norm(u)*.25; v=v/np.linalg.norm(v)*.25
        d.line([p(cx+u[0],cy+u[1]),p(cx+u[0]+v[0],cy+u[1]+v[1]),p(cx+v[0],cy+v[1])],fill=GOLD,width=6)
        formula(im,r'r=4,\quad OA=OB=3',(860,180),height=150)
        txt(d,(885,655),'?',160,WHITE,True)
    elif kind=='sort':
        values=info['arrays'].get('VALUES',info['arrays'].get('values'))
        assert values==[10,8,2,9,1,6,3,5,7,4]
        for i,value in enumerate(values):
            y=240+i*123
            fill=GOLD if i in (0,1) else BLUE
            d.rounded_rectangle((390,y,390+value*100,y+86),radius=13,fill=fill)
            txt(d,(295,y+43),str(value),75,WHITE,True)
        d.line((1500,257,1500,435),fill=TEAL,width=11)
        poly(d,[(1480,410),(1500,440),(1520,410)],TEAL,TEAL,4)
    elif kind=='mirror':
        d.line((860,250,860,1450),fill=TEAL,width=7)
        pairs=[(r'12^2=144',r'441=21^2'),(r'13^2=169',r'961=31^2'),(r'102^2=10404',r'40401=201^2')]
        for i,(a,b) in enumerate(pairs):
            source_text=(ROOT/entry['source']).read_text(encoding='utf-8')
            assert a in source_text and b in source_text
            formula(im,a,(420,400+i*370),width=735,height=140)
            formula(im,b,(1290,400+i*370),width=735,height=140,color=GOLD)
    elif kind=='love':
        # Actual plotted functions in loveyou_animation.py (not its typo in formula5).
        def pp(x,y): return (860+x*115,800-y*115)
        for x in np.arange(-7,8): d.line([pp(x,-4),pp(x,5)],fill='#17243B',width=2)
        for y in range(-4,6): d.line([pp(-7,y),pp(7,y)],fill='#17243B',width=2)
        def curve(xs,ys,color=RED): d.line([pp(float(x),float(y)) for x,y in zip(xs,ys)],fill=color,width=14,joint='curve')
        x=np.linspace(-5.75,-4,200); curve(x,1/(x+6))
        t=np.linspace(0,2*math.pi,250); curve(-2+math.sqrt(2)*np.cos(t),2+math.sqrt(2)*np.sin(t),GOLD)
        x=np.linspace(0,2,200); curve(x,np.abs(2*x-2)+1,TEAL)
        y=np.linspace(1,3,250); curve(6-3*np.sin(np.abs(3*(y-2))),y,BLUE)
        x=np.linspace(-1.2,1.2,200); curve(x,x**4-3,RED)
    elif kind=='flag':
        # Grid units: full flag 30 x 20, upper-left star centers (5,5), etc.
        scale=48; ox=140; oy=250
        d.rectangle((ox,oy,ox+30*scale,oy+20*scale),fill='#CD2433')
        for x in range(1,15): d.line((ox+x*scale,oy,ox+x*scale,oy+10*scale),fill='#D64A53',width=2)
        for y in range(1,10): d.line((ox,oy+y*scale,ox+15*scale,oy+y*scale),fill='#D64A53',width=2)
        for x,y,rad in [(5,5,3),(10,8,1),(12,6,1),(12,3,1),(10,1,1)]:
            sx,sy=ox+x*scale,oy+(10-y)*scale
            angle=-math.pi/2 if rad==3 else math.atan2((y-5),5-x)
            pts=[]
            for k in range(10):
                rr=rad*scale*(1 if k%2==0 else (3-math.sqrt(5))/2)
                t=angle+k*math.pi/5; pts.append((sx+rr*math.cos(t),sy+rr*math.sin(t)))
            d.polygon(pts,fill=GOLD)
        txt(d,(860,1320),'3 : 2',140,GOLD,True)
    elif kind=='apple':
        # Numerically evaluate exactly the source curves, avoiding its optional sympy dependency.
        def pp(x,y): return (860+x*119,1450-y*119)
        def curve(x,y): d.line([pp(float(a),float(b)) for a,b in zip(x,y)],fill=WHITE,width=12,joint='curve')
        p=np.polynomial.Polynomial([-2.03,1]); q=.48*p*p+.01
        roots=(np.polynomial.Polynomial([-5.58,1])**2+(q-5.34)**2-6.63).roots()
        x4=next(float(t.real) for t in roots if abs(t.imag)<1e-7 and 0<t.real<6)
        y4=float(q(x4))
        c1=np.array([5.58,5.34]); c2=np.array([1.95,5.56]); delta=c2-c1; dist=np.linalg.norm(delta)
        a=(6.63-9.14+dist**2)/(2*dist); h=math.sqrt(6.63-a*a)
        base=c1+a*delta/dist; normal=np.array([-delta[1],delta[0]])/dist
        point5=max([base+h*normal,base-h*normal],key=lambda pt:pt[1])
        x7=math.sqrt(9.14-(8.577-5.58)**2)+.18-1.95
        y7=.6*math.sin(x7-1.4)+8.7
        x=np.linspace(-2.03,2.03,180); curve(x,np.cos(x)/3+.1577448)
        x=np.linspace(2.03,x4,150); curve(x,.48*(x-2.03)**2+.01)
        y=np.linspace(y4,point5[1],180); curve(5.58-np.sqrt(np.maximum(0,6.63-(y-5.34)**2)),y)
        x=np.linspace(.85,point5[0],180); curve(x,5.56+np.sqrt(np.maximum(0,9.14-(x-1.95)**2)))
        x=np.linspace(x7,.85,100); curve(x,.6*np.sin(x-1.4)+8.7)
        # ArcBetweenPoints is the minor positive-radius arc in the source.
        end=np.array([-4.9,math.sqrt(9.14-(-4.9+1.95)**2)+5.56]); start=np.array([x7,y7])
        chord=end-start; mid=(start+end)/2; length=np.linalg.norm(chord)
        center=mid+np.array([-chord[1],chord[0]])/length*math.sqrt(9.14-length**2/4)
        t0=math.atan2(start[1]-center[1],start[0]-center[0]); t1=math.atan2(end[1]-center[1],end[0]-center[0])
        while t1<t0: t1+=2*math.pi
        t=np.linspace(t0,t1,160); curve(center[0]+math.sqrt(9.14)*np.cos(t),center[1]+math.sqrt(9.14)*np.sin(t))
        y9=-math.sqrt(26.68-(-x4-.16)**2)+5.14
        y=np.linspace(y9,end[1],180); curve(.16-np.sqrt(np.maximum(0,26.68-(y-5.14)**2)),y)
        x=np.linspace(-x4,-2.03,150); curve(x,.48*(x+2.03)**2+.01)
        # Leaf: boundary of intersection of the two source circles.
        for c,r,other,r2 in [(np.array([2.31,8.77]),math.sqrt(6.35),np.array([-.23,11.02]),5.58),(np.array([-.23,11.02]),math.sqrt(5.58),np.array([2.31,8.77]),6.35)]:
            t=np.linspace(0,2*math.pi,1600); points=c+np.c_[np.cos(t),np.sin(t)]*r
            selected=np.sum((points-other)**2,axis=1)<=r2
            run=[]
            for pt,keep in zip(points,selected):
                if keep: run.append(pp(*pt))
                elif run:
                    if len(run)>1:d.line(run,fill=TEAL,width=12)
                    run=[]
            if len(run)>1:d.line(run,fill=TEAL,width=12)
    elif kind=='tiktok':
        # Boolean union from source: annulus minus rectangle + stem + annular corner.
        xx,yy=np.meshgrid(np.linspace(-8,9,1450),np.linspace(9,-10,1450))
        def mask_at(dx,dy):
            x,y=xx-dx,yy-dy
            ring=((x+3)**2+(y+4)**2<=16)&((x+3)**2+(y+4)**2>=4)
            cut=(x>=-2.2)&(x<=-1)&(y>=-4)&(y<=0)
            stem=(np.abs(x)<=1)&(np.abs(y)<=4)
            corner=((x-4)**2+(y-4)**2<=25)&((x-4)**2+(y-4)**2>=9)&(x>=-1)&(x<=4)&(y>=-1)&(y<=4)
            return (ring&~cut)|stem|corner
        redmask=mask_at(2,1); cyanmask=mask_at(1.4,1.6)
        pix=np.zeros((1450,1450,3),dtype=np.uint8); pix[:]=[11,16,32]
        pix[redmask]=[243,50,83]; pix[cyanmask]=[0,235,235]; pix[redmask&cyanmask]=[237,242,250]
        im.paste(Image.fromarray(pix),(135,95))
    return im


def draw_horizontal(draw, box, entry):
    tile=diagram(entry)
    tile.thumbnail((box[2]-box[0],box[3]-box[1]),Image.Resampling.LANCZOS)
    draw._image.paste(tile,(round((box[0]+box[2]-tile.width)/2),round((box[1]+box[3]-tile.height)/2)))


def main():
    global ROOT, REGULAR, BOLD, WORK
    p=argparse.ArgumentParser(); p.add_argument('--repo',type=Path,required=True); p.add_argument('--studio',type=Path,required=True)
    args=p.parse_args(); ROOT=args.repo.resolve(); studio=args.studio.resolve()
    sys.path.insert(0,str(studio/'tools'))
    from runtime_paths import font_path
    from cover_layout import render
    REGULAR=font_path('arial.ttf'); BOLD=font_path('arialbd.ttf')
    horizontal=load_module('studio_horizontal_cover',studio/'template/longform/code/cover.py')
    WORK=ROOT/'work/english_covers'; WORK.mkdir(parents=True,exist_ok=True)
    out=ROOT/'covers'; out.mkdir(exist_ok=True)
    sources=list((ROOT/'shorts').glob('*.py'))+list((ROOT/'videos').glob('*/*.py'))
    entries=[]
    for key,headline,subtitle,prompt,kind in SPECS:
        source=next(s for s in sources if s.stem==key or s.parent.name==key)
        info=source_info(source)
        portrait=source.parent.name=='shorts' or key=='20240416_bubble_sort'
        entry=dict(id=key,source=source.relative_to(ROOT).as_posix(),source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
                   headline=headline,subtitle=subtitle,prompt=prompt,kind=kind,portrait=portrait,source_info=info)
        jpg=out/(key+'.jpg')
        if portrait:
            cfg=dict(headline=headline,subtitle=subtitle,prompt=prompt)
            cover=render(cfg,diagram(entry),REGULAR,BOLD,scale=2)
            cover.save(jpg,quality=96,subsampling=0,optimize=True)
        else:
            with tempfile.TemporaryDirectory(dir=WORK) as td:
                project=Path(td)
                for folder in ['code','script']: (project/folder).mkdir()
                (project/'code/model.py').write_bytes(source.read_bytes())
                (project/'code/cover_diagram.py').write_text('import batch_covers\nimport json\nfrom pathlib import Path\ndef draw_diagram(draw, box, regular):\n    entry=json.loads((Path(__file__).parent/"entry.json").read_text())\n    batch_covers.draw_horizontal(draw,box,entry)\n',encoding='utf-8')
                (project/'code/entry.json').write_text(json.dumps(entry),encoding='utf-8')
                (project/'script/publication.json').write_text(json.dumps({'en':dict(cover_question=headline,cover_topic=subtitle,cover_subtitle=[prompt])}),encoding='utf-8')
                horizontal.build_cover(project,'en')
                jpg.write_bytes((project/'deliverables/cover.jpg').read_bytes())
        with Image.open(jpg) as check:
            assert check.size==((2160,3840) if portrait else (3840,2160))
            check.verify()
        entry['output']=jpg.relative_to(ROOT).as_posix(); entry['output_sha256']=hashlib.sha256(jpg.read_bytes()).hexdigest()
        entry['bytes']=jpg.stat().st_size
        entry['layout']='studio-cover-v1' if portrait else 'studio-long-cover-v5'
        entries.append(entry)
        print(f'BUILT {key} {entry["bytes"]} bytes',flush=True)
    assert len(entries)==len(sources)==23
    manifest=dict(renderer_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                  studio_layout_sha256=hashlib.sha256((studio/'tools/cover_layout.py').read_bytes()).hexdigest(),
                  studio_horizontal_sha256=hashlib.sha256((studio/'template/longform/code/cover.py').read_bytes()).hexdigest(),entries=entries,
                  visual_review='pending',notes=['Only English high-resolution JPGs are delivered.', 'Shaded-area geometry follows displayed OA=OB=3, not the source drawing value 3.1.'])
    (WORK/'manifest.json').write_text(json.dumps(manifest,indent=2),encoding='utf-8')
    print('ALL 23 JPG COVERS GENERATED',flush=True)


if __name__=='__main__':
    sys.modules['batch_covers']=sys.modules[__name__]
    main()
