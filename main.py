import os
import openai
import json
import time

openai.api_key = "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"  #


def get_prompt_3(prompt_file, sub_type):
    prompts_1 = '''
                   "input":"(AND religion.place_of_worship (JOIN religion.place_of_worship.religion ismailism))"
                        "sub1":"(JOIN religion.place_of_worship.religion ismailism)",
                        "sub2":"(AND religion.place_of_worship (JOIN religion.place_of_worship.religion ismailism))",
                        "sub1-q1":"the place of worship in the ismailism religion",
                        "sub2-q2":"what is the name of the place of worship in the ismailism religion?",
                        "output" :"what is the name of the place of worship in the ismailism religion?"
                   "input":"(AND comic_books.comic_book_series (JOIN (R comic_books.comic_book_genre.comic_book_series_in_this_genre) (JOIN (R comic_books.comic_book_story.genre) Case of the Namesake Murders)))"
                        "sub1":"(JOIN (R comic_books.comic_book_story.genre) Case of the Namesake Murders)",
                        "sub2":"(JOIN (R comic_books.comic_book_genre.comic_book_series_in_this_genre) (JOIN (R comic_books.comic_book_story.genre) Case of the Namesake Murders))",
                        "sub3":"(AND comic_books.comic_book_series (JOIN (R comic_books.comic_book_genre.comic_book_series_in_this_genre) (JOIN (R comic_books.comic_book_story.genre) Case of the Namesake Murders)))",
                        "sub1-q1":"genre of comic book case of the namesake murders",
                        "sub2-q2":"same genre with comic book case of the namesake murders",
                        "sub3-q3":"case of the namesake murders is the same genre as what comic book series?",
                        "output" :"case of the namesake murders is the same genre as what comic book series?"
                   "input":"(ARGMIN food.bottled_water food.bottled_water.nitrate_content)"
                        "sub1":"(ARGMIN food.bottled_water food.bottled_water.nitrate_content)",
                        "sub1-q1":"the bottled water that has the least amount of nitrates?",
                        "output" :"the bottled water that has the least amount of nitrates?"
                   "input":"(ARGMAX physics.particle physics.particle.spin)",
                        "sub1":"(ARGMAX physics.particle physics.particle.spin)",
                        "sub1-q1":"what is the subatomic particle with the fastest spin?",
                        "output" :"what is the subatomic particle with the fastest spin?"
                   "input":"(COUNT (AND aviation.aircraft_manufacturer (JOIN organization.organization.legal_structure S.A.)))"
                        "sub1":"(JOIN organization.organization.legal_structure S.A.)",
                        "sub2":"(AND aviation.aircraft_manufacturer (JOIN organization.organization.legal_structure S.A.))",
                        "sub3":"(COUNT (AND aviation.aircraft_manufacturer (JOIN organization.organization.legal_structure S.A.)))",
                        "sub1-q1":"legal structure of s.a.",
                        "sub2-q2":"aircraft manufacturer in the legal structure of s.a.",
                        "sub3-q3":"what is the number of aircraft manufacturer in the legal structure of s.a.?",                                   
                        "output" :"what is the number of aircraft manufacturer in the legal structure of s.a.?"
                   "input":"(AND user.patrick.default_domain.warship_v1_1 (JOIN user.patrick.default_domain.warship_v1_1.struck 1970-07-01^^http://www.w3.org/2001/XMLSchema#date))"
                        "sub1":"(JOIN user.patrick.default_domain.warship_v1_1.struck 1970-07-01^^http://www.w3.org/2001/XMLSchema#date)",
                        "sub2":"(AND user.patrick.default_domain.warship_v1_1 (JOIN user.patrick.default_domain.warship_v1_1.struck 1970-07-01^^http://www.w3.org/2001/XMLSchema#date))",
                        "sub1-q1":"on 07/01/1970,warship v1.1 hit" ,                 
                        "sub2-q2":"on 07/01/1970, which warship v1.1 was hit?",                 
                        "output" :"on 07/01/1970, which warship v1.1 was hit?" 
                   "input":"(AND business.shopping_center (JOIN business.shopping_center.retail_floor_space_m_2 72000^^http://www.w3.org/2001/XMLSchema#integer))"
                        "sub1":"(JOIN business.shopping_center.retail_floor_space_m_2 72000^^http://www.w3.org/2001/XMLSchema#integer)",
                        "sub2":"(AND business.shopping_center (JOIN business.shopping_center.retail_floor_space_m_2 72000^^http://www.w3.org/2001/XMLSchema#integer))",
                        "sub1-q1":"shopping center has floor space as large as 72000?" ,                                  
                        "sub2-q2":"what is the name of a shopping center that has space as large as 72000?",                                  
                        "output" :"what is the name of a shopping center that has space as large as 72000?"
                   "input":"(AND music.genre (JOIN (R music.genre.parent_genre) (JOIN music.genre.albums confessions tour)))"
                        "sub1":"(JOIN music.genre.albums confessions tour)",
                        "sub2":"(JOIN (R music.genre.parent_genre) (JOIN music.genre.albums confessions tour))",
                        "sub3":"(AND music.genre (JOIN (R music.genre.parent_genre) (JOIN music.genre.albums confessions tour)))",
                        "sub1-q1":"the music genre albums confessions tour",
                        "sub2-q2":"the albums confessions tour is part of what parent genre",
                        "sub3-q3":"the albums confessions tour is part of what parent genre of a musical genre?",
                        "output" :"the albums confessions tour is part of what parent genre of a musical genre?"
                   '''
    prompts_2 = '''
                       "input":"(AND religion.place_of_worship (JOIN religion.place_of_worship.religion ismailism))"
                        "output" :"what is the name of the place of worship in the ismailism religion?"
                       "input":"(AND comic_books.comic_book_series (JOIN (R comic_books.comic_book_genre.comic_book_series_in_this_genre) (JOIN (R comic_books.comic_book_story.genre) Case of the Namesake Murders)))"
                        "output" :"case of the namesake murders is the same genre as what comic book series?"
                       "input":"(ARGMIN food.bottled_water food.bottled_water.nitrate_content)"
                        "output" :"the bottled water that has the least amount of nitrates?"
                       "input":"(ARGMAX physics.particle physics.particle.spin)"
                        "output" :"what is the subatomic particle with the fastest spin?"
                       "input":"(COUNT (AND aviation.aircraft_manufacturer (JOIN organization.organization.legal_structure S.A.)))"
                        "output" :"what is the number of aircraft manufacturer in the legal structure of s.a.?"
                       "input":"(AND user.patrick.default_domain.warship_v1_1 (JOIN user.patrick.default_domain.warship_v1_1.struck 1970-07-01^^http://www.w3.org/2001/XMLSchema#date))"
                        "output" :"on 07/01/1970, which warship v1.1 was hit?"
                       "input":"(AND business.shopping_center (JOIN business.shopping_center.retail_floor_space_m_2 72000^^http://www.w3.org/2001/XMLSchema#integer))"
                        "output" :"what is the name of a shopping center that has space as large as 72000?"
                       "input":"(AND music.genre (JOIN (R music.genre.parent_genre) (JOIN music.genre.albums confessions tour)))"
                        "output" :"the albums confessions tour is part of what parent genre of a musical genre?"
                '''
    if sub_type == -1:
        return prompts_2
    return prompts_1


