import openai
from flask import Flask, request, jsonify, json
from bson import json_util
from flask_cors import CORS
import pymongo
app = Flask(__name__)

CORS(app)

openai.organization = "org-0MLEyOLltuxIvGpSl7Op2CH8"
openai.api_key = "your api key"


@app.route("/questions", methods=["POST", "GET"])
def postQuestionChatGpt():
    try:
        if (request.method == 'POST'):
            mess = request.json["promptMessage"]
            length = request.json["len"]
            arr = openai.Completion.create(
                model="text-davinci-003",
                prompt=mess,
                max_tokens=1500,
                temperature=0
            )
            print("1111")
            print(arr)
            
            data = arr.choices[0].text
            print(data)
            if (len(arr.choices[0]) > 0):
                if (arr.choices[0].text):
                    array = data.split("\n\n")[1:]
                    if (len(array) == int(length)*2):
                        print("printed with  space ")
                        print("arr of questions")
                        print(array)
                        res = []
                        print(len(array))
                        for i in range(0, len(array), 2):
                            questionArr = array[i].split("\n")
                            print(questionArr)
                            res.append({
                                "question": questionArr[0],
                                "optionA": questionArr[1],
                                "optionB": questionArr[2],
                                "optionC": questionArr[3],
                                "optionD": questionArr[4],
                                "answer": array[i+1].split("Answer: ")[1]
                            })
                        print(res)
                        return jsonify({'data': res})
                    else:
                        res = []
                        if(len(array)==int(length)):
                            print("printed with no space ")
                            print(len(array))
                            for i in range(len(array)):
                              questionArr = array[i].split("\n")
                              print(questionArr)
                              res.append({
                                "question": questionArr[0],
                                "optionA": questionArr[1],
                                "optionB": questionArr[2],
                                "optionC": questionArr[3],
                                "optionD": questionArr[4],
                                "answer": questionArr[5].split("Answer: ")[1]
                              })
                            print(res)
                        else:
                            questionArr = array[0].split("\n")
                            print(questionArr)
                            print("exceptional")
                            res.append({
                                "question": questionArr[0],
                                "optionA": questionArr[1],
                                "optionB": questionArr[2],
                                "optionC": questionArr[3],
                                "optionD": questionArr[4],
                                "answer": array[1].split("Answer: ")[1]
                            })
                            print(res)

                        return jsonify({'data': res})
                else:
                    return jsonify({'data': "no questions "})
            else:
                return "no choices"

        else:
            return "bad req"
    except Exception as e:
        print(e)
        return jsonify({"err": e})



@app.route("/add", methods=["POST"])
def addData():
    try:
        if (request.method == 'POST'):
            mess = request.json["promptMessage"]
            print(mess["question"])
            print(11)
            question = collection.find_one({"question" : mess["question"]})
            print(question)
            if(question):
                print("aaaa")
                return "question already exists in the db"
            else:    
               document = collection.insert_one(mess)
               return "succesfully added"
        else:
            return "bad req"
    except:
        return "error from server"


@app.route("/getTopic", methods=["POST"])
def getQuestions():
    try:
        if (request.method == 'POST'):
            mess = request.json["promptMessage"]
            print(mess)
            document = collection.find({"topic": mess})
            data = list(document)
            if (len(data) > 0):
                def parse_json(data):
                    return json.loads(json_util.dumps(data))
                return parse_json(data)
            else:
                return jsonify({"data": "no related questions"})
        else:
            return "bad req"

    except:
        return "error from server"


if __name__ == "__main__":
    client = pymongo.MongoClient("mongodb+srv://Charan:Charan0608@cluster0.53fa25r.mongodb.net/?retryWrites=true&w=majority")
    db = client["blog"]
    collection = db["sample"]
    app.run(debug=True)
