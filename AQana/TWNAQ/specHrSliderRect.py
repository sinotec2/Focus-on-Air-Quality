#!/cluster/miniconda/bin/python
# -*- coding: utf-8 -*-
"""plot the hrly time series of pollutant at station(s)
    specHr.py -b 2071231 -e 20180101 -s PM2.5 -a plot -t wanli,xianxi,puzi,xiaogang """
# from __future__ import print_function
import matplotlib.pyplot as plt
from pandas import *
import sys, os, datetime, subprocess
from matplotlib.widgets import CheckButtons, Slider, Button, RectangleSelector


def getarg():
  """ read time period and station name from argument(std input)
  specHr.py -b 2071231 -e 20180101 -s PM2.5 -a plot -t wanli,xianxi,puzi,xiaogang """
  import argparse
  ap = argparse.ArgumentParser()
  ap.add_argument("-t", "--STNAM", required=True, type=str, help="station name,sep by ,")
  ap.add_argument("-s", "--SPNAM", required=True, type=str, help="spec name")
  ap.add_argument("-b", "--BEGD", required=True, type=int, help="yyyymmdd")
  ap.add_argument("-e", "--ENDD", required=True, type=int, help="yyyymmdd")
  ap.add_argument("-a", "--ACTION", required=True, type=str, help="save or plot")
  args = vars(ap.parse_args())
  return [args['STNAM'], args['SPNAM'], args['BEGD'], args['ENDD'], args['ACTION']]


def dt2int(dt):
  a = [int(i) for i in str(dt).split()[0].split('-')]
  return a[0] * 100 * 100 + a[1] * 100 + a[2]


def int2dt(idt):
  """idt=yyyymmdd"""
  return datetime.datetime(idt / 100 / 100, idt / 100 % 100, idt % 100)


def bool_dt(x):
  if dt2int(int2dt(x) + datetime.timedelta(days=1)) in ymd or \
      dt2int(int2dt(x) + datetime.timedelta(days=0)) in ymd or \
      dt2int(int2dt(x) + datetime.timedelta(days=-1)) in ymd:
    return True
  return False


def nstnam():
  import json
  fn = open('/home/backup/data/epa/pys/sta_list.json')
  d_nstnam = json.load(fn)
  d_namnst = {v: k for k, v in d_nstnam.iteritems()}
  return (d_nstnam, d_namnst)


def func(label):
  for i in xrange(len(labl)):
    if label == labl[i]:
      l[i].set_visible(not l[i].get_visible())
  plt.draw()


def update(val):
  # reading the slider movements and update fig.
  begr = int(sbeg.val / 100. * ldays0) - 1
  endr = max(int(send.val / 100. * ldays0), begr + 1)
  begd, endd = ymd0[max(0, begr)], ymd0[min(ldays0, endr)]
  Movr = 0.5 - sMov.val / 100.
  if Movr != 0:
    if len(s[0])<lx*2:
      for i in xrange(len(nam)):
        s[i]=s[i]+[0 for j in xrange(len(s[i]),lx*2)]
    lhs = max(0, int(lx * (0.5 + Movr)))
    rhs = min(len(s[0]), lx + lhs)
    # print(lx, rhs, lhs, len(s[0]))
    for i in xrange(len(nam)):
      l[i].set_ydata(s[i][lhs:rhs])
    fig.canvas.draw_idle()
    begr,endr=ymd0.index(begd),ymd0.index(endd)
    begd, endd = ymd0[max(0, begr + int(Movr * del_i))], ymd0[max(0, endr + int(Movr * del_i))]
  else:
    # just beg or end sliders are touched, close the old plt and re_construct the diagram
    plt.close()
  with open('input.txt', 'w') as f:
    f.write(str(begd) + ',' + str(endd))
  # print(begd, endd)


def reset(event):
  sys.exit()

def line_select_callback(eclick, erelease):
  'eclick and erelease are the press and release events'
  # x1, y1 = eclick.xdata, eclick.ydata
  # x2, y2 = erelease.xdata, erelease.ydata
  x1 = eclick.xdata
  x2 = erelease.xdata
  begd,endd=ymdh[int(min(x1,x2))]/100,ymdh[int(max(x1,x2))]/100
  with open('input.txt', 'w') as f:
    f.write(str(begd) + ',' + str(endd))
  # print(begd, endd)
  plt.close()
