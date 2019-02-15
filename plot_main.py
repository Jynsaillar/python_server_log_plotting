import matplotlib.pyplot as plt
import numpy as np
import mysql_helper as db_data
import helper as helper
from datetime import datetime


def makeplot(ax, dates, users, name, distinct_color):

    plotname = ''
    if helper.only_roman_chars(name):
        plotname = name
    else:
        plotname = helper.arabicstring(name)
    ax.plot(dates, users, label=plotname, color=distinct_color)
    return


def populateaxes(ax, server_names, db_params, verbose, date_blob, nightmode, graph_type):

    colors = helper.getcolors(offset=0, n=len(server_names), nightmode=nightmode)
    serverlogdata = []
    timedata = []
    usercountdata = []
    colorcounter = 0
    for server in server_names:
        timedata.clear()
        usercountdata.clear()
        serverlogdata = db_data.getserverlog(db_params, verbose, date_blob, server)
        for entry in serverlogdata:
            timedata.append(entry[0])
            # 1 = MIN, 2 = AVG, 3 = MAX
            usercountdata.append(entry[graph_type])
        makeplot(ax, timedata, usercountdata, server, colors[colorcounter])
        colorcounter += 1
    return


def drawfullplot(fig, ax, server_names, db_params, verbose, date_blob, intervals, nightmode, graph_type):

    _, _, date_from, date_to = date_blob
    intervalusers, intervalhours = intervals
    maxplayers = db_data.getmaxplayers(db_params, verbose, date_blob)

    # Configuring the plot.
    ax.set_xlabel('Time')
    ax.set_ylabel('Player Count')
    if graph_type == 1:
        ax.set_title('Rappelz Global Player Statistics - Least Users Per Hour')
    elif graph_type == 2:
        ax.set_title('Rappelz Global Player Statistics - Average Users Per Hour')
    elif graph_type == 3:
        ax.set_title('Rappelz Global Player Statistics - Most Users Per Hour')

    ylimit = helper.roundtonextbase(x=maxplayers, base=intervalusers)
    xlimit = helper.gethoursdifference(date_from, date_to)
    ax.set_xlim(left=0, right=xlimit-1)
    ax.set_ylim(bottom=0, top=ylimit)

    # Pulls log data from the database and builds plots for each server.
    populateaxes(ax, server_names, db_params, verbose, date_blob, nightmode, graph_type)

    start, end = ax.get_xlim()
    end = helper.roundtonextbase(end, intervalhours) + 1
    ax.xaxis.set_ticks(np.arange(start, end, intervalhours))
    ax.yaxis.set_ticks(np.arange(0, ylimit+intervalusers, step=intervalusers))
    # Fixes rotation of xticks, otherwise they would overlap horizontally.
    for tick in ax.get_xticklabels():
        tick.set_rotation(90)

    ax.tick_params(axis='x', labelsize=8)
    # Legend must be created after populating the plots as it needs the server names.
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, 1), ncol=4, fancybox=True)

    return


def onresize(event):
    # Calls tight_layout from plot.getcurrentfigure() which minimizes blank space.
    plt.gcf().tight_layout()


def main():

    cmdargs = dict(helper.parseparams())

    dbparams = (
        cmdargs.get('dbuser'),
        cmdargs.get('dbpassword'),
        cmdargs.get('dbhost'),
        cmdargs.get('dbname'))
    datestringfrom = cmdargs.get('datestringfrom')
    datestringto = cmdargs.get('datestringto')
    dateformat = cmdargs.get('dateformat')
    intervalusers = cmdargs.get('intervalusers')
    intervalhours = cmdargs.get('intervalhours')
    verbose = cmdargs.get('verbose')
    nightmode = cmdargs.get('nightmode')
    graph_type = cmdargs.get('graph')

    if nightmode:
        plt.style.use('dark_background')

    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.1)

    if nightmode:
        ax.grid(color="darkgray", alpha=0.125)
    else:
        bgcolor = 'xkcd:white'
        fig.patch.set_facecolor(bgcolor)
        ax.set_facecolor(bgcolor)
        ax.grid(color="darkgray", alpha=0.8)

    fig.canvas.mpl_connect('resize_event', onresize)
    fig.canvas.set_window_title('Rappelz Log Statistics')

    datefrom = datetime.strptime(datestringfrom, dateformat)
    dateto = datetime.strptime(datestringto, dateformat)

    dateblob = (datestringfrom, datestringto, datefrom, dateto)
    intervals = (intervalusers, intervalhours)

    servernames = helper.extractservernames(
                  db_data.getservernames(dbparams, verbose))

    drawfullplot(fig, ax, servernames, dbparams, verbose, dateblob, intervals, nightmode, graph_type)

    plt.show()
    return


if __name__ == "__main__":
    main()
