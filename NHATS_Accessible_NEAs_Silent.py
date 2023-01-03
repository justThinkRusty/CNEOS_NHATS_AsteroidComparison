import requests  # For API string pull
from matplotlib import pyplot  # Required for plotting
import numpy as np  # is numpy
from datetime import date  # File naming and displayed date of currency
from PIL import Image  # For image manipulation
import os  # For deleting intermittent image files
import time  # For tracking time duration

from PlanetaryData import *  # Pre-defined planetary data import from file

t = time.time()
today = date.today()

# Specify path for local machine to save intermittent and final graphs
fullpath_spec = os.path.dirname(os.path.realpath(__file__)) + "/CNEOS_Pictures/"


# Font for internal graphing
# If on a Mac, use Helvetica
# If on a PC, use Arial
# If on Ubuntu use FreeSans

if os.name == 'posix': # My ubuntu machine
    font_name = 'FreeSans'
elif os.name == 'nt': # PC
    font_name = 'Arial'
elif os.name == 'Darwin': #My Mac
    font_name = 'Helvetica'
else: 
    # Ask user to specify font
    font_name = input("Please specify the font name for your system (If on a Mac, use 'Helvetica', if on a PC, use 'Arial' and if on Ubuntu use 'F'reeSans'): ")

fontdict = {'family': font_name,
            'weight': 'normal',
            'size': 7,
            }

# Font for left side statistics
fontdict2 = {'family': font_name,
             'weight': 'normal',
             'size': 5,
             }

# Font for data currency date
fontdict3 = {'family': font_name,
             'weight': 'normal',
             'size': 9,
             'color': '#ff9b00',
             }

fontdict6 = {'family': font_name,
             'weight': 'bold',
             'size': 5.75,
             }

# Pull the date for today

# Automatically rounds to values 10-15 years in the future of rounded value to nearest 5 increment
# There are a few here, because a few different ranges have been asked for - can select one pattern for integration 
# (or keep as a variable for end-user selection?)
Green_Range = str(5*round(today.year/5)+10) + "-" + str(5*round(today.year/5)+15)
Green_Range_2 = str(5*round(today.year/5)+15) + "-" + str(5*round(today.year/5)+20)
Green_Name_Range = str(5*round(today.year/5)+10) + "-" + str(5*round(today.year/5)+20)

# Auto set large year range to be within the previous 5 years to 25 years from that in future
Blue_Range = str(5*round((today.year-3)/5)) + "-" + str(5*round((today.year-3)/5)+25)
Ranges = [Blue_Range, Green_Range, Green_Range_2]  # Color based dedication of ranges for final plot

# Figure with proper sizing for main central plot
fig = pyplot.figure(figsize=(7.06, 5.80), dpi=370)
ax = fig.gca()
pyplot.xlim(0, 950), pyplot.xticks(np.arange(0, 950+1, 50), fontsize=6)
pyplot.ylim(0, 18), pyplot.yticks(np.arange(0, 18+1, 1), fontsize=6)
ax.tick_params('both', length = 0, pad = 1)

# Well formatted gridlines:
for i in np.arange(0, 950, 50):
    if i == 45:
        pyplot.plot([i, i], [12, 18], color = 'lightgray', linestyle = 'dashed', linewidth = 1,zorder=1)
    else:
        pyplot.plot([i, i], [0, 18], color = 'lightgray', linestyle = 'dashed', linewidth = 1,zorder=1)
for i in np.arange(0, 18, 1):
    if i != 12:
        pyplot.plot([0, 950], [i, i], color = 'lightgray', linestyle = 'dashed', linewidth = 1,zorder=1)

# Axis labels with reduced padding to be closer to matlab standards
pyplot.xlabel('Round-Trip Flight Time, days', fontsize=8, labelpad=3)
pyplot.ylabel('Total Round-Trip \u0394V (from LEO), km/s', fontsize=8, labelpad=3)

blue_tot = 0

