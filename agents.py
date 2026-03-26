from google.genai import types
from google import genai
from tools import my_tools , gemini_client , calculate , search_web , search_document , generate_pdf

def agent(user_question , collection):
    history = [types.Content(role="user" , parts=[types.Part(text=user_question)])]

    while True:
        response = gemini_client.models.generate_content(
            model="gemini-3-flash-preview",
            contents=history,
            config= {"tools": my_tools}

        )
        function_call =  response.candidates[0].content.parts[0].function_call

        if function_call:
            history.append(response.candidates[0].content)
            fname = function_call.name
            args = function_call.args

            if fname == "calculate":
                result = calculate(**args)
                
            
            elif fname == "search_web":
                result = search_web(**args)
                
            elif fname == "search_document":
                result = search_document(**args , collection=collection)
                

            elif fname == "generate_pdf":
                result = generate_pdf(**args)
                
            history.append(types.Content(role="user" , parts=[types.Part(
                function_response=types.FunctionResponse(
                    name=fname,
                    response={"result" : result}
                )
            )]))

        else:
            return response.text
        