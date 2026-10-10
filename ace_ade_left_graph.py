#!/usr/bin/env python3
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

BG = '#0f1117'
SPINE = '#3a3f4b'
MUTED = '#8b949e'
TITLE = '#e6edf3'
ACE_FILL = '#60a5fa'
ADE_COLOR = '#f97316'
TITLE_FS = 16
FOOTER_FS = 11
AXIS_LABEL_FS = 11
TICK_FS = 9
POINT_LABEL_FS = 16

def style_axis(ax):
    ax.set_facecolor(BG)
    ax.tick_params(colors=MUTED,labelsize=TICK_FS)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_color(SPINE)
    ax.spines['left'].set_color(SPINE)
    ax.spines['bottom'].set_linewidth(1.1)
    ax.spines['left'].set_linewidth(1.1)

def draw_left_graph(ax):
    style_axis(ax)
    ax.set_xlim(-.12,1.32)
    ax.set_ylim(-.08,1.18)
    ax.set_aspect('equal')
    E=(0.,0.)
    A=(1.,.5)
    C=(1.,1.)
    D=(1.,.25)

    ace_poly = Polygon([E,A,C],closed=True,facecolor=ACE_FILL,edgecolor=ACE_FILL,alpha=.30,lw=2.0,zorder=2)
    ax.add_patch(ace_poly)
    ax.plot([E[0],A[0],C[0],E[0]],[E[1],A[1],C[1],E[1]],color=ACE_FILL,lw=2.0,zorder=3)

    ade_poly = Polygon([E,A,D],closed=True,facecolor=ADE_COLOR,edgecolor=ADE_COLOR,alpha=.22,lw=2.0,zorder=1)
    ax.add_patch(ade_poly)
    ax.plot([E[0],A[0],D[0],E[0]],[E[1],A[1],D[1],E[1]],color=ADE_COLOR,lw=2.0,zorder=4)

    specs=[(E,'E',ACE_FILL,-.08,.06),(A,'A',ACE_FILL,.08,.06),(C,'C',ACE_FILL,-.04,.10),(D,'D',ADE_COLOR,.08,-.02)]
    for (x,y),label,color,dx,dy in specs:
        ax.scatter([x],[y],s=180,color=color,alpha=.28,edgecolors='none',zorder=5,clip_on=False)
        ax.scatter([x],[y],s=45,color=color,edgecolors=color,zorder=6,clip_on=False)
        ax.text(x+dx,y+dy,label,color=color,fontsize=POINT_LABEL_FS,zorder=7)

    ax.set_xticks([0,1])
    ax.set_yticks([0,.25,.5,1.0])
    ax.set_yticklabels(['0','1/4','1/2','1'])
    ax.set_xlabel('rMZ',color=MUTED,fontsize=AXIS_LABEL_FS,labelpad=10)
    ax.set_ylabel('rDZ',color=MUTED,fontsize=AXIS_LABEL_FS,labelpad=10)
    ax.grid(color=SPINE,alpha=.35,lw=.7)
    ax.annotate('',xy=(1.29,0),xytext=(0,0),arrowprops=dict(arrowstyle='-|>',color=SPINE,lw=1.1),annotation_clip=False,zorder=3)
    ax.annotate('',xy=(0,1.15),xytext=(0,0),arrowprops=dict(arrowstyle='-|>',color=SPINE,lw=1.1),annotation_clip=False,zorder=3)

def make_plot(output_path):
    fig,ax = plt.subplots(figsize=(7.2,6.4),facecolor=BG)
    draw_left_graph(ax)
    fig.suptitle('How the ACE and ADE triangles are formed',x=.5,y=.955,ha='center',va='center',color=TITLE,fontsize=TITLE_FS,fontweight='bold')
    fig.text(.985,.025,'antisymmetry.substack.com',ha='right',va='bottom',fontsize=FOOTER_FS,color=TITLE)
    fig.savefig(output_path,dpi=180,facecolor=fig.get_facecolor())
    plt.close(fig)

if __name__ == '__main__':
    make_plot(Path('ace_ade_left_graph.png'))
