import json

ss='''
"let’s think step by step.",
"sub1" : "(join (r opera.opera_production.designers) the telephone / the medium)",
"sub2" : "(join (r opera.opera_designer_gig.design_role) sub1)",
"sub3" : "(and opera.opera_designer_role sub2)",
"sub1-q1" : "opera production designers the telephone/the medium",
"sub2-q2" : "opera designer gig design role of the telephone/the medium",
"sub3-q3" : "what is the opera designer role of the telephone/the medium?",
"output" : "what is the opera designer role of the telephone/the medium?"
'''
ss=ss.split('''"let’s think step by step.",''')[-1]
ss="{"+ss+"}"
print(ss)
print(json.loads(ss))