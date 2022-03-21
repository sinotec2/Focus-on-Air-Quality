#!/cluster/miniconda/bin/python
# -*- coding: utf-8 -*-
"""plot the hrly time series of pollutant at station(s)
    specHr.py -b 2071231 -e 20180101 -s PM2.5 -a plot -t wanli,xianxi,puzi,xiaogang """
import matplotlib.pyplot as plt
from pandas import *
import sys, os, datetime
from matplotlib.widgets import CheckButtons, Slider, Button


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
  for i in xrange(len(nam)):
    if label == nam[i]:
      l[i].set_visible(not l[i].get_visible())
  plt.draw()


def update(val):
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
    plt.close()
  with open('input.txt', 'w') as f:
    f.write(str(begd) + ',' + str(endd))
  print(begd, endd)


def reset(event):
  sys.exit()


stnam, SPNAM, begd, endd, act = getarg()
nam = [i for i in stnam.split(',')]
csv_fname = SPNAM + stnam.replace(',', '') + str(begd) + str(endd) + '.csv'
try:
  df = read_csv(csv_fname)
  days = set([i / 100 for i in df.YYYYMMDD])
  ymd = list(days)
  ymd.sort()
  nam = set([i for i in df.nam])
except:
  (d_nstnam, d_namnst) = nstnam()
  for stnam in nam:
    if stnam not in d_namnst: sys.exit("station name not right: " + stnam)
  stn = [d_namnst[i] for i in nam]
  stn = ['0' * (2 - len(i)) + i for i in stn]

  fname = '/home/backup/data/epa/pys/item2.txt'  # items of EPA monitoring stations
  with open(fname) as ftext:
    itm = [line.strip('\n') for line in ftext]
  SPNAMe = SPNAM
  if SPNAMe == 'O3e': SPNAMe = 'O3'
  if SPNAMe not in itm: sys.exit('error in item_SPNAM: ' + SPNAMe)
  itx = itm.index(SPNAMe)

  SPNAMs = ['O3', 'PM10', 'PM2.5', 'PMc', 'NOx', 'SO2', 'CO', 'NMHC']
  units = ['ppb', 'ug/M3', 'ug/M3', 'ug/M3', 'PPB', 'PPB', 'PPM', 'PPM']
  d_sp2un = {i: j for i, j in zip(SPNAMs, units)}
  if SPNAMe not in SPNAMs: sys.exit('error in unit_SPNAM: ' + SPNAM)
  unit = d_sp2un[SPNAMe]
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
      dfs = read_csv(fname, header=None)
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
        print 'Unknown Error - 222'
    else:
      if len(dfs.columns) != 28: continue
      dfs.columns = cols
      dfs = dfs[dfs['PollID'] == itx].reset_index(drop=True)
      dfs = dfs[dfs['YYYYMMDD'].map(lambda x: bool_dt(x))].reset_index(drop=True)
      if len(dfs) == 0:
        continue
      dfs[SPNAM] = [list(dfs.iloc[i, 4:]) for i in xrange(len(dfs))]
      df1 = DataFrame({'MDH': [i % 10000 * 100 + k for i in dfs['YYYYMMDD'] for k in xrange(24)],
                       'YMDH': [i * 100 + k for i in dfs['YYYYMMDD'] for k in xrange(24)],
                       'nam': [d_nstnam[str(int(fname[-2:]))] for i in xrange(len(dfs) * 24)],
                       SPNAM: [i[k] for i in dfs[SPNAM] for k in xrange(24)]})
      df = df.append(df1).reset_index(drop=True)
      for i in list(dfs['YYYYMMDD']):
        days.add(i)
  df = df.sort_values(['nam', 'YMDH']).reset_index(drop=True).clip(0)
  if SPNAM == 'O3e':
    for stnam in nam:
      df1 = df[df['nam'] == stnam].reset_index(drop=True)
      l = list(df1[SPNAM])
      l8 = l
      l8[3:len(df1) - 5] = [np.mean(l[i - 3:i + 5]) for i in xrange(3, len(df1) - 5)]
      df.loc[df['nam'] == stnam, 'O3e'] = l8
  df.set_index('YMDH').to_csv(csv_fname)
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
    boo = (df['nam'] == stnam) & (df['YMDH'].map(lambda x: x / 100 in ymd2))
    df1 = df[boo].reset_index(drop=True)
    s.append(list(df1.loc[:, SPNAM]))

  fig, ax = plt.subplots()
  plt.subplots_adjust(left=0.1, bottom=0.25)
  # ax = plt.axes([0.1, 0.3, 0.8, 0.6])
  plt.legend(loc='SouthEast')
  plt.xlabel(SPNAM + ' from ' + str(begd) + ' to ' + str(endd))
  plt.ylabel(SPNAM + "(" + unit + ")")
  intv = 3
  ldays = min(len(days), len(ymd))
  for i in xrange(6, -1, -1):
    if 5 <= ldays * 24 / ints[i] <= 20: intv = ints[i]

  l = []
  for stnam in nam:
    boo = (df['nam'] == stnam) & (df['YMDH'].map(lambda x: x / 100 in ymd))
    df1 = df[boo].reset_index(drop=True)
    totalSeed = df1.index.tolist()
    lx = len(totalSeed)
    l1, = ax.plot(totalSeed, df1.loc[:, SPNAM], label=stnam, lw=2)
    l.append(l1)
    if stnam == nam[0]:
      xticks = list(range(0, len(totalSeed), intv))
    xlabels = [df1.loc[:, 'MDH'][x] for x in xticks]
    xlabels.append(str(int(xlabels[-1]) + intv))
    ax.set_xticks(xticks)
    ax.set_xticklabels(xlabels, rotation=40, fontsize=8)
    ax.legend(bbox_to_anchor=(0., 1.08), loc=2, borderaxespad=0., fontsize=9, ncol=5)  # len(nam)

  # check box module begin__________
  rax = plt.axes([0.13, 0.72, 0.1, 0.15], alpha=0.5, frame_on=False)
  boo = [True for i in xrange(len(nam))]
  check = CheckButtons(rax, (nam), (boo))
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

  if act[0] == 'plot'[0]: plt.show()

  if act[0] == 'save'[0]:
    dir = '/home/backup/data/epa/pys/SPNAMHr/pngs'
    os.system('if ! [ -e ' + dir + ' ];then  mkdir -p ' + dir + ' ;fi')
    name = SPNAM + '@' + str(begd)
    for i in nam:
      name = name + i
      plt.savefig(dir + '/' + name + '.png')