def toggle_selector(event):
  if event.key in ['Q', 'q'] and toggle_selector.RS.active:
      toggle_selector.RS.set_active(False)
  if event.key in ['A', 'a'] and not toggle_selector.RS.active:
      toggle_selector.RS.set_active(True)


# begining of main program...
# read the overall stations and bounds of dates
stnam, SPNAM, begd, endd, act = getarg()
nam = [i for i in stnam.split(',')]
spe = [i for i in SPNAM.split(',')]
if len(nam)>1:
  nam.sort()
if len(spe)>1:
  spe.sort()
csv_fname = SPNAM.replace(',','') + stnam.replace(',', '') + str(begd) + str(endd) + '.csv'
try:
  # in case of replicated execution, read the csv file directly
  df = read_csv(csv_fname)
  days = set([i / 100 for i in df.YYYYMMDD])
  ymd = list(days)
  ymd.sort()
  nam = set([i for i in df.nam])
except:
  # if no exactly same situation, re_reading the EPA original data set
  (d_nstnam, d_namnst) = nstnam()
  if nam[0]=='EPA_ALL':
    nam=list(d_namnst)
    csv_fname = 'EPA_ALL' + str(begd) + str(endd) + '.csv'
  if 'NMHC' in SPNAM:
    nmhc=read_csv('/home/backup/data/epa/pys/NMHC.csv')
    hc_nst=set(nmhc.nst)
    for i in d_nstnam:
      if int(i) not in hc_nst:
        i_name=d_nstnam[i]
        d_namnst.pop(i_name, None)
  for stnam in nam:
    if stnam not in d_namnst: sys.exit("station name not right: " + stnam)
  stn = [d_namnst[i] for i in nam]
  stn = ['0' * (2 - len(i)) + i for i in stn]

  SPNAMs = ['O3', 'PM10', 'PM2.5', 'PMc', 'NOx', 'NO2', 'SO2', 'CO', 'NMHC','WIND_SPEED','WIND_DIREC']
  units = ['PPB', 'ug/M3', 'ug/M3', 'ug/M3', 'PPB','PPB', 'PPB', 'PPM', 'PPM','m/s','deg']
  d_sp2un = {i: j for i, j in zip(SPNAMs, units)}
  fname = '/home/backup/data/epa/pys/item2.txt'  # items of EPA monitoring stations
  with open(fname) as ftext:
    itm = [line.strip('\n') for line in ftext]
  its,unit=[],[]
  for s in spe:
    SPNAMe = s
    if SPNAMe == 'O3e': SPNAMe = 'O3'
    if SPNAMe not in itm: sys.exit('error in item_SPNAM: ' + SPNAMe)
    its.append(itm.index(SPNAMe))
    if SPNAMe not in SPNAMs: sys.exit('error in unit_SPNAM: ' + SPNAMe)
    unit.append(d_sp2un[SPNAMe])
  d_unit={i:j for i, j in zip(spe, unit)}
  sunit=list(set(unit))
  if len(sunit)>2: sys.exit('units more than 2')
  bdate = datetime.datetime(begd / 100 / 100, begd / 100 % 100, begd % 100)
  edate = datetime.datetime(endd / 100 / 100, endd / 100 % 100, endd % 100)
  leng = int(str(edate - bdate).split()[0].split('-')[0]) + 1
  ymd = [dt2int(bdate + datetime.timedelta(days=i)) for i in xrange(leng)]
  yr = set([str(i / 100 / 100) for i in ymd])
  yrmn = set([str(i / 100) for i in ymd])

  mnda = ['0131', '0228', '0331', '0430', '0531', '0630', '0731', '0831', '0930', '1031', '1130', '1231']
  cols = ['NS', 'NAMEST', 'PollID', 'YYYYMMDD']
  for i in xrange(1, 25):
    cols.append('V' + str(i))

  filenm = set()
  for iy in yrmn:
    i = iy[0:4]  # YYYY
    for j in stn:
      k = mnda[int(iy[4:]) - 1]
      yn = k
      if float(i) % 4 == 0 and k == '0228': yn = '0229'
      fn = '/home/backup/data/epa/' + i + '/HS' + i[2:] + yn + '.0' + j
      if fn not in filenm: filenm.add(fn)
  df = DataFrame({})
  line = []
  expected = []
  saw = []
  cont = True
  days = set()
  for fname in filenm:
    try:
      dfA = read_csv(fname, header=None)
    except Exception as e:
      errortype = e.message.split('.')[0].strip()
      if errortype == 'Error tokenizing data':
        cerror = e.message.split(':')[1].strip().replace(',', '')
        nums = [n for n in cerror.split(' ') if str.isdigit(n)]
        expected.append(int(nums[0]))
        saw.append(int(nums[2]))
        line.append(int(nums[1]) - 1)
      else:
        cerror = 'Unknown'
        # print ('Unknown Error - 222')
    else:
      if len(dfA.columns) != 28: continue
      dfA.columns = cols
      df_fl=DataFrame({})
      for itx in its:
        SPNAMe=spe[its.index(itx)]
        if SPNAMe == 'O3e': SPNAMe = 'O3'
        dfs = dfA[dfA['PollID'] == itx].reset_index(drop=True)
        dfs = dfs[dfs['YYYYMMDD'].map(lambda x: bool_dt(x))].reset_index(drop=True)
        if len(dfs) == 0: continue
        dfs[SPNAMe] = [list(dfs.iloc[i, 4:]) for i in xrange(len(dfs))]
        df1 = DataFrame({'YMDH': [i * 100 + k for i in dfs['YYYYMMDD'] for k in xrange(24)],
                         'nam': [d_nstnam[str(int(fname[-2:]))] for i in xrange(len(dfs) * 24)],
                       SPNAMe: [i[k] for i in dfs[SPNAMe] for k in xrange(24)]})
        if its.index(itx)==0:
          df_fl=df1
        else:
          df_fl=merge(df_fl,df1,on=['YMDH','nam'])
      df = df.append(df_fl).reset_index(drop=True)
  df = df.sort_values(['nam', 'YMDH']).reset_index(drop=True).clip(0)
  df['YMD']=[i/100 for i in df.YMDH]
  df['MDH']=[i%1000000 for i in df.YMDH]
  for i in list(df['YMD']):
    days.add(i)
  if 'O3e' in SPNAM:
    for stnam in nam:
      df1 = df[df['nam'] == stnam].reset_index(drop=True)
      l = list(df1['O3'])
      l8 = l
      l8[3:len(df1) - 5] = [np.mean(l[i - 3:i + 5]) for i in xrange(3, len(df1) - 5)]
      df.loc[df['nam'] == stnam, 'O3e'] = l8
  df.set_index('YMDH').to_csv(csv_fname)
  if csv_fname[:7]=='EPA_ALL':sys.exit('saved EPA_ALL')
  with open('input.txt', 'w') as f:
    f.write(str(begd) + ',' + str(endd))
