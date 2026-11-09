import re, difflib, numpy as np, pandas as pd

def norm_state(s):
    t=str(s).lower().replace("&","and"); t=re.sub(r"[^a-z]","",t)
    alias={"chattisgarh":"chhattisgarh","keralam":"kerala","uttrakhand":"uttarakhand","orissa":"odisha","pondicherry":"puducherry",
           "nctofdelhi":"delhi","andamanandnicobar":"andamanandnicobarislands","dadraandnagarhavelianddamananddiu":"dnhdd",
           "dadranagarhavelianddamandiu":"dnhdd","dadraandnagarhaveli":"dnhdd","damananddiu":"dnhdd","tamilnadu":"tamilnadu","uttarpradesh":"uttarpradesh","uttarprdesh":"uttarpradesh","maharastra":"maharashtra","thedadraandnagarhavelianddamananddiu":"dnhdd","dadraandnagarhavelianddamananddiu":"dnhdd"}
    return alias.get(t,t)

def pretty_state(k):
    return {"dnhdd":"Dadra and Nagar Haveli and Daman and Diu","andamanandnicobarislands":"Andaman and Nicobar Islands","jammuandkashmir":"Jammu and Kashmir"}.get(k,k)

DALIAS={"ballari":"bellary","belagavi":"belgaum","kalaburagi":"gulbarga","vijayapura":"bijapur","mysuru":"mysore","tumakuru":"tumkur",
 "shivamogga":"shimoga","chikkamagaluru":"chikmagalur","chamarajanagara":"chamarajanagar","bengaluruurban":"bangalore",
 "bengalururural":"bangalorerural","ramanagara":"ramanagar","gurugram":"gurgaon","prayagraj":"allahabad","ayodhya":"faizabad",
 "ahmedabad":"ahmadabad","dahod":"dohad","mahesana":"mehsana","kutch":"kachchh","panchmahal":"panchmahals","sabarkantha":"sabarkantha",
 "kanpurnagar":"kanpurnagar","kanpurdehat":"kanpurdehat","lakhimpurkheri":"lakhimpurkheri","santravidasnagarbhadohi":"santravidasnagar",
 "bhadohi":"santravidasnagar","raebareli":"raebareli","ysrkadapa":"ysr","kadapa":"ysr","cuddapah":"ysr","spsrnellore":"sripottisriramulunellore",
 "nellore":"sripottisriramulunellore","visakhapatnam":"visakhapatnam","anantapuramu":"anantapur","ananthapuramu":"anantapur",
 "east godavari":"eastgodavari","purbabardhaman":"purbabardhaman","bardhaman":"purbabardhaman","burdwan":"purbabardhaman","medinipurwest":"paschimmedinipur",
 "westmidnapore":"paschimmedinipur","eastmidnapore":"purbamedinipur","medinipureast":"purbamedinipur","kamrupmetropolitan":"kamrupmetro","kamrupmetro":"kamrupmetro",
 "sribhadradricothagudem":"bhadradrikothagudem","bhadradrikothagudem":"bhadradrikothagudem","jagitial":"jagtial","jangaon":"jangoan","rangareddy":"rangareddy",
 "yadadribhuvanagiri":"yadadribhuvanagiri","bhadradri":"bhadradrikothagudem","kamareddy":"kamareddy","sahibzadaajitsinghnagar":"sasnagarmohali","sasnagar":"sasnagarmohali","mohali":"sasnagarmohali",
 "nawanshahr":"shahidbhagatsinghnagar","sbsnagar":"shahidbhagatsinghnagar","firozepur":"firozpur","ferozepur":"firozpur","muktsar":"sribmuktsarsahib","sribmuktsarsahib":"sribmuktsarsahib",
 "ri_bhoi":"ribhoi","kanyakumari":"kanniyakumari","thoothukudi":"thoothukkudi","tuticorin":"thoothukkudi","thiruvallur":"tiruvallur","villupuram":"viluppuram","tiruchirappalli":"tiruchirappalli","trichy":"tiruchirappalli",
 "thiruvananthapuram":"thiruvananthapuram","kasaragod":"kasaragod","pathanamthitta":"pathanamthitta","alappuzha":"alappuzha","palakkad":"palakkad","kozhikode":"kozhikode","wayanad":"wayanad","kannur":"kannur",
 "bandipora":"bandipore","baramulla":"baramula","budgam":"badgam","shopian":"shupiyan","kupwara":"kupwara","leh":"leh","kargil":"kargil","ladakh":"leh",
 "janjgirchampa":"janjgirchampa","kawardha":"kabeerdham","kabirdham":"kabeerdham","dantewada":"dakshinbastardantewada","bijapurcg":"bijapur","narayanpur":"narayanpur",
 "gaurelapendramarwahi":"gaurelapendramarwahi","mahendragarh":"mahendragarh","nuh":"mewat","mewat":"mewat","charkhidadri":"charkhidadri","jhunjhunun":"jhunjhunu","chittorgarh":"chittaurgarh","dholpur":"dhaulpur","sawaimadhopur":"sawaimadhopur",
 "sriganganagar":"ganganagar","hanumangarh":"hanumangarh","bhilwara":"bhilwara","hoshangabad":"hoshangabad","narmadapuram":"hoshangabad","khargone":"westnimar","westnimar":"westnimar","khandwa":"eastnimar","eastnimar":"eastnimar",
 "singrauli":"singrauli","agarmalwa":"agarmalwa","alirajpur":"alirajpur","burhanpur":"burhanpur","anuppur":"anuppur","ashoknagar":"ashoknagar","gondia":"gondiya","raigad":"raigarh","raigarh":"raigarh","ahmednagar":"ahmadnagar","ahilyanagar":"ahmadnagar","chhatrapatisambhajinagar":"aurangabad","osmanabad":"osmanabad","dharashiv":"osmanabad","buldana":"buldhana","gadchiroli":"gadchiroli","sindhudurg":"sindhudurg","mumbaisuburban":"mumbaisuburban",
 "nicobars":"nicobars","northmiddleandaman":"northandmiddleandaman","southandaman":"southandaman","dimapur":"dimapur","kohima":"kohima","kiphire":"kiphire","longleng":"longleng","mon":"mon","noklak":"noklak","peren":"peren","phek":"phek","tuensang":"tuensang","wokha":"wokha","zunheboto":"zunheboto",
 "angul":"anugul","baleshwar":"balasore","baleswar":"balasore","bargarh":"baragarh","debagarh":"deogarh","jagatsinghapur":"jagatsinghpur","jajapur":"jajpur","kendujhar":"keonjhar","nabarangapur":"nabarangpur","sonepur":"subarnapur","subarnapur":"subarnapur","sundargarh":"sundargarh","boudh":"baudh","khordha":"khurda","khurda":"khurda"}

