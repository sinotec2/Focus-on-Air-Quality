#kuang@DEVP /nas1/ecmwf/CAMS/CAMS_global_atmospheric_composition_forecasts/2022
#$ cat get_All.py
#!/opt/miniconda3/envs/gribby/bin/python
import cdsapi
import sys
dt=sys.argv[1]
hr=sys.argv[2]
nm=sys.argv[3]
c = cdsapi.Client()
kk= ['137', '135', '133', '129', '125', '122', '120', '117', '114', '112', '110', '107', '105',
 '101', '96', '92', '87', '83', '78', '73', '67', '61', '56', '51']
SPECs =['carbon_monoxide','ethane', 'formaldehyde', 'isoprene', 'nitrogen_dioxide', 'nitrogen_monoxide', 'propane', 'sulphur_dioxide' ]
SPECs+=['ozone', 'ammonium', 'nitrate', 'olefins', 'organic_nitrates', 'paraffins']
PARTs =[
            'dust_aerosol_0.03-0.55um_mixing_ratio', 'dust_aerosol_0.55-0.9um_mixing_ratio', 'dust_aerosol_0.9-20um_mixing_ratio',
            'hydrophilic_black_carbon_aerosol_mixing_ratio', 'hydrophilic_organic_matter_aerosol_mixing_ratio', 'hydrophobic_black_carbon_aerosol_mixing_ratio',
            'hydrophobic_organic_matter_aerosol_mixing_ratio', 'nitric_acid', 'peroxyacetyl_nitrate',
            'sea_salt_aerosol_0.03-0.5um_mixing_ratio', 'sea_salt_aerosol_0.5-5um_mixing_ratio', 'sea_salt_aerosol_5-20um_mixing_ratio',
            'sulphate_aerosol_mixing_ratio',
        ]
All=SPECs+PARTs
i=int(nm)
All=All[9*(i-1):9*i] #i=1,2,3
c.retrieve(
    'cams-global-atmospheric-composition-forecasts',
    {
        'date': dt+'/'+dt,
        'type': 'forecast',
        'format': 'grib',
        'time': hr,
        'model_level': kk,
        'variable': All,
        'leadtime_hour': [str(i) for i in range(0,121,3)],
        'area': [ 55, 50, -5, 180, ],
    },
    'allEA_'+nm+'.grib')