#Begin iterative pulls:
for YearRange in Ranges:  # Set from published API string requirements

    for dv in range(4, 12+1, 1):  # Manual set of current API dV limits

        for dur in range (30, 450+1, 30):  # Manual set of current API duration limitations
            
            #Assemble API string for current iteration:
            API_String = 'https://ssd-api.jpl.nasa.gov/nhats.api?dv=' + str(dv) + "&dur=" + str(dur) + '&launch=' + YearRange
            response_API = requests.get(API_String)  # Pull from the API
            dataName = 'NHATS_' + str(dv) + '_' + str(dur)  # Create an interim name for the JSON file according to dV and duration
            dataName = response_API.json()  # Translate the file to JSON formatting

            # Count how many asteroids exist in this dataset iteration
            NumObjects = int(dataName['count']) #Get total number of asteroids per pull
            sortedName = np.empty([NumObjects, 4]) #Create an array for housing the specified duration/dV data from each point

            # Assign desired values to temp matrix for plotting of delta V's and durations in each minimizied case:
            track = 0
            for i in dataName['data']:

                # Separate out the data from the JSON file into a matrix
                sortedName[track,0] = float(i['min_dv']['dv'])
                sortedName[track,1] = float(i['min_dv']['dur'])
                sortedName[track,2] = float(i['min_dur']['dv'])
                sortedName[track,3] = float(i['min_dur']['dur'])
                track = track + 1
                # if YearRange == Blue_Range:
                blue_tot = blue_tot + 1

            # Plotting in specified color:s
            if YearRange == Green_Range or YearRange == Green_Range_2:
                pyplot.scatter(sortedName[:,1],sortedName[:,0],s=4,c='#00FF00',marker='x',zorder=3)
                pyplot.scatter(sortedName[:,3],sortedName[:,2],s=4,c='#00FF00',marker='x',zorder=3)
            else:
                pyplot.scatter(sortedName[:,1],sortedName[:,0],s=4,c='#0000FF',marker='x',zorder=3)
                pyplot.scatter(sortedName[:,3],sortedName[:,2],s=4,c='#0000FF',marker='x',zorder=3)


# Data plotting functions:
# Filter variables for current year, scatter points and plot descriptive strings
def sortNamePlot(matrx, clr, mrkr):
    for rows in matrx:
        if rows[2] >= today.year:
            pyplot.scatter(rows[1], rows[0],  s=16, color = "none", edgecolors = clr, marker = mrkr, zorder=4)
            pyplot.text(rows[1] + rows[4], rows[0] + rows[5], str(round(rows[2])) + ", " + str(round(rows[3], 2)) + "AU", fontdict)

# For data that does not need to be sorted (kept for context):
def NamePlot(matrx, clr, mrkr):
    for rows in matrx:
        pyplot.scatter(rows[1], rows[0], s=16, color = "none", edgecolors = clr, marker = mrkr, zorder=4)
        pyplot.text(rows[1] + rows[4], rows[0] + rows[5], str(round(rows[2])) + ", " + str(round(rows[3], 2)) + "AU", fontdict)

# Add (w/Venus flyby) text on graph
def addVenus(matrx):
    for rows in matrx:
        if rows[2] >= today.year:
            pyplot.text(rows[1] + rows[4], rows[0] + rows[5] - 0.375, "(w/Venus flyby)", fontdict)


# -------------------------- Brent Barbee Data - Required import of PlanetaryData.py -----------------------------
min_esc_dv = 3.176
xmax = 950

# Lunar-related data:
lunar_surf_dt = np.arange(14,21+0.01,0.1)
lunar_surf_dv = 9*np.ones(np.size(lunar_surf_dt))

lunar_orb_dt = np.arange(7, 21 + 0.01, .1)
lunar_orb_dv = 5*np.ones((1, len(lunar_orb_dt)))

# Earth LEO escape data:
min_esc_dv_x = np.arange(0, xmax + 0.01, .1)
min_esc_dv_y = min_esc_dv*np.ones(np.size(min_esc_dv_x))

# Lunar data plotting:
pyplot.scatter(lunar_surf_dt,lunar_surf_dv, s=4, color = "none", edgecolors=  '#00FFFF', marker='*', zorder=4)
pyplot.scatter(lunar_orb_dt,lunar_orb_dv, s=4, color = "none", edgecolors = '#FF00FF', marker='*', zorder=4)

# Earth escape LEO line:
pyplot.plot(min_esc_dv_x,min_esc_dv_y, c='#00FF00', linewidth = 3, zorder=3)

#A RRM Plotting - Removed March 17, 2022:
# pyplot.scatter(arrm[1],arrm[0], s=6, color = "none", edgecolors=  '#ff9f21', marker='*', zorder=4)

# Mars data plotting:
sortNamePlot(mars_Fast7, '#FF0000', "o" )
sortNamePlot(mars_Fast45, '#FF0000', "^")
sortNamePlot(mars_Venus45, '#FF0000', '*')
addVenus(mars_Venus45)