def norm_dist(s):
    t=str(s).lower(); t=re.sub(r"\(.*?\)","",t); t=t.replace("&","and"); t=re.sub(r"\b(district|dist)\b","",t); t=re.sub(r"[^a-z]","",t)
    return DALIAS.get(t,t)

def match_districts(src, nf, src_state="state_k", src_dist="dist_raw", thr=0.84, margin=0.04):
    """Map unique (state,district) pairs in src onto NFHS (state,district). Returns DataFrame with method and score."""
    nf=nf.copy(); nf["dk"]=nf["district"].map(norm_dist)
    rows=[]
    for (st,d),_ in src.groupby([src_state,src_dist]):
        dk=norm_dist(d); pool=nf[nf.state_k==st]
        if pool.empty: rows.append((st,d,None,"no_state",0.0)); continue
        ex=pool[pool.dk==dk]
        if len(ex)==1: rows.append((st,d,ex.district.iloc[0],"exact",1.0)); continue
        sc=sorted(((difflib.SequenceMatcher(None,dk,k).ratio(),nm) for k,nm in zip(pool.dk,pool.district)),reverse=True)
        if sc and sc[0][0]>=thr and (len(sc)==1 or sc[0][0]-sc[1][0]>=margin): rows.append((st,d,sc[0][1],"fuzzy",round(sc[0][0],3)))
        else: rows.append((st,d,None,"unmatched",round(sc[0][0],3) if sc else 0.0))
    m=pd.DataFrame(rows,columns=["state_k","dist_raw","nfhs_district","method","score"])
    # one NFHS district may only take its best source district
    ok=m[m.nfhs_district.notna()].sort_values(["state_k","nfhs_district","score"],ascending=[True,True,False])
    dup=ok.duplicated(["state_k","nfhs_district"],keep="first"); m.loc[dup[dup].index,["nfhs_district","method"]]=[None,"conflict"]
    return m
