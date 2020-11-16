from dateutil.relativedelta import *
from datetime import date, datetime

#
# CALCULATE AGE FROM DOB
#

def get_age_from_dob(dob, only_years = False):
    today = date.today()
    dob = datetime.strptime(dob,"%Y-%m-%d")
    age = relativedelta(today, dob)
    
    if only_years:
        return age.years    
    return age
    
    
#
# CALCULATE YEAR OF BIRTH FROM AGE
#
    
def get_birth_year_from_age(age):
    today = date.today()
    year_of_birth = datetime.now() - relativedelta(years=int(age))
        
    return year_of_birth.strftime("%Y")
 
#
# CALCULATE YEAR-01-01 OF BIRTH FROM AGE
#
 
def get_birth_full_from_age(age):

    today = date.today()
    year_of_birth = datetime.now() - relativedelta(years=int(age))
        
    yr = year_of_birth.strftime("%Y")
    
    return "{}-{}-{}".format(yr,"01","01")  