def get_prompt_2(prompt_file, sub_type):
    with open(prompt_file, "r", encoding='utf-8') as f:
        datas = json.load(f)
        f.close()
    prompt_lst = []
    for _, data in datas.items():
        if sub_type == -1:
            prompt_lst.append('''"input": "''' + data["input"] + '''",''')
            prompt_lst.append('''"output": "''' + data["output"] + '''"''')
        else:
            for key, value in data.items():
                if key != "output":
                    prompt_lst.append('''"''' + key + '''" : "''' + data[key] + '''",''')
                    if key == "input":
                        prompt_lst.append('''"Let’s think step by step."''')
                else:
                    prompt_lst.append('''"''' + key + '''" : "''' + data[key] + '''"''')
    return "\n".join(prompt_lst)


def get_prompt(prompt_file, sub_type):
    with open(prompt_file, "r", encoding='utf-8') as f:
        datas = json.load(f)
        f.close()
    prompt_lst = []
    for _, data in datas.items():
        if sub_type == -1:
            prompt_lst.append("input:" + data["input"])
            prompt_lst.append("output:" + data["output"])
        else:
            for key, value in data.items():
                prompt_lst.append(key + ":" + data[key])
    return "".join(prompt_lst)


def generate_sentence(data_file, prompt_file, target_file, limit_num, sub_type=-1):  # sub_type =-1 input:output
    prompts = get_prompt_2(prompt_file, sub_type)
    with open(data_file, "r", encoding='utf-8') as f:
        datas = json.load(f)
        f.close()
    if not os.path.exists(target_file):
        with open(target_file, "w", encoding='utf-8') as f:
            f.close()
            result = {}
    else:
        with open(target_file, "r", encoding='utf-8') as f:
            result = json.load(f)
            f.close()
    i = 0
    try:
        for qid, q in datas.items():
            i += 1
            if i > limit_num:
                break
            if qid in result:
                continue
            print(i, "-------", qid)
            sen = ''.join(['''"input": "''', q, '''",'''])
            data = ''.join([prompts, sen])
            response = openai.Completion.create(model="text-davinci-003", prompt=data, max_tokens=1000, temperature=0)
            # text = response.choices[0].text
            text = response.choices[0].text.split('''"Let’s think step by step."''')[-1]
            text = "{" + text + "}"
            print(text)
            result[qid] = json.loads(text)["output"].lower()
            # result[qid]= text.split('''output" : ''')[-1].lower()
            print(result[qid])
            time.sleep(3)
    except Exception as e:
        print(e)
    g = open(target_file, "w", encoding='utf-8')
    json.dump(result, g, indent=2)
    g.close()


if __name__ == '__main__':
    limit_num = 500
    data_file = "./data/dev_sp_name.json"
    prompt_file = "./handlabel/prompt_data_cluster_kmeans.json"
    target_file = "./result/dev_genarate_question_davinci_kmeans_sub_short_first_ls.json"
    generate_sentence(data_file, prompt_file, target_file, limit_num, 1)
