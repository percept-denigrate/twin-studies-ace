#!/usr/bin/env python3
from pathlib import Path
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

BG = '#0f1117'
SPINE = '#3a3f4b'
FG = '#c9d1d9'
MUTED = '#8b949e'
TITLE = '#e6edf3'
LEFT_COLOR = '#38bdf8'
RIGHT_COLOR = '#f2cc60'
EEA_COLOR = '#f97316'
AM_COLOR = '#a78bfa'
SQRT3_2 = math.sqrt(3) / 2

def to_xy(a, c, e):
    return a + 0.5*c, SQRT3_2*c

def draw_triangle(ax):
    verts = [(0,0),(1,0),(0.5,SQRT3_2),(0,0)]
    xs, ys = zip(*verts)
    ax.plot(xs, ys, color=SPINE, linewidth=1.4, zorder=2)
    for frac in (0.2,0.4,0.6,0.8):
        p1,p2 = to_xy(frac,1-frac,0), to_xy(frac,0,1-frac)
        ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color=SPINE,lw=.6,ls='--',zorder=1)
        p1,p2 = to_xy(1-frac,frac,0), to_xy(0,frac,1-frac)
        ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color=SPINE,lw=.6,ls='--',zorder=1)
        p1,p2 = to_xy(1-frac,0,frac), to_xy(0,1-frac,frac)
        ax.plot([p1[0],p2[0]],[p1[1],p2[1]],color=SPINE,lw=.6,ls=':',zorder=1)
        tx,ty = to_xy(frac,1-frac,0)
        ax.text(tx,ty-.028,str(int(frac*100)),ha='center',va='top',fontsize=7.5,color=MUTED,zorder=3)
    ax.text(-.045,-.032,'Non-shared\nEnvironment',ha='center',va='top',fontsize=12,fontweight='bold',color=LEFT_COLOR)
    ax.text(1.045,-.032,'Genetic',ha='center',va='top',fontsize=12,fontweight='bold',color=RIGHT_COLOR)
    ax.text(.5,SQRT3_2+.028,'Shared\nEnvironment',ha='center',va='bottom',fontsize=12,fontweight='bold',color=FG)

def extend_point(x0,y0,x1,y1,target_length):
    dx,dy = x1-x0,y1-y0
    d = math.hypot(dx,dy)
    if d == 0:
        return x1,y1
    s = target_length/d
    return x0+dx*s, y0+dy*s

def make_plot(output_path):
    fig, ax = plt.subplots(figsize=(12.4,10.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_aspect('equal')
    ax.axis('off')
    draw_triangle(ax)

    A=C=E=1/3
    x0,y0 = to_xy(A,C,E)
    ax.scatter([x0],[y0],s=165,color=FG,edgecolors='#d0d7de',linewidths=1.0,zorder=6)
    ax.text(x0,y0-.060,'"True"\nACE values',ha='center',va='top',fontsize=12,fontweight='bold',color=FG,zorder=7)

    x_values = [0.05,0.10]
    eea_points = [(xv,*to_xy(A+2*xv,C-xv,E-xv)) for xv in x_values]
    r_values = [0.20,0.40]
    am_points = [(rv,*to_xy(A*(1-rv),C+rv*A,E)) for rv in r_values]

    eea_far_x,eea_far_y = eea_points[-1][1],eea_points[-1][2]
    am_far_x,am_far_y = am_points[-1][1],am_points[-1][2]
    eea_len = math.hypot(eea_far_x-x0,eea_far_y-y0)
    am_len = math.hypot(am_far_x-x0,am_far_y-y0)
    eea_tip_x,eea_tip_y = extend_point(x0,y0,eea_far_x,eea_far_y,eea_len*1.5)
    am_tip_x,am_tip_y = extend_point(x0,y0,am_far_x,am_far_y,am_len*1.5)

    ax.annotate('',xy=(eea_tip_x,eea_tip_y),xytext=(x0,y0),arrowprops=dict(arrowstyle='->',lw=2.2,color=EEA_COLOR),zorder=4)
    ax.annotate('',xy=(am_tip_x,am_tip_y),xytext=(x0,y0),arrowprops=dict(arrowstyle='->',lw=2.2,color=AM_COLOR),zorder=4)

    ax.text(eea_tip_x+.045,eea_tip_y-.05,'EEA violation',ha='left',va='center',fontsize=11,color=EEA_COLOR,fontweight='bold',zorder=7)
    ax.text(am_tip_x-.1,am_tip_y+.03,'Assortative mating',ha='left',va='center',fontsize=11,color=AM_COLOR,fontweight='bold',zorder=7)

    for i,(xv,xp,yp) in enumerate(eea_points):
        ax.scatter([xp],[yp],s=95,color=EEA_COLOR,edgecolors='#d0d7de',linewidths=.8,zorder=6)
        if i == 0:
            ax.text(xp+.022,yp+.018,f'x = {xv:.2f}',ha='left',va='center',fontsize=10.5,color=EEA_COLOR,zorder=7)
        else:
            ax.text(xp+.022,yp,f'x = {xv:.2f}',ha='left',va='center',fontsize=10.5,color=EEA_COLOR,zorder=7)

    for i,(rv,xp,yp) in enumerate(am_points):
        ax.scatter([xp],[yp],s=95,color=AM_COLOR,edgecolors='#d0d7de',linewidths=.8,zorder=6)
        ax.text(xp-.115,yp,f'r = {rv:.2f}',ha='left',va='center',fontsize=10.5,color=AM_COLOR,zorder=7)

    ax.set_xlim(-.18,1.18)
    ax.set_ylim(-.14,SQRT3_2+.08)
    fig.suptitle('Bias directions in ACE space',color=TITLE,fontsize=16,fontweight='bold',y=.975)
    fig.text(.99,.01,'antisymmetry.substack.com',ha='right',va='bottom',fontsize=11,color=TITLE)
    fig.tight_layout(rect=[.01,.01,.99,.97])
    fig.savefig(output_path,dpi=180,bbox_inches='tight',facecolor=fig.get_facecolor())
    plt.close(fig)

if __name__ == '__main__':
    make_plot(Path('ace_bias_schematic.png'))
