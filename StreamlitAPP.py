import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file,get_table_data
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging


#load the response (loading json file)
with open(r'C:\Users\PUJA KUMARI\Desktop\mcqgen\Response.json','r') as file:
    RESPONSE_JSON=json.load(file)

#creating a title for the app(create web application)
st.title=("MCQ creator application with LangChain !! ")


#creata a form using st.form
with st.form("user_inputs"):
    #file upload
    uploaded_file=st.file_uploader("Upload a PDF or txt file")

    #input fields
    mcq_count=st.number_input("NO. of MCQs",min_value=3,max_value=50)

    #subjects
    subject=st.text_input("Insert subject",max_chars=20)

    #Quiz tone
    tone=st.text_input("Complexity level of Questions",max_chars=20,placeholder="Simple")

    #add Button
    button=st.form_submit_button("Create MCQs")

    #check if the button is clickd and all fields have input
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading........."):
            try:
                #reading this file which we defined in utils file(defined)
                text=read_file(uploaded_file)
                #count tokens and the cost of API call
                with get_openai_callback() as cb:
                    response=generate_evaluate_chain(
                        {#parameters
                        "text":text,
                        "number":mcq_count,
                        "subject":subject,
                        "tone":tone,
                        "response_json":json.dumps(RESPONSE_JSON)
                        }
                    )

                #st.write(response)
            except Exception as e:
                traceback.print_exception(type(e),e,e.__traceback__)
                st.error("Erros")

            else :
                print(f"Total Tokens:{cb.total_tokens}")
                print(f"Prompt Tokens:{cb.prompt_tokens}")
                print(f"Completion Tokens:{cb.completion_tokens}")
                print(f"Total Cost:{cb.total_cost}")
                if isinstance(response,dict):
                    #extract the quiz data from the response
                    quiz=response.get("quiz",None)
                    if quiz is not None :
                        table_data=get_table_data(quiz)
                        #convert the data into dataframe
                        if table_data is not None:
                            df=pd.DataFrameta(table_data)
                            df.index=df.index+1
                            st.table(df)
                            #Display the review in a text box as well
                            st.text_area(label="Review",value=response["review"])
                        else:
                            st.error("Error in the table data")

                else :
                    st.write(response)