pyplot.scatter(mars_dra_no_surf_dv12[:,1], mars_dra_no_surf_dv12[:,0], s=16, color = "none", edgecolors = '#FF0000', marker='s', zorder=3)
pyplot.scatter(mars_dra_surf_dv12[:,1], mars_dra_surf_dv12[:,0], s=16, color = "none", edgecolors = '#FF0000', marker='s', zorder=3)

# Free return plotting:
NamePlot(mars_free_ret_eme, '#FF0000', 'D')
addVenus(mars_free_ret_eme)

# Free return plotting:
NamePlot(mars_free_ret_evme, '#FF0000', 'D')
addVenus(mars_free_ret_evme)
# -------------------------- End Brent Barbee Data -----------------------------

# Barrier line plotting - based on API string pull limits
pyplot.plot([450, 450], [0, 12], 'k--', linewidth = 2)
pyplot.plot([0, 950], [12, 12], 'k--', linewidth = 2)

# Creating names for both main graph and final plot
name = fullpath_spec + 'NEO_Comparison_' + str(today.year) + '_' + str(today.month) + '_' + str(today.day) + '.png'
nameFin = fullpath_spec + 'CNEOS_AstCompare_' + str(today.year) + '_' + str(today.month) + '_' + str(today.day) + '.png'
pyplot.savefig(name, transparent=True) #Save main central plot


# ---------------------- Small body database comparison statistics -----------------------------------
# Pull the most broad case from NHATS API
NHATS_Broad = requests.get('https://ssd-api.jpl.nasa.gov/nhats.api'); NHATS_unc = NHATS_Broad.json()
NHATS_tot = int(NHATS_unc['count'])

# Pull from all four classes of asteroid:
SMDB_Atira = requests.get('https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,pdes,e,a,i,H&sb-class=IEO'); SMDB_Atira_unc = SMDB_Atira.json()
SMDB_Aten = requests.get('https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,pdes,e,a,i,H&sb-class=ATE'); SMDB_Aten_unc = SMDB_Aten.json()
SMDB_Apollo = requests.get('https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,pdes,e,a,i,H&sb-class=APO'); SMDB_Apollo_unc = SMDB_Apollo.json()
SMDB_Amor = requests.get('https://ssd-api.jpl.nasa.gov/sbdb_query.api?fields=spkid,pdes,e,a,i,H&sb-class=AMO'); SMDB_Amor_unc = SMDB_Amor.json()

# Count totals for each
Atira_tot = int(SMDB_Atira_unc['count'])
Aten_tot = int(SMDB_Aten_unc['count'])
Apollo_tot = int(SMDB_Apollo_unc['count'])
Amor_tot = int(SMDB_Amor_unc['count'])

Total_NEAs = Atira_tot + Aten_tot + Apollo_tot + Amor_tot  # Total NEAs for stats later

frac_NEAs = NHATS_tot/Total_NEAs*100; perc = round(frac_NEAs, 2)  # What fraction of NEAs are in NHATS

# Counter in separate categories to make sure all NEAs have been acounted for
IEO_c = 0; ATE_c = 0; APO_c = 0; AMO_c = 0

# Asteroid data tracking
NHATS_i = np.empty([NHATS_tot, 1]); NHATS_H = np.empty([NHATS_tot, 1])
NHATS_a = np.empty([NHATS_tot, 1]); NHATS_e = np.empty([NHATS_tot, 1])
NEAs_H = np.empty([Total_NEAs, 1])

foo = 0  # Counter through all asteroids for H

# Iterate through each list of general asteroid classes to identiy NHATS opportunities
for i in SMDB_Atira_unc['data']:
    NEAs_H[foo] = i[5]; foo = foo + 1  # Get H for all asteroids
    for j in NHATS_unc['data']:  # Iterate through the NAHTS pull to compare name strings
        if i[1] == j['des']:  # If name strings identical
            # print('Atira found')
            indx = IEO_c  # Set indexing value and subsequently fill desired data in predef mats
            NHATS_e[indx] = i[2]; NHATS_a[indx] = i[3]
            NHATS_i[indx] = i[4]; NHATS_H[indx] = i[5]
            IEO_c = IEO_c + 1

for i in SMDB_Aten_unc['data']:
    NEAs_H[foo] = i[5]; foo = foo + 1  # Get H for all asteroids
    for j in NHATS_unc['data']:
        if i[1] == j['des']:
            # print('Aten Found')
            indx = IEO_c + ATE_c
            NHATS_e[indx] = i[2]; NHATS_a[indx] = i[3]
            NHATS_i[indx] = i[4]; NHATS_H[indx] = i[5]
            ATE_c = ATE_c + 1

