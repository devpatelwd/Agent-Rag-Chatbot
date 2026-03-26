import re
from google import genai
from dotenv import load_dotenv
from ddgs import _DDGSProxy
from fpdf import FPDF
load_dotenv()
ddgs = _DDGSProxy()


gemini_client = genai.Client()

def calculate(expression):
    if re.match(r"^[0-9*+\-/.() ]+$" , expression):
        result = eval(expression)
        return result
    else:
        return "only math bruh"

def search_web(query , result_limit = 3):
    result = ddgs.text(query , max_results=result_limit)

    all_results = []
    for resut in result:

        all_results.append({"title" : resut["title"] , "href" : resut["href"] , "body" : resut["body"]})
    
    return all_results

def search_document(query , collection):
    result = gemini_client.models.embed_content(
        model="gemini-embedding-001",
        contents=query
    )

    
    embeddings = result.embeddings[0].values

    query_result = collection.query(
        query_embeddings = embeddings,
        n_results = 1
    )

    return query_result["documents"][0]

def generate_pdf(content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("helvetica" , "" , 12)

    pdf.multi_cell(
        w = 0,
        h = 6,
        text=content
    )

    pdf.output("output.pdf")
    return "saved pdf as output.pdf"

my_tools = [
    {
        "function_declarations":[
            {
                "name" : "calculate",
                "description" : "calculates a mathematical expression",
                "parameters" : {
                    "type" : "OBJECT",
                    "properties" : {
                        "expression" : {
                            "type" : "STRING",
                            "description" : "the math expression to calculate , for example 89 * 12"
                        }
                    },
                    "required" : ["expression"]
                }
            },

            {
                "name" : "search_web",
                "description" : "Search the web for a query",
                "parameters" : {
                    "type" : "OBJECT",
                    "properties" : {
                        "query":{
                            "type" : "STRING",
                            "description" : "search for a query , eg what is machine learning"
                        }
                    },
                    "required" : ["query"]
                }
            },
            {
                "name" : "search_document",
                "description" : "searching in document uploaded",
                "parameters" : {
                    "type" : "OBJECT",
                    "properties" : {
                        "query" : {
                            "type" : "STRING",
                            "description" : "search query for collection"
                        }
                    } ,
                    "required" : ["query"]
                }
            },
            {
                "name" : "generate_pdf",
                "description" : "generate pdf",
                "parameters" : {
                    "type" : "OBJECT",
                    "properties" :{
                        "content" : {
                            "type" : "STRING",
                            "description" : " for eg , Generate a pdf of summary or answers "
                        }
                    },
                    "required" : ["content"]
                }
            }
        ]
    }
]