# time series plot
# prepare for endless loop of plotting(viewing)
ints = [3, 6, 12, 24, 48, 72, 168]
ymd0 = ymd
days0 = days
begd0, endd0 = begd, endd
ldays0 = min(len(days0), len(ymd0))
while True:
  with open('input.txt', 'r') as f:
    af = [i.strip('\n').split(',') for i in f]
  begd, endd = [int(i) for i in af[0]]
  ymd = [i for i in ymd0 if i >= begd and i <= endd]
  days = [i for i in days0 if i >= begd and i <= endd]

  # prepare the data for the mover slider, it need 2*lx data
  ibeg, iend = ymd0.index(begd), ymd0.index(endd)
  del_i = iend - ibeg
  if del_i > 0.5 * ldays0:
    ymd2 = ymd
  else:
    lhs = max(0, int(ibeg - del_i / 2))
    rhs = min(ldays0, int(iend + del_i / 2))
    ymd2 = list(set(ymd + ymd0[lhs:ibeg] + ymd0[iend:rhs]))
    ymd2.sort()
  s = []
  for stnam in nam:
    for sp in spe:
      boo = (df['nam'] == stnam) & (df['YMDH'].map(lambda x: x / 100 in ymd2))
      df1 = df[boo].reset_index(drop=True)
      s.append(list(df1.loc[:, sp]))

  # initialize of fig.
  fig, ax = plt.subplots()
  SPNAM1=''
  for sp in spe:
    if d_unit[sp]==sunit[0]:
      SPNAM1+=sp+','
  SPNAM1=SPNAM1[:-1]
  plt.ylabel(SPNAM1 + "(" + sunit[0] + ")")
  if sunit[0]=='deg':
    ax.yaxis.set_ticks(np.arange(0, 361, 45))
  if len(sunit)==2:
    ax2 = ax.twinx()
    SPNAM2=''
    for sp in spe:
      if d_unit[sp]==sunit[1]:
        SPNAM2+=sp+','
    SPNAM2=SPNAM2[:-1]
    ax2.set_ylabel(SPNAM2 + '(' + sunit[1] + ')', color='y')
  plt.subplots_adjust(left=0.1, bottom=0.25)
  # ax = plt.axes([0.1, 0.3, 0.8, 0.6])
