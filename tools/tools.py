from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
import requests


# tool creation
@tool 
def multiply(a: int, b: int) -> int:
    """ Muiltiply two integers together."""
    return a * b


print(multiply.invoke({"a" : 2, "b" : 3}))

print(multiply.name)
print(multiply.description)
print(multiply.args)

# tool binding
llm = ChatOpenAI()
llm_with_tools = llm.bind_tool([multiply])


# tool calling
query = HumanMessage("What is 2 multiplied by 3?")
messages = [query]

result = llm_with_tools.invoke(messages)
messages.apend(result)

# tool execution
# args = result.tool_calls[0]['args']
# multiply.invoke(args)

tool_result = multiply.invoke(result.tool_calls[0])
messages.append(tool_result)

llm_with_tools.invoke(messages)


# Tool Creation, Tool Binding, Tool Calling, Tool Execution