for i in SMDB_Apollo_unc['data']:
    NEAs_H[foo] = i[5]; foo = foo + 1  # Get H for all asteroids
    for j in NHATS_unc['data']:
        if i[1] == j['des']:
            # print('Apollo Found')
            indx = IEO_c + ATE_c + APO_c
            NHATS_e[indx] = i[2]; NHATS_a[indx] = i[3]
            NHATS_i[indx] = i[4]; NHATS_H[indx] = i[5]
            APO_c = APO_c + 1

for i in SMDB_Amor_unc['data']:
    NEAs_H[foo] = i[5]; foo = foo + 1  # Get H for all asteroids
    for j in NHATS_unc['data']:
        if i[1] == j['des']:
            # print('Amor Found')
            indx = IEO_c + ATE_c + APO_c + AMO_c
            NHATS_e[indx] = i[2]; NHATS_a[indx] = i[3]
            NHATS_i[indx] = i[4]; NHATS_H[indx] = i[5]
            AMO_c = AMO_c + 1


# Test sum for all asteroids found to be in NHATS
sum_test = IEO_c + ATE_c + APO_c + AMO_c


# Function for definining mins, averages, and max values in each matrix (excluding nans if they occur)
def min_avg_max(mat):
    min = np.nanmin(mat)
    avg = np.nanmean(mat)
    max = np.nanmax(mat)
    nums = [min, avg, max]
    return nums


i_nums = min_avg_max(NHATS_i); H_nums = min_avg_max(NHATS_H);
a_nums = min_avg_max(NHATS_a); e_nums = min_avg_max(NHATS_e);
H_NEA_nums = min_avg_max(NEAs_H)

# Create figure for plotting numerical statistics
fig2 = pyplot.figure(figsize=(1, 2.1), dpi=400)
ax = fig2.gca()
pyplot.xlim(0, 2); pyplot.ylim(0, 4)
ax.axis('off')


# Rounding and plotting the min, avg, and max values in each category
def multi_stats_plotting(mats, x, y):
    pyplot.text(x, y, str(round(mats[0], 2)) + ", " + str(round(mats[1], 2)) + ", " + str(round(mats[2],2)), fontdict2) #Semi-major axis AU


# Plot the min, avg, and max values of the selected set at coordinate values
multi_stats_plotting(a_nums, 0.125, 1.35)
multi_stats_plotting(e_nums, 0.125, 0.72)
multi_stats_plotting(i_nums, 0.125, 0.08)


# Function for plotting the percentage statistics
def perc_visuals(NHATS_count, Total_count, x1, x2, y):  # Plotting for percentages in stats corner
    # NHATS_count is the number of NHATS asteroids found in this categroy
    # Total_count is the total number of asteroids known in this category
    per_NHATS = round(NHATS_count/NHATS_tot*100)
    per_total = round(NHATS_count/Total_count*100)
    pyplot.text(x1, y, str(per_NHATS) + "%", fontdict2)
    pyplot.text(x2, y, str(per_total) + "%", fontdict2)


# Plot the percentage statistics
perc_visuals(IEO_c, Atira_tot, 0.9, 1.4, 2.39)
perc_visuals(ATE_c, Aten_tot, 0.8, 1.3, 2.198)
perc_visuals(APO_c, Apollo_tot, 0.8, 1.3, 2)
perc_visuals(AMO_c, Amor_tot, 0.8, 1.4, 1.80)


# Single number statistics at top of statistics corner
def single_num_stats(num, x, y):
    pyplot.text(x, y, str(num), fontdict2)


single_num_stats(round(H_nums[1],3), 0.125, 2.775)  # NHATS H averages
single_num_stats(round(H_NEA_nums[1],3), 0.125, 3.2)  # Total NEAs H
single_num_stats("{:,}".format(NHATS_tot), 0.125, 3.64)  # NHATS total
single_num_stats(str(perc) + "%", 0.65, 3.65)  # Percentage NHATS/SMDB
single_num_stats("{:,}".format(Total_NEAs), 0.125, 4.07)  # Total from SMDB


name_stats = fullpath_spec + 'NEO_Stats_' + str(today.year) + '_' + str(today.month) + '_' + str(today.day) + '.png'
fig2.savefig(name_stats, transparent=True)


# Figure for updating day of currency
fig3 = pyplot.figure(figsize=(0.75, 0.2), dpi=400)
ax = fig3.gca()
pyplot.xlim(0, 0.5); pyplot.ylim(0, 0.2)
ax.axis('off')
pyplot.text(0, 0, str(today.year) + "-" + str(today.month) + "-" + str(today.day), fontdict3)
name_date = fullpath_spec + 'NEO_date_' + str(today.year) + '_' + str(today.month) + '_' + str(today.day) + '.png'
fig3.savefig(name_date, transparent=True)


