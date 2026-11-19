from concurrent.futures import ThreadPoolExecutor

def research_agent(goal):
    return {"role":"research","output":"Past events favored a 24-hour format with themed tracks."}
def logistics_agent(goal):
    return {"role":"logistics","output":{"venue":"Grand Hall","venue_cost":45000,"date":"Saturday"}}
def budget_agent(goal):
    return {"role":"budget","output":{"total_cap":30000}}
def judging_agent(goal):
    return {"role":"judging","output":"Judge on innovation, technical depth, and demo quality."}

ROLES={"research":research_agent,"logistics":logistics_agent,"budget":budget_agent,"judging":judging_agent}

def run_swarm(goal):
    print("Launching independent role agents concurrently...")
    with ThreadPoolExecutor(max_workers=len(ROLES)) as pool:
        futures={name:pool.submit(fn,goal) for name,fn in ROLES.items()}
        return {name:future.result() for name,future in futures.items()}

def merge(outputs):
    return {
        "format_notes":outputs["research"]["output"],
        "venue":outputs["logistics"]["output"]["venue"],
        "venue_cost":outputs["logistics"]["output"]["venue_cost"],
        "date":outputs["logistics"]["output"]["date"],
        "budget_cap":outputs["budget"]["output"]["total_cap"],
        "judging_criteria":outputs["judging"]["output"],
    }

def critique(draft):
    conflicts=[]
    if draft["venue_cost"]>draft["budget_cap"]:
        conflicts.append({"conflict":"venue_cost exceeds budget_cap","roles_involved":["logistics","budget"],"logistics_value":draft["venue_cost"],"budget_value":draft["budget_cap"]})
    return conflicts

def resolve(conflict,priority_rule="budget_over_preference"):
    if conflict["conflict"]=="venue_cost exceeds budget_cap":
        return {"rule_applied":priority_rule,"resolution":f"Reject venue at {conflict['logistics_value']}; request logistics propose an alternative under {conflict['budget_value']}."}
    return {"rule_applied":priority_rule,"resolution":"no rule matched"}

if __name__=="__main__":
    outputs=run_swarm("Plan a college AI hackathon")
    print("\\n=== Parallel role outputs ===")
    for name,out in outputs.items(): print(name,":",out["output"])
    draft=merge(outputs)
    print("\\n=== Merged draft plan ===")
    print(draft)
    conflicts=critique(draft)
    print("\\n=== Conflict resolution ===")
    log=[]
    for conflict in conflicts:
        entry={**conflict,**resolve(conflict)}
        log.append(entry)
        print(conflict,"-> resolution:",resolve(conflict))
    print("\\n=== Final conflict log ===")
    for entry in log: print(entry)
