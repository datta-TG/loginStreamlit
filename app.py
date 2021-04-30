import requests 
import streamlit as st
import SessionState
import streamlit.components.v1 as components
import json
import time
import pandas as pd
from GPT3_Main import ice
_material_login = components.declare_component(
    "material_login", url="http://3.133.44.166:3001/",
)

def scrap(link):
    position = []
    company = []
    name = []
    lugar = []
    con = 0
    for j in link:
        
        time.sleep(10)
        print("out time")
        #url = "https://google-search3.p.rapidapi.com/api/v1/search/q=" + link
        url = "https://google-search3.p.rapidapi.com/api/v1/search/q=" + j


        headers = {'x-rapidapi-key': "6585b12e00mshf87bb201b8c187dp112b28jsn8ed861800eb3",'x-rapidapi-host': "google-search3.p.rapidapi.com"}

        response = requests.request("GET", url, headers=headers)
        print(url)
        print(response.text)
        dic = json.loads(response.text)

    
#         dic = {"results":[{"title":"Maria Guasch - Director of F&A - Typeform | LinkedIn","link":"https","description":"Barcelona y alrededores, España","g_review_stars":"Barcelona y alrededores, España"}],"image_results":[],"total":1,"answers":[],"ts":1.2}
        if len(dic["results"]) > 0:
            for i in dic["results"]:
                di = i
                break
            ndc = di["title"]
            ndc = ndc.replace("| LinkedIn","").replace(".","")
            ndc = ndc.replace("–","-")
            ndc = ndc.replace("and","").strip().split(" - ")
            #st.write(ndc)
            try:
                name.append(ndc[0])
            except:
                name.append(None)
            try:
                position.append(ndc[1])
            except:
                position.append(None)
            try:
                place = di["description"]
                #st.write(place)
                if (len(place)>40):
                    lugar.append(place[:40])
                else:
                    lugar.append(place)
            except:
                lugar.append(None)
            if len(ndc)>2:
                if ndc[2] == "LinkedIn":
                    company.append(None)
                else:
                    company.append(ndc[2])

            else:
                company.append(None)
        else:
            company.append(None)
            name.append(None)
            position.apend(None)
            lugar.append(None)
        
    con+=1    
    return [position,company,lugar,name]


def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(
        csv.encode()
    ).decode()  # some strings <-> bytes conversions necessary here
    return f'<a href="data:file/csv;base64,{b64}" download="myfilename.csv">Download csv file</a>'




def addc(cat,diccs,pred,op):
    cat = ['Time and position', 'Company News', 'Location', 'Education']
    ch = []
    op = sorted(op)
    for i in op:
        ch.append(cat[i-1])
    for k in range(len(diccs['Option'])):
        var = []
        for i in pred:
            var.append(i[k])

        diccs["category: "+str(ch[k])] = var
    del diccs['Option']
    return diccs




def rerun():
    raise st.script_runner.RerunException(st.script_request_queue.RerunData(None))

def material_login(title, key=None):
    return _material_login(title=title, key=key)


session_state = SessionState.get(isLoggedIn=False,x=[],df=[])

USERNAME = "a@a.com"
PASSWORD = "t"

if session_state.isLoggedIn:
    pass
else:
    logged_in_data = material_login("Insert your account")

    if bool(logged_in_data) and logged_in_data['username'] == USERNAME and logged_in_data['password'] == PASSWORD:
        session_state.isLoggedIn = True
        rerun()
        
if session_state.isLoggedIn:
    st.header("TEST GPT3 LinkedIn")
    st.subheader("HOW TO START")
    st.markdown(":small_red_triangle_down: Put the name, the company and the time of the user and then press the predict button.")
    genre = st.sidebar.radio("OPTIONS",('Link', 'Upload csv file'))
    if genre == 'Link':
        session_state.fl2 = []
        linkd = st.text_input("put the name from linkedin profile")
        if linkd:
            if st.button('Scrap'):
                p =linkd.find("w.")
                with st.spinner('Wait...'):
                    session_state.x = scrap([linkd[(p+2):]])
                st.success('Done!')
                
    else:
        input_buffer = st.file_uploader("Upload a file", type=("csv"))
        if input_buffer:
            dfa= pd.read_csv(input_buffer, sep=',',prefix=None)
            dfa.columns = ['LINKS']
            p1 = dfa["LINKS"].values.tolist()
            value = []
            for j in p1:
                p =j.find("w.")
                value.append(j[(p+2):])
            if st.button('Scrap'):
                with st.spinner('Wait...'):
                    session_state.x = scrap(value)
                st.success('Done!')
    
    if session_state.x:
        va = session_state.x
        diccs= {'Name' : va[3], 'Company' : va[1] ,'Position': va[0],'Location':va[2]}
        df = st.table(diccs)
        profiles = []
        for i in range(len(session_state.x[0])):
            profiles.append("Profile "+str(i+1))
        f = st.sidebar.selectbox(label="PROFILES",options=profiles,index=0)
        index = profiles.index(f)   
        st.subheader("Name: "+va[3][index])
        position = st.text_input("Put the position",va[0][index])
        company = st.text_input("Put the company",va[1][index])
        location = st.text_input("Put the location",va[2][index])
        cat = ['Time and position', 'Company News', 'Location', 'Education']
        options = st.multiselect('Choose the categories',cat,'Time and position')
        op = []
        for k in options:
            if k in cat:
                idx = cat.index(k)
                op.append(idx+1)
        diccs['Option'] = sorted(op)
        
        ############# PREDICCTION ###################
        
        
        if st.button('Predict',key='start'):  ##predict indiv
            if op:
                dicc= {'Name' : [va[3][index]], 'Company' :[ company],'Position': [position], 'Time_in_position': ["None"] ,
                       'Location':[location],'Education': ["None"],'Option':sorted(op)}
               # st.write(dicc)
                with st.spinner('Wait...'):
                    predi = ice(dicc)
                # st.write(predi)
                st.success('Done!')
               # st.write(predi)
                diccs = addc(cat,dicc,predi,op)
                session_state.df = pd.DataFrame(diccs)
                st.write(session_state.df)
            else:
                st.error("Please choose one category")