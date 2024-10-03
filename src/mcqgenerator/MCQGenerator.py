import os 
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
from src.mcqgenerator.logger import logging


#imporing necessary packages from langchain
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chains import SequentialChain


#load environment variables from the .env file
load_dotenv()

#keep the key in key variable and access the environment variable just like we would with os.getenv
key=os.getenv("mykey")

#calling my chatopenai 
llm=ChatOpenAI(openai_api_key=key,model_name="gpt-3.5-turbo",temperature=0.3)


#creating my prompt template(input prompt)
#template is nothing just guiding my gpt model
template="""
Text:{text}
You are an expert MCQ maker. Given the above text, it is your job to \
create a quiz  of {number} multiple choice questions for {subject} students in {tone} tone. 
Make sure the questions are not repeated and check all the questions to be conforming the text as well.
Make sure to format your response like  RESPONSE_JSON below  and use it as a guide. \
Ensure to make {number} MCQs
### RESPONSE_JSON
{response_json}


"""

#we have two prompt input and output prompts(collection of words and tokens)5 input variables
quiz_generation_prompt=PromptTemplate(
    input_variables=["text","number","subject","tone","response_json"],
    template=template
)

#create the chain by passing 
#whatever output we get we keep in our quiz variable
quiz_chain=LLMChain(llm=llm,prompts=quiz_generation_prompt,output_key="quiz",verbose=True)

#create second template 
#whatever output store in quiz variable and we are getting then passing in this
template2="""You are an expert english grammarian and writer. Given a Multiple Choice Quiz for {subject} students.\
You need to evaluate the complexity of the question and give a complete analysis of the quiz. Only use at max 50 words for complexity analysis. 
if the quiz is not at per with the cognitive and analytical abilities of the students,\
update the quiz questions which needs to be changed and change the tone such that it perfectly fits the student abilities
Quiz_MCQs:
{quiz}

Check from an expert English Writer of the above quiz:
"""

quiz_evaluation_prompt=PromptTemplate(input_variables=["subject","quiz"],template=template2)

#defined my second chain and output store in review variav]blr
review_chain=LLMChain(llm=llm,prompt=quiz_evaluation_prompt,output_key="review",verbose=True)

#create a sequntial chain to combine review chain and quiz chai
generate_evaluate_chain=SequentialChain(chains=[quiz_chain,review_chain],input_variables=["text","number","subject","tone","response_json"],output_variables=["quiz","review"],verbose=True,)

