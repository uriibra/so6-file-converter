import pandas as pd

def add_country_flow(i):
    i['country_flow'] = i.apply(lambda row: sorted([row['origin'][0:2], row['destination'][0:2]]) , axis=1)
    i['country_flow'] = i['country_flow'].str[0] + '_' + i['country_flow'].str[-1]
    i['country_flow'] = i['country_flow'].replace('EI_GC', 'EG_GC') #add ireland to eg flow
    return i 

def so6_to_df(route): #line x line as so6
    columns = ['segment_id', 'origin', 'destination', 'ac_type', 'time_ini_seg', 'time_end_seg', 'fl_ini', 'fl_end', 'status', 'callsign',\
               'date_ini', 'date_end', 'lat_ini', 'lon_ini', 'lat_end', 'lon_end', 'flightid', 'sequence', 'segment_length', 'segment_color']
    data = []
    
    with open(route) as doc:
        for line in doc:
            line = line.split()
            data.append(line)
    
    df = pd.DataFrame(data, columns=columns)
    
    #transform coordinates into decimal
    df['lat_ini'] = df['lat_ini'].astype(float)/60 
    df['lat_end'] = df['lat_end'].astype(float)/60
    df['lon_ini'] = df['lon_ini'].astype(float)/60
    df['lon_end'] = df['lon_end'].astype(float)/60
    
    #transform numeric values into numeric
    df['segment_length'] = df['segment_length'].astype(float)
    df['fl_ini']  = df['fl_ini'].astype(int)
    df['fl_end']  = df['fl_end'].astype(int)
    df['status']  = df['status'].astype(int)
    df['sequence']  = df['sequence'].astype(int)
    df['segment_color']  = df['segment_color'].astype(int)
    
    #create new column total_distance
    dist_sum = df.groupby('flightid')['segment_length'].sum().reset_index()
    df = df.merge(dist_sum, on='flightid', suffixes=('', '_sum'))
    df.rename(columns={'segment_length_sum': 'flown_distance'}, inplace=True)
    df1 = add_country_flow(df)
    return df1
    
def so6_to_df_simple(route): #one line x flight list with lat, lon, alt, no segments, simplifyed
    columns = ['callsign', 'flightid', 'origin', 'destination', 'lat', 'long', 'alt', 'time', 'date', 'total_distance', 'ac_type']
    data = []
    last = ''
    with open(route) as doc:
        tmp = []
        for line in doc:
            line = line.split()
            if line[16] != last:
                if len(tmp)>0: data.append(tmp)
                tmp = []
                tmp.append(line[9])
                tmp.append(line[16])
                tmp.append(line[1])
                tmp.append(line[2])
                tmp.append([float(line[12])/60])
                tmp.append([float(line[13])/60])
                tmp.append([int(line[6])])
                tmp.append([line[4]])
                tmp.append([line[10]])
                tmp.append(float(line[18]))
                tmp.append(line[3])
                last = line[16]

            else:
                tmp[4].append(float(line[12])/60)
                tmp[5].append(float(line[13])/60)
                tmp[6].append(int(line[6]))
                tmp[7].append(line[4])
                tmp[8].append(line[10])
                tmp[9]+= float(line[18])

    df = pd.DataFrame(data, columns=columns)
    df1 = add_country_flow(df)
    return df1

def so6_to_df_waypoints(route): #structured x waypints, one line x wpt
    columns = ['waypoint', 'callsign', 'flightid', 'origin', 'destination', 'lat', 'lon', 'alt', 'time', 'date']
    data = []
    with open(route) as doc:
        for line in doc:
            tmp = [] #first wpt
            line = line.split()
            wpt1, wpt2 = line[0].split("_")
            tmp.append(wpt1)
            tmp.append(line[9]) #callsign
            tmp.append(line[16]) #flightid
            tmp.append(line[1]) #ori
            tmp.append(line[2]) #dest
            tmp.append(float(line[12])/60) #lat
            tmp.append(float(line[13])/60) #lon
            tmp.append(int(line[6])) #alt
            tmp.append(line[4]) #time
            tmp.append(line[10]) #date
            data.append(tmp)
            
            tmp = [] #secondwpt
            tmp.append(wpt2)
            tmp.append(line[9]) #callsign
            tmp.append(line[16]) #flightid
            tmp.append(line[1]) #ori
            tmp.append(line[2]) #dest
            tmp.append(float(line[14])/60) #lat
            tmp.append(float(line[15])/60) #lon
            tmp.append(int(line[7])) #alt
            tmp.append(line[5]) #time
            tmp.append(line[11]) #date
            data.append(tmp)
    
    df = pd.DataFrame(data, columns=columns)
    df1 = add_country_flow(df)
    
    return df1.drop_duplicates()


    
    
    
    
