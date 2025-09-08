from langchain_groq import ChatGroq
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
from langchain.globals import set_verbose, set_debug
from langgraph.prebuilt import create_react_agent
from prompts import *
from states import *
from tools import *
from langgraph.constants import END
from langgraph.graph import StateGraph

_ = load_dotenv()

set_debug(True)
set_verbose(True)


# llm =  ChatGroq(model="openai/gpt-oss-120b")
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
def planner_agent(state:dict)-> dict:
    user_prompt = state['user_prompt']
    res = llm.with_structured_output(Plan).invoke(planner_prompt(user_prompt))
    if res is None:
        raise ValueError("Planner did not return a valid response.")
    return {"plan": res}

def architect_agent(state:dict)-> dict:
    plan = state['plan']
    res = llm.with_structured_output(TaskPlan).invoke(architect_prompt(plan))
    if res is None:
        raise ValueError("Architect did not return a valid response.")
    # To attach plan here, we used ConfigDict(extra="allow") in TaskPlan class
    # This is to maintain context
    res.plan = plan
    return {"task_plan": res}

def coder_agent(state:dict)-> dict:
    coder_state =  state.get('coder_state')
    if coder_state is None:
        coder_state = CoderState(task_plan=state['task_plan'],current_step_idx=0)

    steps = coder_state.task_plan.implementation_steps
    if coder_state.current_step_idx >= len(steps):
        return {"coder_state": coder_state,"status": "DONE"}


    current_task = steps[coder_state.current_step_idx]
    existing_content = read_file.run(current_task.filepath)
    user_prompt = (
        f"Task: {current_task.task_description}\n"
        f"File: {current_task.filepath}\n"
        f"Existing content: \n{existing_content}"
        "Use write_file(path,content) to save your changes."
    )

    system_prompt =  coder_system_prompt()
    coder_tools = [read_file, write_file, list_files, get_current_directory]
    react_agent = create_react_agent(llm,coder_tools)
    react_agent.invoke({
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    })
    coder_state.current_step_idx += 1

    return {"coder_state": coder_state}

graph = StateGraph(dict)
graph.add_node("planner",planner_agent)
graph.add_node("architect",architect_agent)
graph.add_node("coder",coder_agent)
graph.add_edge("planner","architect")
graph.add_edge("architect","coder")
graph.add_conditional_edges(
    'coder',
    lambda s: "END" if s.get("status") == "DONE" else "coder",
    {"END": END,"coder": "coder"}
)
graph.set_entry_point("planner")


agent = graph.compile()

if __name__ == "__main__":
    user_prompt="Create a simple calculator web application"
    result = agent.invoke({"user_prompt":user_prompt}, {"recursion_limit":100})
    print(result)