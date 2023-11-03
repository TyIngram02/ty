import requests
import tls_client
import csv

from flask import Flask, render_template

app = Flask(__name__)
w = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'no-cache',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    }

requests = tls_client.Session(
        client_identifier="chrome112",
    )

prizepicks = requests.get('https://api.prizepicks.com/projections').json()

underdog = requests.get("https://api.underdogfantasy.com/beta/v3/over_under_lines").json()

pplist = []
udlist = []
table_data = []
def prizepicks_nba():
    for included in prizepicks['included']:
    #get id we will match this later o
        PPname_id = included['id']
        #getting prizepicks prop name
        PPname = included['attributes']['name']
        if 'team' in included['attributes']:
                teamname = included['attributes']['team']
        
        #nested loop must go thru data
        for data1 in prizepicks['data']:
            #ppid will match this to id to get correct information
            PPid = data1['relationships']['new_player']['data']['id']
            #getting pp line //ex map 1-2 kills
            PPprop_value = data1['attributes']['line_score']
            #gettting value// ex 7.5 kills
            PPprop_type = data1['attributes']['stat_type']
            
            if 'league' in included['attributes']:
                Sport_type = included['attributes']['league']
                #filtering esports props only
            if PPprop_type == 'Points' and PPname_id == PPid and Sport_type =='NBA':
                PPprop_type= 'NBA Points'
            elif PPprop_type == 'Rebounds' and PPname_id == PPid and Sport_type =='NBA':
                PPprop_type= 'NBA Rebounds'
            elif PPprop_type == 'Assists' and PPname_id == PPid and Sport_type =='NBA':
                PPprop_type= 'NBA Assists'
            elif PPprop_type == 'FG Made' and PPname_id == PPid and Sport_type =='NBA':
                PPprop_type= 'NBA FG Made'
            elif PPprop_type == 'Pts+Rebs+Asts' and PPname_id == PPid and Sport_type =='NBA':
                PPprop_type =='NBA PRA'
            elif PPprop_type == '3-PT Attempted' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type == 'NBA 3-point attempts'
            elif PPprop_type == 'Free Throws Made' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type == 'NBA FT Made'
            elif PPprop_type == 'FG Attempted' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type == 'NBA FG Attempts'
            elif PPprop_type == 'FG Missed' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type == 'NBA FG Missed'
            elif PPprop_type == 'Pts+Rebs' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type == 'NBA PR'
            elif PPprop_type == 'Pts+Asts' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type == 'NBA PA'
            elif PPprop_type == '3-PT Made' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type == 'NBA 3pt made'
            elif PPprop_type == 'Blocked Shots' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type == 'NBA Blocked Shots'
            elif PPprop_type == 'Steals' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type = 'NBA Steals'
            elif PPprop_type == 'Rebs+Asts' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type = 'NBA RA'
            elif PPprop_type == 'Blks+Stls' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type = 'NBA Blocks & Steals'
            elif PPprop_type == 'Turnovers' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type = 'NBA Turnovers'
            elif PPprop_type == 'Fantasy Score' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type = 'NBA FS'
            elif PPprop_type == 'Defensive Rebounds' and PPname_id == PPid and Sport_type == 'NBA':
                PPprop_type == 'NBA Defensive Rebounds'
            if PPprop_type == 'NBA Points' or PPprop_type == 'NBA Rebounds' or PPprop_type == 'NBA Assists' or PPprop_type =='NBA PRA' or PPprop_type =='NBA 3-point attempts' or PPprop_type == 'NBA FT Made' or PPprop_type == 'NBA FT Made' or PPprop_type == 'NBA FG Attempts' or PPprop_type == 'NBA PR' or PPprop_type == 'NBA PA' or PPprop_type == 'NBA PA' or PPprop_type == '3pt made' or PPprop_type == 'NBA Blocked Shots' or PPprop_type == 'NBA Blocks & Steals' or PPprop_type == 'NBA RA' or PPprop_type == 'NBA Turnovers' or PPprop_type == 'NBA FS':
                ppdic = {'Name': PPname, 'Stat':PPprop_type, 'Line': PPprop_value}
                pplist.append(ppdic)
    print(pplist)
    
        



