from concurrent.futures import ThreadPoolExecutor

def research_agent(goal):
    return {"role":"research","output":"Use a 24-hour event with themed tracks."}
def logistics_agent(goal):
    return {"role":"logistics","output":{"venue":"Grand Hall","venue_cost":45000,"date":"Saturday"}}
def budget_agent(goal):
    return {"role":"budget","output":{"total_cap":30000}}
def judging_agent(goal):
    return {"role":"judging","output":"Innovation, technical depth, and demo quality."}
def marketing_agent(goal):
    return {"role":"marketing","output":{"publicity_plan":"Campus posters, social media, and email campaign","marketing_cost":35000}}

ROLES={"research":research_agent,"logistics":logistics_agent,"budget":budget_agent,"judging":judging_agent,"marketing":marketing_agent}

def run_swarm(goal):
    with ThreadPoolExecutor(max_workers=len(ROLES)) as pool:
        futures={name:pool.submit(fn,goal) for name,fn in ROLES.items()}
        return {name:future.result() for name,future in futures.items()}

def merge(o):
    return {"format_notes":o["research"]["output"],"venue":o["logistics"]["output"]["venue"],"venue_cost":o["logistics"]["output"]["venue_cost"],"date":o["logistics"]["output"]["date"],"budget_cap":o["budget"]["output"]["total_cap"],"judging_criteria":o["judging"]["output"],"publicity_plan":o["marketing"]["output"]["publicity_plan"],"marketing_cost":o["marketing"]["output"]["marketing_cost"]}

def critique(d):
    conflicts=[]
    if d["venue_cost"]>d["budget_cap"]:
        conflicts.append({"conflict":"venue_cost exceeds budget_cap","roles_involved":["logistics","budget"],"proposed_cost":d["venue_cost"],"budget_cap":d["budget_cap"]})
    if d["marketing_cost"]>d["budget_cap"]:
        conflicts.append({"conflict":"marketing_cost exceeds budget_cap","roles_involved":["marketing","budget"],"proposed_cost":d["marketing_cost"],"budget_cap":d["budget_cap"]})
    return conflicts

def resolve(c,priority_rule="budget_over_preference"):
    return {"rule_applied":priority_rule,"resolution":f"Reduce or redesign {c['conflict'].split()[0]} proposal from {c['proposed_cost']} to fit within {c['budget_cap']}."}

if __name__=="__main__":
    outputs=run_swarm("Plan a college AI hackathon")
    print("=== Five parallel role outputs ===")
    for name,result in outputs.items(): print(name,":",result["output"])
    draft=merge(outputs)
    print("\\n=== Merged draft ===")
    print(draft)
    print("\\n=== Extended conflict log ===")
    for conflict in critique(draft): print({**conflict,**resolve(conflict)})
