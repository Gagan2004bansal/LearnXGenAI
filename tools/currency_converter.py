from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import requests
import json

from langchain_core.tools import InjectedToolArg
from typing import Annotated

@tool 
def get_coversion_factor(base_currency : str, target_currency : str) -> float:
    """
    Get the conversion factor between two currencies.
    """
    url = "YOUR_API_KEY"
    response = requests.get(url)
    return response.json()

@tool 
def covert(base_currency_value : int, conversion_rate : Annotated[float, InjectedToolArg]) -> float:
    """
    Convert the base currency value to target currency value using conversion rate.
    """

    return base_currency_value * conversion_rate

get_coversion_factor.invoke({"base_currency" : "USD", "target_currency" : "INR"})


# tool binding
llm = ChatOpenAI()

llm_with_tools = llm.bind_tool([get_coversion_factor, covert])

messages = [HumanMessage(content="What is the conversion factor between USD and INR? and based on that what is the value of 100 USD in INR?", additional_kwargs={}, response_metadata={})]

ai_message = llm_with_tools.invoke(messages)
messages.append(ai_message)

print(ai_message.tool_calls)

for tool_call in ai_message.tool_calls:
    # execute the 1st tool call to get the conversion rate
    if tool_call['name'] == 'get_coversion_factor':
        res = get_coversion_factor.invoke(tool_call)
        coversion_rate = json.loads(res.content)['conversion_rate']
        messages.append(res)
    # execute the 2nd tool call to get the converted value
    if tool_call['name'] == 'convert':
        tool_call['args']['conversion_rate'] = coversion_rate
        res = covert.invoke(tool_call)
        messages.append(res)

response = llm_with_tools.invoke(messages)
print(response)