# Figure for updating years in green range
fig4 = pyplot.figure(figsize=(0.75, 0.2), dpi=400)
ax = fig4.gca()
pyplot.xlim(0, 0.5); pyplot.ylim(0, 0.2)
ax.axis('off')
pyplot.text(0, 0, Green_Name_Range, fontdict2)
name_Green = fullpath_spec + 'NEO_GreenRange_' + str(today.year) + '_' + str(today.month) + '_' + str(today.day) + '.png'
fig4.savefig(name_Green, transparent=True)

# #Figure for updating years in blue range
# fig5 = pyplot.figure(figsize=(0.75, 0.2), dpi=400)
# ax = fig5.gca()
# pyplot.xlim(0, 0.5); pyplot.ylim(0, 0.2)
# ax.axis('off')
# pyplot.text(0, 0, Blue_Range, fontdict2)
# name_Blue = fullpath_spec + 'NEO_BlueRange_' + str(today.year) + '_' + str(today.month) + '_' + str(today.day) + '.png'
# fig5.savefig(name_Blue, transparent=True)

# Figure for marker identification
fig5 = pyplot.figure(figsize=(1, 2.1), dpi=400)
ax = fig5.gca()
pyplot.xlim(0, 2); pyplot.ylim(0, 4)
ax.axis('off')
# Change the following markers if the red markers ever decide to get changed:
pyplot.scatter(1, 2.25, s=32, color = "none", edgecolors = '#FF0000', marker='o')
pyplot.scatter(1, 1.65, s=32, color = "none", edgecolors = '#FF0000', marker='^')
pyplot.scatter(1, 0.95, s=45, color = "none", edgecolors = '#FF0000', marker='*')
pyplot.scatter(1, 0.25, s=32, color = "none", edgecolors = '#FF0000', marker='D')
name_markers = fullpath_spec + 'NEO_markers_' + str(today.year) + '_' + str(today.month) + '_' + str(today.day) + '.png'
fig5.savefig(name_markers, transparent=True)

fig6 = pyplot.figure(figsize=(2.1, 1), dpi=400)
ax = fig6.gca()
pyplot.xlim(0, 2); pyplot.ylim(0, 4)
ax.axis('off')


def single_fig6_stats(num, x, y):
    pyplot.text(x, y, str(num), fontdict6)


single_fig6_stats("{:,}".format(NHATS_tot), 0.12, 1.55)  # NHATS total
single_fig6_stats("{:,}".format(blue_tot), 0.12, 2.05)  # Total trajectories blue
pyplot.text(1.75, 1.55, Blue_Range, fontdict6)

name_block = fullpath_spec + 'NEO_Block_' + str(today.year) + '_' + str(today.month) + '_' + str(today.day) + '.png'
fig6.savefig(name_block, transparent=True)


# ----------------------------- Image stacking: ----------------------------
plotted_data = Image.open(name)  # Central plot image
stats_data = Image.open(name_stats)  # Statistics data image
date_data = Image.open(name_date)  # Day of currency image
# date_Blue = Image.open(name_Blue) # Blue date range image
date_Green = Image.open(name_Green)  # Green date range image
mrkrs = Image.open(name_markers)  # Marker image
stats_yearBlock = Image.open(name_block)  # Year name block corner image
background = Image.open(fullpath_spec + 'NHATS_Accessible_NEAs_BottomLayer_2.png')  # Background - prerendered
foreground = Image.open(fullpath_spec + 'NHATS_Accessible_NEAs_TopLayer_2.png')  # Foreground - prerendered

# Paste each image onto background
background.paste(plotted_data, (237,292), plotted_data)
background.paste(stats_data, (5,608), stats_data)
background.paste(date_data, (2580,305), date_data)
# background.paste(date_Blue, (1172,1938), date_Blue)
background.paste(date_Green, (1102,2030), date_Green)
background.paste(mrkrs, (445,250), mrkrs)
background.paste(stats_yearBlock, (550,1785), stats_yearBlock)
background.paste(foreground, (0,0), foreground)
background.save(nameFin)

# Cleanup all images never to be used again
os.remove(name)
os.remove(name_stats)
os.remove(name_date)
# os.remove(name_Blue)
os.remove(name_Green)
os.remove(name_markers)
os.remove(name_block)
# This leaves only the final desired image on machine