def underdog_nba():
    for appearances in underdog["over_under_lines"]:
        for items in underdog['appearances']:
                #filtering for sport type
                underdog_sport = ''.join(appearances["over_under"]["title"].split()[0:1])
                #title is equal to players name/// using split method to only get first name
                underdog_title = ' '.join(appearances["over_under"]["title"].split()[0:2])
                #display stat is equal to prop// ex map 1 kills
                UDdisplay_stat = f"{appearances['over_under']['appearance_stat']['display_stat']}"          
                #stat value is equal to the prop value ex 5.5 /// so on
                UDstat_value = appearances['stat_value']
                appearancesid = appearances['over_under']['appearance_stat']['appearance_id']
                id = items['id']
                if appearancesid == id:
                    matchid = items['match_id']
                    matchtype = items['match_type']
        for items2 in underdog['games']:
            new_id = items2['id']
            if matchid == new_id:
                time = items2['scheduled_at']
                sport = items2['sport_id']
        if UDdisplay_stat == 'Points' and matchtype == 'Game' and sport == 'NBA':
             UDdisplay_stat = 'NBA Points'
        elif UDdisplay_stat == 'Rebounds' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA Rebounds'
        elif UDdisplay_stat == 'Assists' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA Assists'
        elif UDdisplay_stat == 'Pts + Rebs + Asts' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA PRA'
        elif UDdisplay_stat == 'Pts + Rebs + Asts' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA PRA'
        elif UDdisplay_stat == '3\'s Attempted' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA 3-point attempts'
        elif UDdisplay_stat == 'FT Made' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA FT Made'
        elif UDdisplay_stat == 'FG Attempted' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA FG Attempts'
        elif UDdisplay_stat == 'Points + Rebounds' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA PR'
        elif UDdisplay_stat == 'Points + Assists' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA PA'
        elif UDdisplay_stat == '3-Pointers Made' and matchtype == 'Game' and sport =='NBA':
            UDdisplay_stat = 'NBA 3pt made'
        elif UDdisplay_stat == 'Block' and matchtype == 'Game' and sport =='NBA':
            UDdisplay_stat = 'NBA Blocked Shots'
        elif UDdisplay_stat == 'Blocks + Steals' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA Blocks & Steals'
        elif UDdisplay_stat == 'Rebounds + Assists' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA RA'
        elif UDdisplay_stat == 'Turnovers' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat ='NBA Turnovers'
        elif UDdisplay_stat =='Fantasy Points' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA FS'
        elif UDdisplay_stat =='Defensive Rebounds' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA Defensive Rebounds'
        elif UDdisplay_stat =='Offensive Rebounds' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA Offensive Rebounds'
        elif UDdisplay_stat =='Offensive Rebounds' and matchtype == 'Game' and sport == 'NBA':
            UDdisplay_stat = 'NBA Offensive Rebounds'
        if UDdisplay_stat == 'NBA Points' or UDdisplay_stat == 'NBA Rebounds' or UDdisplay_stat == 'NBA Assists' or UDdisplay_stat =='NBA PRA' or UDdisplay_stat =='NBA 3-point attempts' or UDdisplay_stat == 'NBA FT Made' or UDdisplay_stat == 'NBA FT Made' or UDdisplay_stat == 'NBA FG Attempts' or UDdisplay_stat == 'NBA PR' or UDdisplay_stat == 'NBA PA' or UDdisplay_stat == 'NBA PA' or UDdisplay_stat == 'NBA 3pt made' or UDdisplay_stat == 'NBA Blocked Shots' or UDdisplay_stat == 'NBA Blocks & Steals' or UDdisplay_stat == 'NBA RA' or UDdisplay_stat == 'NBA Turnovers' or UDdisplay_stat == 'NBA FS':
            uddic = {'Name': underdog_title, 'Stat': UDdisplay_stat, 'Line': UDstat_value}
            udlist.append(uddic)
      


def compare():
    for udn in udlist:
        for ppn in pplist:
            if udn["Name"] == ppn["Name"] and udn['Stat'] == ppn['Stat']:
                average = (float(ppn['Line']) + float(udn['Line'])) /2
                dif = abs(float(udn['Line']) - abs(float(ppn['Line'])))
                ndif = round(dif, 2)
                perc = dif/average
                finalperc = perc * 100
                finalperc = round(finalperc, 2)
                final = {"Name": udn["Name"] ,"Stat":udn["Stat"], "UD": float(udn["Line"]), "PP": float(ppn["Line"]), "Dif": ndif, 'Per':finalperc}
               
                table_data.append(final)
                def sort_key(d):
                    return d["Per"]
                table_data.sort(key=sort_key, reverse=True)
    headings = ("Name","Stat","PP","UD","DIF", 'PERC')
    csv_file_path = "compare.csv"

    # Write table_data to a CSV file
    with open(csv_file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        
        # Write the headers
        csv_writer.writerow(headings)
        
        # Write the data
        for row in table_data:
            csv_writer.writerow([row['Name'], row['Stat'], row['PP'], row['UD'], row['Dif'],row['Per']])






app = Flask(__name__)

# Your existing code here

# Define an endpoint to access your functionality
@app.route('/compare', methods=['GET'])
def compare_endpoint():
    prizepicks_nba()
    underdog_nba()
    compare()
    headings = ("Name","Stat","PP","UD","DIF", 'PERC')
    return render_template('compare.html', headers=headings, table_data=table_data)


if __name__ == '__main__':
    app.run(debug=True)