#  plt.legend(loc='SouthEast')plt.xlabel(SPNAM + ' from ' + str(begd) + ' to ' + str(endd))
  plt.xlabel(SPNAM + ' from ' + str(begd) + ' to ' + str(endd))

  # dealing with xticks for different density of dates by try and error to find best fit
  intv = 3
  ldays = min(len(days), len(ymd))
  for i in xrange(6, -1, -1):
    if 5 <= ldays * 24 / ints[i] <= 20: intv = ints[i]

  # store the figures of each station to the list of l[]
  l,labl= [],[]
  for stnam in nam:
    boo = (df['nam'] == stnam) & (df['YMDH'].map(lambda x: x / 100 in ymd))
    df1 = df[boo].reset_index(drop=True)
    totalSeed = df1.index.tolist()
    lx = len(totalSeed)
    for sp in spe:
      if d_unit[sp]==sunit[0]:
        l1, = ax.plot(totalSeed, df1.loc[:, sp], label=stnam, lw=1)#+'_'+sp, lw=1)
      else:
        l1, = ax2.plot(totalSeed, df1.loc[:, sp], label=stnam+'_'+sp, lw=1,linestyle='--')
      l.append(l1)
      labl.append(stnam+'_'+sp)
    if stnam == nam[0]:
      xticks = list(range(0, len(totalSeed), intv))
    ymdh = list(df1.loc[:, 'YMDH'])
    xlabels = [df1.loc[:, 'MDH'][x] for x in xticks]
    xlabels.append(str(int(xlabels[-1]) + intv))
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, rotation=40, fontsize=8)
    ax.legend(bbox_to_anchor=(0., 1.08), loc=2, borderaxespad=0., fontsize=9, ncol=len(nam))

  # check box module begin__________
  llabl=0.04*len(labl)
  rax = plt.axes([0.11, 0.88-llabl, 0.1, llabl], alpha=0.5, frame_on=False)
  boo = [True for i in xrange(len(labl))]
  check = CheckButtons(rax, (labl), (boo))
  check.on_clicked(func)
  # check box module end_____________ before show

  # Slider module begin__________
  b0, e0 = 0.1, 0.1
  bm, em = ibeg * 100. / ldays0, iend * 100. / ldays0
  axcolor = 'lightgoldenrodyellow'
  width = 0.75
  axbeg = plt.axes([0.13, 0.09, width, 0.03], facecolor=axcolor)
  axMov = plt.axes([0.13 + (bm / 100 * width), 0.05, max(0.2, (em - bm) / 100. * width), 0.03], facecolor=axcolor)
  axend = plt.axes([0.13, 0.01, width, 0.03], facecolor=axcolor)
  sbeg = Slider(axbeg, 'beg', 0.1, 100.0, valinit=bm, valfmt='%1.0f')
  send = Slider(axend, 'end', 0.1, 100.0, valinit=em, valfmt='%1.0f')
  sMov = Slider(axMov, '', 0.1, 100.0, valinit=50, valfmt='%1.0f')
  sbeg.on_changed(update)
  send.on_changed(update)
  sMov.on_changed(update)
  # Slider end_____________ before show

  # button module begin__________
  resetax = plt.axes([0.89, 0.01, 0.08, 0.04])
  button = Button(resetax, 'Exit', color=axcolor, hovercolor='0.975')
  button.on_clicked(reset)
  # button end_____________ before show

  # output the diagram, either to DISPLAY or savefig

  # drawtype is 'box' or 'line' or 'none'
  toggle_selector.RS = RectangleSelector(ax, line_select_callback,
                                       drawtype='box', useblit=True,
                                       button=[1, 3],  # don't use middle button
                                       minspanx=5, minspany=5,
                                       spancoords='pixels',
                                       interactive=True)
  plt.connect('key_press_event', toggle_selector)

  if act[0] == 'plot'[0]: plt.show()
  if act[0] == 'save'[0]:
    pwd = subprocess.check_output('pwd', shell=True).strip('\n')
    dir = pwd + '/pngs'
    os.system('if ! [ -e ' + dir + ' ];then  mkdir -p ' + dir + ' ;fi')
    name = SPNAM.replace(',','') + '@' + str(begd)
    for i in nam:
      name = name + i
    plt.savefig(dir + '/' + name + '.png')
    break
